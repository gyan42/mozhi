NER - Named Entity Recognition
******************************

What is NER?
############

Named entity recognition is a process where an algorithm takes a string of text (sentence or paragraph) as input and
identifies relevant nouns (people, places, organizations, etc.,) that are mentioned in that string. As per Wikipedia,
a named entity is a real-world object (can be abstract or have a physical existence) such as persons,
locations, organizations, products, etc. that can be denoted with a proper name.

NER is part of information extraction task where the goal is to locate and classify such named entities from
unstructured text into predefined categories.

Use cases of NER?
#################

- **Content Recommendations** : Extracting entities from current article and recommending articles with similar entities
- **Customer Support** : Categorizing the feedback based on the entities extracted
- **Research Papers**: Classifying papers base don the entities from each paper/journels
- **Chatbot** : Extracting entities helps in providing relevant recommendations/information based on the mentioned entity.

Methods to extract NER
######################

- Rule based
- Unsupervised approaches

   - Inverse document frequency
   - Shallow syntactic knowledge (e.g. noun phrase chunking)

- Supervised approaches (multi class classification)
- Deep Learning approaches

   - Features : word2vectors, context vectors



.. toctree::
   :maxdepth: 1

   intro.md
   datasets.md
   deeplearning.md
   papers.md
   references.md