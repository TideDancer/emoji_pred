from __future__ import print_function, division
import json
import csv
import numpy as np
import pandas as pd
import tensorflow as tf
from deepmoji.sentence_tokenizer import SentenceTokenizer
from deepmoji.model_def import deepmoji_emojis
from deepmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH
from flask import Flask, make_response, request

maxlen = 30
batch_size = 32
emoji_lookup = pd.read_csv("emoji-lookup.csv", encoding='utf-8').iloc[:,1].tolist()

with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)
st = SentenceTokenizer(vocabulary, maxlen)
model = deepmoji_emojis(maxlen, PRETRAINED_PATH)
graph = tf.get_default_graph()

def get_emoji(sentences):
    global graph
    with graph.as_default(): 
        tokenized, _, _ = st.tokenize_sentences(sentences)
        prob = model.predict(tokenized)
        emoji = []
        for i, t in enumerate(sentences):
            emoji.append(zip(emoji_lookup,prob[i]))
    return emoji

app = Flask(__name__)

@app.route('/', methods=["POST"])
def emoji_api():
    sentences = request.get_json(force=True)["sentences"]
    emoji = get_emoji(sentences)
    emoji_string = '{\"emoji\":['+','.join(map(lambda y: "[" + (','.join(map(lambda x: "{\"emoji\": \"" + x[0] + "\", \"prob\": " + '{:.20f}'.format(x[1]) + "}",y))) + "]",emoji))+']}'
    to_be_returned = make_response(emoji_string)
    to_be_returned.mimetype ='application/json;charset=utf-8'
    return to_be_returned

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("12345"), debug=True)

