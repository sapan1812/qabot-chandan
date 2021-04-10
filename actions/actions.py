# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from similarity.main import run1
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
import csv,random
import os
import sys

QUESTIONS_FINAL = []
ANSWERS_FINAL = []
USER_DICT = {}
Q_dict = {}
A_dict = {}
csv_data = []
anslist =[]
RAND_ID_LIST=[]
user_input=[]
#
# dirnameTags=sys.path.append(os.path.realpath('..'))
#  # = os.path.dirname(_file_)
# filename_python = os.path.join(dirnameTags, 'python_demo.csv')
# python_dataset = pd.read_csv(filename_python, sep=',')
#python_merged_df = pd.read_csv(python_dataset)

class ActionReady(Action):
    def name(self) -> Text:
        return "action_ready"

    def get_question(self):
        #questions = set()
        with open(r"C:\etc\QABot\project-up1\qabot-chandan\actions\python_demo.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                csv_data.append(row)
                Q_dict[row[1]] = row[4]
        RAND_ID_LIST.extend(random.sample(list(Q_dict.keys()), 5))
        for i in RAND_ID_LIST:
            QUESTIONS_FINAL.append(Q_dict[i])

        for k, v in Q_dict.items():
            a_list = []
            for row in csv_data:
                if str(k) == str(row[1]):
                    a_list.append(row[6])

            A_dict[k] = a_list

        # with open(r"D:\python_demo.csv", "r", encoding="utf-8") as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         questions.add(row[4])
        # QUESTIONS_FINAL.extend(random.sample(list(questions),6))

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        self.get_question()
        # dispatcher.utter_message(text=(str(QUESTIONS_FINAL)))
        # dispatcher.utter_message(text=(" ").join(QUESTIONS_FINAL))

        return []


def send_question():
    for question in QUESTIONS_FINAL:
        yield question


next_question = send_question()


class ActionAskQuestion(Action):
    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question = next(next_question)
        dispatcher.utter_message(text=question)
        # dispatcher.utter_message(text=(" ").join(QUESTIONS_FINAL))

        return []


class ActionGetAnswer(Action):
    def name(self) -> Text:
        return "get_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message['text']

        ANSWERS_FINAL.append(message)

        return []

class ActionGetSimilarity(Action):
    def name(self) -> Text:
        return "get_similarity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #print(ANSWERS_FINAL, "Answers_Final")
        print(RAND_ID_LIST)
        for i in range(0, len(RAND_ID_LIST)):
            USER_DICT[RAND_ID_LIST[i]] = ANSWERS_FINAL[i]
            # print(user_dict)  ## Dict with IDs and User Inputs

        for k, v in USER_DICT.items():
            anslist = A_dict[k]
            user_input.append(v)
            result ='Marks given:' + str(run1(RAND_ID_LIST,anslist,user_input))
            #anslist-->dataset_answers, v-->user_input

        dispatcher.utter_message(text=str(result))
        return []


