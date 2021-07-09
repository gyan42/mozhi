import spacy
from fastapi import APIRouter

from api.internal.json_models import Text, ExtractedNER

router = APIRouter()
nlp = spacy.load("en_core_web_sm")


@router.post("/mozhi/ner/model/spacy")
async def get_ner_tags(data: Text):
    text = data.text
    doc = nlp(text)
    res = {}
    for token in doc:
        if token.ent_type_:
            type = "ner"
        else:
            type = "o"
        res[token.idx] = ExtractedNER(text=token.text,
                                      start=token.idx,
                                      label=token.ent_type_,
                                      end=token.idx + len(token.text),
                                      type=type)
    print(res)
    return {"predictions": res}