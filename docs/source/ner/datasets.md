# NER Datasets

## Datasets

- CoNLL-2003
    - What is CoNLL data format?
        - [2020 So question](https://stackoverflow.com/questions/27416164/what-is-conll-data-format)
        - [CoNLL-2009 Shared Task](https://ufal.mff.cuni.cz/conll2009-st/task-description.html)
    - [https://www.clips.uantwerpen.be/conll2003/ner/](https://www.clips.uantwerpen.be/conll2003/ner/)
- OntoNotes
- ACE 2004 and ACE 2005  
- Tensorflow Datasets
    - [https://www.tensorflow.org/datasets/catalog/overview](https://www.tensorflow.org/datasets/catalog/overview)
- Hugging Face Datasets
    - [https://huggingface.co/datasets](https://huggingface.co/datasets)
- https://analyticsindiamag.com/most-popular-datasets-for-neural-sequence-tagging-with-the-implementation-in-tensorflow-and-pytorch/ 
- https://lionbridge.ai/datasets/15-free-datasets-and-corpora-for-named-entity-recognition-ner/
## Formats

## Spacy

List of tuples    
  - First tuple: `String`     
  - Second tuple: `Dict`     
      - {'entities' : [(start_index, end_index, 'NER_TAG'), (start_index, end_index, 'NER_TAG'), ...]}   

```
TRAIN_DATA = [
    ('Who is Nishanth?', {
        'entities': [(7, 15, 'PERSON')]
    }),
     ('Who is Kamal Khumar?', {
        'entities': [(7, 19, 'PERSON')]
    }),
    ('I like London and Berlin.', {
        'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
    })
]
```

## [IOB](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)): Inside–outside–beginning (tagging) Format

```
Alex I-PER
is O
going O
to O
Los I-LOC
Angeles I-LOC
in O
California I-LOC
```

## [BILOU]

BILOU format: Beginning, Inside, Last, Outer, Unit.
