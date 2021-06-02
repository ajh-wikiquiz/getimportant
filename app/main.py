from app.lib.cache import cache, get_cache
from app.lib.getimportant import get_phrases, get_summary
from app.lib.models import PhrasesGET, PhrasesGraphQL, SummaryGET, SummaryGraphQL

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
from starlette.graphql import GraphQLApp

from typing import Dict, List

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


# Routes
@app.get('/phrases', response_model=Dict[str, Dict[str, List[PhrasesGET]]], response_class=ORJSONResponse)
@app.get('/phrases/{text}', response_model=Dict[str, Dict[str, List[PhrasesGET]]], response_class=ORJSONResponse)
async def phrases_get(text: str, topn: int = 10):
  return {'data': {'phrases': get_cache(get_phrases, text, topn)}}


@app.get('/summary', response_model=Dict[str, Dict[str, SummaryGET]], response_class=ORJSONResponse)
@app.get('/summary/{text}', response_model=Dict[str, Dict[str, SummaryGET]], response_class=ORJSONResponse)
async def summary_get(text: str, top_phrases: int = 15, top_sentences: int = 5):
  return {'data': {'summary': get_cache(get_summary, text, top_phrases, top_sentences)}}


# GraphQL
class Query(graphene.ObjectType):
  phrases = graphene.List(
    PhrasesGraphQL,
    text=graphene.String(required=True),
    topn=graphene.Int(default_value=10),
  )
  summary = graphene.Field(
    SummaryGraphQL,
    text=graphene.String(required=True),
    top_phrases=graphene.Int(default_value=15),
    top_sentences=graphene.Int(default_value=5),
  )

  def resolve_phrases(parent, info, text, topn):
    return get_cache(get_phrases, text, topn)

  def resolve_summary(parent, info, text, top_phrases, top_sentences):
    return get_cache(get_summary, text, top_phrases, top_sentences)


app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))
