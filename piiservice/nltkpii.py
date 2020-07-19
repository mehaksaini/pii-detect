import os
import nltk
from nltk import TreebankWordTokenizer
from nltk import pos_tag
from nltk.chunk import ne_chunk
from nltk.corpus import words
from nltk.chunk import tree2conlltags

dirname = os.path.join(os.path.dirname(__file__), '..')
nltk.data.path.append(os.path.join(dirname, 'nltk_data', 'packages'))

class NltkPii:

    PII_TYPE = ['B-PERSON', 'I-PERSON', 'B-GPE', 'I-GPE', 'B-ORGANIZATION', 'I-ORGANIZATION']
    PII_TAG = ['JJ']

    def __call__(self, data):
        tw = TreebankWordTokenizer()
        spans = list(tw.span_tokenize(data))
        tokens = [data[i:j] for i, j in spans]
        pos_tags = pos_tag(tokens)
        ne_tree = ne_chunk(pos_tags)
        iob_tagged = tree2conlltags(ne_tree)
        indices = []
        dict = words.words()
        with_index = zip(iob_tagged, spans)
        for iob_tagged, span in with_index:
            word, tag, category = iob_tagged
            print(word, tag, category)
            if category in self.PII_TAG and word.lower() not in dict:
                indices.append(span)
            elif tag == 'NNP' and word.lower() not in dict:
                indices.append(span)
        return indices



