#!/usr/bin/env bash
mkdir -p ~/.mozhi/
cp -r data/ ~/.mozhi/

export VF_GLOVE_6B_FILE=~/.mozhi/data/wordvec/glove.6B.zip
if [ -f "$VF_GLOVE_6B_FILE" ]; then
  echo "$VF_GLOVE_6B_FILE exists"
else
  wget http://nlp.stanford.edu/data/glove.6B.zip -O $VF_GLOVE_6B_FILE
  unzip $VF_GLOVE_6B_FILE -d ~/.mozhi/data/wordvec/
fi
export VF_MG_GLOVE_6B_FILE=~/.mozhi/data/wordvec/glove.6B.300d.magnitude
wget http://magnitude.plasticity.ai/glove/medium/glove.6B.300d.magnitude -O $VF_MG_GLOVE_6B_FILE