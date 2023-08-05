import os
import sys

import spacy
import pickle
import numpy as np
import pandas as pd

MODULE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, MODULE)
sys.path.insert(1, os.path.join(MODULE, "pattern"))

from pattern.text.en import modality
from pattern.text.en.modality import mood

import warnings
warnings.filterwarnings('ignore')

try:
    nlp = spacy.load('en_core_web_sm')
except:
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')


def run_init():
    while True:
        try : 
            if modality('I will do it'):
                break
        except:
            pass

run_init()
sys.path.pop(0)
sys.path.pop(1)
   
model_path = os.path.join(MODULE, "model_checkpoint")

def load_models():
    with open(os.path.join(model_path, 'model.pkl'), 'rb') as file:
        LR = pickle.load(file)

    with open(os.path.join(model_path, 'enc_input.pkl'), 'rb') as file:
        enc_input = pickle.load(file)
        
    return LR, enc_input


def get_verb_tenses(s):
    doc = nlp(s)
    pres, past, unk=0, 0, 0
    
    verb_lst = [w for w in doc if (w.pos_=='VERB')]
    
    for v in verb_lst:
        try:
            if v.morph.get('Tense')[0] == 'Pres':
                pres+=1
            elif v.morph.get('Tense')[0] == 'Past':
                past+=1
        except:
            unk+=1
    return [pres, past, unk]


def predict(model_input):
    
    LR, enc_input = load_models()
    
    if isinstance(model_input, str): 
        model_input = pd.DataFrame(data=[model_input], columns=['sentences'])
        
    model_input['mood'] = model_input[model_input.columns[0]].apply(lambda x: mood(x))
    model_input['modality'] = model_input['sentences'].apply(lambda x: modality(x))
    tenses = pd.DataFrame(model_input[model_input.columns[0]].apply(lambda x: get_verb_tenses(x)).to_list())
    model_input['present'], model_input['past'], model_input['unknown'] = tenses[0], tenses[1], tenses[2]
    
    model_input = model_input[model_input.mood != 'subjunctive'].reset_index(drop=True)
    
    model_input['mood'] = enc_input.transform(model_input['mood'])
    
    cols = ['mood', 'modality', 'present', 'past', 'unknown']

    model_input['is_future'] = LR.predict(model_input[cols])
    return model_input[['sentences', 'is_future']]


def predict_proba(model_input):
    
    LR, enc_input = load_models()
    
    if isinstance(model_input, str): 
        model_input = pd.DataFrame(data=[model_input], columns=['sentences'])
        
    model_input['mood'] = model_input[model_input.columns[0]].apply(lambda x: mood(x))
    model_input['modality'] = model_input['sentences'].apply(lambda x: modality(x))
    tenses = pd.DataFrame(model_input[model_input.columns[0]].apply(lambda x: get_verb_tenses(x)).to_list())
    model_input['present'], model_input['past'], model_input['unknown'] = tenses[0], tenses[1], tenses[2]
    
    model_input = model_input[model_input.mood != 'subjunctive'].reset_index(drop=True)
    
    model_input['mood'] = enc_input.transform(model_input['mood'])
    
    cols = ['mood', 'modality', 'present', 'past', 'unknown']

    model_input['is_future'] = LR.predict_proba(model_input[cols])[:,1]
    return model_input[['sentences', 'is_future']]
 

