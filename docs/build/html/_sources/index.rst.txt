.. Mozhi documentation master file, created by
   sphinx-quickstart on Mon Apr 13 12:10:20 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html

Welcome to Mozhi's documentation!
====================================

NER is an information extraction technique to identify and classify named entities in text.
It’s a process where an algorithm takes a string of text (sentence or paragraph) as input and identifies
relevant nouns (mainly people, places, and organizations…) that are mentioned in that string.
NER has a wide variety of use cases in the business like, when you are writing an email and mention time or attaching
a file, Gmail offers to set a calendar notification or remind you to attach the file in case you are sending the email
without an attachment.


Use cases of  NER:

* Extracting important named entities from legal, financial, and medical documents

* Classification and Detection of Fake News : News and publishing houses generate large amounts of online content on a daily basis and managing them correctly is very important to get the most use of each article. Named Entity Recognition can automatically investigate entire articles and expose which are the major people, organizations, and places discussed in them. Knowing the relevant tags for each article helps in automatically classifying the articles in defined hierarchies and enable smooth content discovery. An example of how this work can be seen in the example below.

* Efficient Search Algorithms: Let’s suppose you are intending to design an internal search algorithm for an online publisher that has millions of articles. If for every search query the algo ends up searching all the words in millions of articles, the process will take hell lot of time! Instead, if NER can be run once on all the articles and the relevant entities (tags) associated with each of those articles are stored separately, this could speed up the search process incredibly! With this approach, a search term will be matched with only the small list of entities discussed in each article leading to faster search execution.

* Customer Support: There are a number of ways to make the process of customer feedback procedure smooth and easy by using NER. Let’s take an example to understand the process. If you are handling the customer support department of an electronic store with multiple branches worldwide, you go through a number mentions in your customers’ feedback.


Mozhi provides set of tools for end-to-end Named Entity Recognition (NER) NLP tasks, that includes:

* Web based annotation tool
* Data preprocessing
* Model training
* Deploying models

.. image:: ../images/mozhi_image_annotator.png
    :align: center
    :alt: header-img

Contents
========

.. toctree::
   :maxdepth: 1

   setup/setup.rst
   study_materials/study_materials.rst
   ner/ner.rst

API
===

.. toctree::
   :maxdepth: 2

   mozhi/mozhi.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
