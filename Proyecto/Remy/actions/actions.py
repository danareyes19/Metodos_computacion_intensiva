# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import pandas as pd 
from typing import Any, Text, Dict, List
#
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
#
#
data = pd.read_csv('https://raw.githubusercontent.com/danareyes19/Metodos_computacion_intensiva/main/Proyecto/Recetas.csv')
RECETAS = list(data['Nombre receta'])

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

