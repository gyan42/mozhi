from fastapi import APIRouter
from api.internal.json_models import Text, Words
import nltk
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer

router = APIRouter()


@router.post("/mozhi/nlp/tokenize")
def tokenize(data: Text):
    text = data.text
    res = []
    # print(text)
    # try:
    #     spans = list(TreebankWordTokenizer().span_tokenize(text))
    # except LookupError:
    #     nltk.download("punkt")
    #     spans = list(TreebankWordTokenizer().span_tokenize(text))
    # ret = {"tokens": [{"start": s[0], "end": s[1], "text": text[s[0]:s[1]]} for s in spans]}
    # print(ret)
    i = 0
    for t in text.split(" "):
        res.append({"start": i, "end": i + len(t), "text": t})
        i = i + len(t) + 1
    return {"tokens": res}


@router.post("/mozhi/ner/detokenize")
def detokenize(data: Words):
    words = data.words
    return {"text": TreebankWordDetokenizer().detokenize(words)}