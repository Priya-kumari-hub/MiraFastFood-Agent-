from google.cloud import dialogflow_v2 as dialogflow
import uuid
import os

PROJECT_ID = os.getenv("mira-fastfood-tcoq")

def detect_intent_text(text, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text
