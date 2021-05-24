from app.lib.getimportant import get_important
from app.lib.models import Request, PhrasesREST, PhrasesGraphQL

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
from os import environ
from starlette.graphql import GraphQLApp
from typing import Dict, List

# Cache
cache = None
if 'FLY_REDIS_CACHE_URL' in environ:
	import redis
	import orjson
	try:
		cache = redis.from_url(environ.get('FLY_REDIS_CACHE_URL'), db=0)
	except redis.exceptions.ConnectionError:
		pass

# Initialization
app = FastAPI()

# Allow CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)


def get_important_cache(text: str) -> list:
	"""Returns the important phrases results from the cache first if found.

	TODO: fix redundant deserialization?
	"""
	if cache:
		try:
			cached_value = cache.get(text)
			if cached_value:
				results = orjson.loads(cached_value.decode())
			else:  # value is not cached yet
				results = get_important(text)
				cache.set(text, orjson.dumps(results))
		except redis.exceptions.ResponseError:
			results = get_important(text)
	else:  # no cache available
		results = get_important(text)
	return results


# Routes
@app.get('/phrases', response_model=Dict[str, Dict[str, List[PhrasesREST]]], response_class=ORJSONResponse)
@app.get('/phrases/{text}', response_model=Dict[str, Dict[str, List[PhrasesREST]]], response_class=ORJSONResponse)
async def phrases_text(text: str):
	return {'data': {'phrases': get_important_cache(text)}}


# GraphQL
class Query(graphene.ObjectType):
	phrases = graphene.List(PhrasesGraphQL, text=graphene.String(required=True))

	def resolve_phrases(parent, info, text):
		return get_important_cache(text)


app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))
