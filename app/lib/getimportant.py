import spacy
import pytextrank
from time import perf_counter

# load a spaCy model
nlp = spacy.load('en_core_web_sm')

# add PyTextRank to the spaCy pipeline
nlp.add_pipe('positionrank')


def get_phrases(text: str, topn: int = 10) -> list:
  """Returns important phrases from the text by rank in descending order."""
  doc = nlp(text)
  return [
    {
      'text': phrase.text,
      'rank': phrase.rank,
      'count': phrase.count,
      'sentences': [
        doc[chunk.sent.start : max(chunk.sent.end, chunk.end)].text
        for chunk in phrase.chunks
      ],
    }
    for phrase in doc._.phrases[:topn]  # already sorted
  ]


def get_summary(
  text: str, top_phrases: int = 15, top_sentences: int = 5
) -> list:
  """Returns a summary of the text."""
  doc = nlp(text)
  # Get each individual sentence in the generated summary.
  split = [
    sentence.text for sentence in doc._.textrank.summary(
    limit_phrases=top_phrases, limit_sentences=top_sentences)
  ]
  return {
    'whole': ' '.join(split),
    'split': split,
  }
