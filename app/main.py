from app.lib.custom_redis_connection import CustomConnection as RedisCustomConnection
from app.lib.getimportant import get_important
from app.lib.models import Request, PhrasesREST, PhrasesGraphQL

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
import orjson
import redis
from starlette.graphql import GraphQLApp

from os import environ
from typing import Dict, List

# Cache
cache = None
env_var = None
if 'REDIS_URL' in environ:
  env_var = 'REDIS_URL'
elif 'FLY_REDIS_CACHE_URL' in environ:
  env_var = 'FLY_REDIS_CACHE_URL'
if env_var:
  try:
    redis_connection_pool = redis.ConnectionPool.from_url(
      url=environ.get(env_var),
      db=0,
      connection_class=RedisCustomConnection
    )
    redis_connection_pool.timeout = 1.0
    redis_connection_pool.max_connections = 10
    cache = redis.Redis(
      connection_pool=redis_connection_pool,
    )
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
  """
  if cache:
    try:
      cached_value = cache.get(text)
      if cached_value:
        results = orjson.loads(cached_value.decode())
      else:  # value is not cached yet
        results = get_important(text)
        cache.set(text, orjson.dumps(results))
    except (
      redis.exceptions.ConnectionError,
      redis.exceptions.TimeoutError,
      redis.exceptions.ResponseError,
      orjson.JSONDecodeError
    ):
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
