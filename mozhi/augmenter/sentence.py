import random
from transformers import pipeline

# https://www.depends-on-the-definition.com/data-augmentation-with-transformers/
class TransformerAugmenter():
    """
    Use the pretrained masked language model to generate more
    labeled samples from one labeled sentence.
    """

    def __init__(self):
        self.num_sample_tokens = 5
        self.fill_mask = pipeline(
            "fill-mask",
            topk=self.num_sample_tokens,
            model="distilroberta-base"
        )

    def generate(self, sentence, num_replace_tokens=3):
        """Return a list of n augmented sentences."""

        # run as often as tokens should be replaced
        augmented_sentence = sentence.copy()
        for i in range(num_replace_tokens):
            # join the text
            text = " ".join([w[0] for w in augmented_sentence])
            # pick a token
            replace_token = random.choice(augmented_sentence)
            # mask the picked token
            masked_text = text.replace(
                replace_token[0],
                f"{self.fill_mask.tokenizer.mask_token}",
                1
            )
            # fill in the masked token with Bert
            res = self.fill_mask(masked_text)[random.choice(range(self.num_sample_tokens))]
            # create output samples list
            tmp_sentence, augmented_sentence = augmented_sentence.copy(), []
            for w in tmp_sentence:
                if w[0] == replace_token[0]:
                    augmented_sentence.append((res["token_str"].replace("Ġ", ""), w[1], w[2]))
                else:
                    augmented_sentence.append(w)
            text = " ".join([w[0] for w in augmented_sentence])
        return [sentence, augmented_sentence]
