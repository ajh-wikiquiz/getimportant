import spacy
import pytextrank


def get_important(text: str) -> list:
  """Returns important phrases from the text by rank in descending order."""
  # load a spaCy model
  nlp = spacy.load('en_core_web_sm')

  # add PyTextRank to the spaCy pipeline
  nlp.add_pipe('textrank')
  doc = nlp(text)

  # return the top-ranked phrases in the document
  return sorted(
    [
      {
        'text': phrase.text,
        'rank': phrase.rank,
        'count': phrase.count,
        'sentences': [
          doc[chunk.sent.start : max(chunk.sent.end, chunk.end)].text
          for chunk in phrase.chunks
        ],
      }
      for phrase in doc._.phrases
    ],
    key=lambda obj: obj['rank'],
    reverse=True,
  )
