from app.lib.getimportant import get_important
from app.lib.models import Request, PhrasesREST, PhrasesGraphQL, Query

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
from starlette.graphql import GraphQLApp
from typing import Dict, List

app = FastAPI()

origins = ['*']

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)


# Routes
@app.get('/phrases', response_model=Dict[str, Dict[str, List[PhrasesREST]]], response_class=ORJSONResponse)
@app.get('/phrases/{text}', response_model=List[PhrasesREST], response_class=ORJSONResponse)
async def phrases_text(text: str):
  return {'data': {'phrases': get_important(text)}}


@app.post('/phrases', response_model=Dict[str, Dict[str, List[PhrasesREST]]], response_class=ORJSONResponse)
async def phrases(request: Request):
  return {'data': {'phrases': get_important(request.text)}}


app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))
