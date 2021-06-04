import graphene
from pydantic import BaseModel

from typing import Optional, List


class PhrasesRequestPOST(BaseModel):
  text: str
  topn: int = 10


class PhrasesResponseREST(BaseModel):
  text: str
  rank: float
  count: int
  sentences: List[str]


class PhrasesResponseGraphQL(graphene.ObjectType):
  text = graphene.String()
  rank = graphene.Float()
  count = graphene.Int()
  sentences = graphene.List(graphene.String)


class SummaryRequestPOST(BaseModel):
  text: str
  top_phrases: int = 15
  top_sentences: int = 5


class SummaryResponseREST(BaseModel):
  whole: str
  split: List[str]


class SummaryResponseGraphQL(graphene.ObjectType):
  whole = graphene.String()
  split = graphene.List(graphene.String)
