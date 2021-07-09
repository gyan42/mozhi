"""
Refs:
    - https://huggingface.co/transformers/usage.html#named-entity-recognition
"""

from transformers import pipeline
from transformers import AutoModelForTokenClassification, AutoTokenizer
from fastapi import APIRouter

from api.internal.json_models import Text, ExtractedNER

router = APIRouter()
nlp = pipeline("ner")

@router.post("/mozhi/ner/model/transformers")
async def get_ner_tags(data: Text):
    text = data.text
    doc = nlp(text)
    res = {}
    for idx, token in enumerate(doc):
        if token['entity'] == 'O':
            type = "o"
        else:
            type = "ner"
        res[idx] = ExtractedNER(text=token['word'],
                                start=0,
                                label=token['entity'],
                                end=0,
                                type=type)

    return {"predictions": res}