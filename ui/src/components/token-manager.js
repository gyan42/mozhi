/**
 * Token Manager that handles tokenized text for NER tags
 */
class TokenManager {

  // static predefined = {"TOKEN" : "token", "LABEL": "label", "DEFAULT_LABEL" : 'O'}


  static predefined() {
    // remember, this = Article
    return {"TOKEN" : "token", "LABEL": "label", "DEFAULT_LABEL" : 'O'}
  }

  /**
   *
   * @param {Array} tokens, where each token is a tuple of (start index, end index, text)
   */
  constructor(tokens) {

    // For spacy format {start, end, label}
    this.tokens = tokens.map((t) => ({
      start: 'start' in t ? t['start'] : null,
      end: 'end' in t ? t['end'] : null,
      text: 'text' in t ? t['text'] : null,
      type: 'type' in t ? t['type'] : TokenManager.predefined().TOKEN,
      classId: 'classId' in t ? t['classId'] : "",
      label: 'label' in t  ? t['label']: TokenManager.predefined().DEFAULT_LABEL,
    }));
    this.words = tokens.map(t => t['text']);
    console.log(this.tokens)
  }

  /**
   * Creates a new token label block with the tokens whose starts match the input
   * parameters
   *
   * @param {Number} start_index 'start' value of the token forming the start of the token label block
   * @param {Number} end_index 'start' value of the token forming the end of the token label block
   * @param {Object} label_obj the id of the class to highlight
   */
  addNewLabelTag(start_index, end_index, label_obj) {
    console.log("addNewBlock", start_index, end_index, label_obj)
    console.log("this.tokens", this.tokens)
    this.tokens = this.tokens.map((t) => {
      if (t.start >= start_index && t.start <= end_index) {
        t['classID'] = label_obj['id']
        t['label'] = label_obj['name']
        t['type'] = TokenManager.predefined().LABEL
        console.log("text.....", t.text)
      }
      return t

    });
  }

  /**
   * Removes a token block and puts back all the tokens in their original position
   *
   * @param {Number} blockStart 'start' value of the token block to remove
   */
  removeBlock(blockStart) {
    this.tokens = this.tokens.map((t) => {
      if (t.start === blockStart) {
        t['type'] = TokenManager.predefined().TOKEN
        t['classID'] = null
        t['label'] = TokenManager.predefined().DEFAULT_LABEL
      }
      return t
    });
  }

  /**
   * Removes all the tag blocks and leaves only tokens
   */
  resetBlocks() {
    this.tokens = this.tokens.map((t) => {
      t['label'] = TokenManager.predefined().DEFAULT_LABEL
      t['type'] = TokenManager.predefined().TOKEN
      t['classID'] = null
      return t
    });
  }

  /**
   * Exports the tokens and the token blocks as annotations
   */
  exportAsAnnotation() {
    let entities = [];
    for (let i = 0; i < this.tokens.length; i++) {
      if (this.tokens[i].type === TokenManager.predefined().LABEL) {
        let b = this.tokens[i];
        entities.push([b.start, b.end, b.label]);
      }
    }
    return entities;
  }

  /**
   * Export as CoNLL format
   */
  exportASCoNLLAnnotations() {
    let tokens = []
    let entities = [];
    for (let i = 0; i < this.tokens.length; i++) {
      let b = this.tokens[i];
      tokens.push(b.text);
      entities.push(b.label);
    }
    return [tokens, entities]
  }
}

export default TokenManager;
