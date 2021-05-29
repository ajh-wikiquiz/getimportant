import graphene
from pydantic import BaseModel

from typing import Optional, List


class Request(BaseModel):
  text: str


class PhrasesGET(BaseModel):
  text: str
  rank: float
  count: int
  sentences: List[str]


class PhrasesGraphQL(graphene.ObjectType):
  text = graphene.String()
  rank = graphene.Float()
  count = graphene.Int()
  sentences = graphene.List(graphene.String)


class SummaryGET(BaseModel):
  whole: str
  split: List[str]


class SummaryGraphQL(graphene.ObjectType):
  whole = graphene.String()
  split = graphene.List(graphene.String)
