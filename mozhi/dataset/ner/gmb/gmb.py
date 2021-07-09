"""
http://www.let.rug.nl/bjerva/gmb/about.php

GMB(Groningen Meaning Bank) corpus for entity recognition.

GMB is a fairly large corpus with a lot of annotations. Note,
that GMB is not completely human annotated and it’s not considered 100% correct.
The data is labeled using the IOB format (short for inside, outside, beginning).

The following classes appear in the dataset:

    LOC = Geographical Entity
    ORG = Organization
    PER = Person
    GPE = Geopolitical Entity
    TIME = Time indicator
    ART = Artifact
    EVE = Event
    NAT = Natural Phenomenon


"""

import wget
wget.download('https://dldata-public.s3.us-east-2.amazonaws.com/gmb_v_2.2.0_clean.zip', DATA_DIR)