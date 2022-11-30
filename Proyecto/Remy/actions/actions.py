# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import pandas as pd 
from typing import Any, Text, Dict, List
#
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
#
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
#
#
data = pd.read_csv('https://raw.githubusercontent.com/danareyes19/Metodos_computacion_intensiva/main/Proyecto/Recetas.csv')
RECETAS = list(data['Nombre receta'])
INGREDIENTES = list(data['Ingredientes'])
PREPARACION = list(data['Preparación'])

model_name = 'hiiamsid/sentence_similarity_spanish_es'
model = SentenceTransformer(model_name_or_path=model_name, device='cpu')
embedding_bert_train_ing = model.encode(INGREDIENTES, show_progress_bar=True)
embedding_bert_train_rec = model.encode(RECETAS, show_progress_bar=True)
embedding_bert_train_prep = model.encode(PREPARACION, show_progress_bar=True)

class ActionSearchRecipe(Action):

    def name(self) -> Text:
        return "action_search_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) ->  List[Dict[Text, Any]]:
        receta = next(tracker.get_latest_entity_values("recetas"), None)

        if not receta:
            msg = "No entendi lo que me pides."
            dispatcher.utter_message(text=msg)
            return []

        tz_string = RECETAS.get(receta, None)
        if not tz_string:
            msg = f"No tengo la receta {receta}. Intenta de nuevo."
            dispatcher.utter_message(text=msg)
            return []

        msg = f"Ingredientes de la receta {receta}."
        dispatcher.utter_message(text=msg)

        return []

class ActionSearchIngredients():
    def name(self) -> Text:
       return "action_search_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) ->  List[Dict[Text, Any]]:
            ingrediente = next(tracker.get_latest_entity_values("ingrediente"), None)

            embedding_bert_ing = model.encode(ingrediente, show_progress_bar=False)
            similarity_i = cosine_similarity(
            [embedding_bert_ing],
            embedding_bert_train_ing[0:]
        )
            similaridad_i = pd.DataFrame(similarity_i).transpose()
            similaridad_i['Receta'] = recetas['Nombre receta']
            similaridad_i = similaridad_i.rename(columns={0:'Similarity'})
            similaridad_i = similaridad_i.sort_values(by=['Similarity'], ascending=False)

            sug = similaridad_i['Receta'][0:5].values
            msg = f"Te sugiero que preparemos {sug[0]} , ¿qué te parece?"
            dispatcher.utter_message(text=msg)

class ActionCooking(Action):

    def name(self) -> Text:
        return "action_cooking"


class ActionSearchEntities(Action):

    def name(self) -> Text:
        return "action_search_entities"


class ActionChangeRecipe(Action):

    def name(self) -> Text:
        return "action_change_recipe"


class ActionIngredients(Action):

    def name(self) -> Text:
        return "action_ingredients"