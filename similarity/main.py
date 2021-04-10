from typing import Any, Text, Dict, List
import warnings

warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import os
import math
import re
from collections import Counter
import spacy


QUESTIONS_FINAL = []
#ANSWERS_FINAL = "The encoder-decoder model provides a pattern for using recurrent neural networks to address challenging sequence-to-sequence prediction problems, such as machine translation"
ACTUAL_ANSWERS_DATASET=[]
#QUESTIONS_DATASET = []
TAGS_DATASET = []
SIMILARITY_RESULT=[]
MESSAGE=""


def run1(rand_id_list,anslist,user_input):
    nlp = spacy.load('en_core_web_sm')
    glv_position = 0
    glv_score = 0
    glv_marks = 0

    ##have to use relative path here
    python_merged_df = pd.read_csv(r"C:\etc\QABot\project-up1\qabot-chandan\actions\Python_Cleaned_Questions.csv")
    for question_random_id in rand_id_list:
        answers_randID = python_merged_df[python_merged_df.Id == int(question_random_id)][['A_Score', 'P_A_Body_wo_freq']]
        answersList = answers_randID['P_A_Body_wo_freq'].tolist()
        answers_randID.A_Score -= answers_randID.A_Score.min()
        answers_randID.A_Score /= answers_randID.A_Score.max()
        answers_randID.A_Score *= (10 - 1)
        answers_randID.A_Score += 1

        scores = answers_randID['A_Score'].tolist()

        for answer in enumerate(anslist):
            doc1 = nlp(answer[1])
            doc2 = nlp(user_input[0])
            # print("spaCy :", doc1.similarity(doc2))

            # print(cos_distance)
            if doc1.similarity(doc2) > glv_score:
                score = doc1.similarity(doc2)
                glv_position = answer[0]
            glv_marks = doc1.similarity(doc2) * scores[answer[0]]

    print("Marks given : ", math.ceil(glv_marks))
    return math.ceil(glv_marks)

# run1(["152580"],['check type object is check it sinc encourag duck type tri object method them look writabl object check subclass tri write method cours sometim nice abstract break isinstanceobj cl need sparingli',
#  'think cool thing dynam languag realli check someth that call requir method object catch attributeerror later allow call method seemingli unrel object accomplish differ task mock object test alot get data web urllib2urlopen return object turn pass almost method read implement read method real sure time place isinst otherwis probabl happyfaceorsmiley',
#  'isinstanceo str link',
#  'isinstanceo str return true str type inherit str typeo str return true str return fals type inherit str',
#  'check type exactli str typeo str check instanc str subclass str thi canon isinstanceo str follow also'
#  ' work case issubclasstypeo str typeo str strsubclass see builtin librari refer relev inform one note case may'
#  ' actual isinstanceo basestr also catch unicod string unicod subclass str str unicod subclass basestr altern '
#  'isinst accept tupl return true x instanc subclass str unicod isinstanceo str unicod'],['this would'])