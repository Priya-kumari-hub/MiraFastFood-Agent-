import os
import json
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")

credentials_info = json.loads(def detect_intent_and_params(text, session_id):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    intent_name = response.query_result.intent.display_name
    parameters = dict(response.query_result.parameters)

    return intent_name, parameters

    os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info
)

def detect_intent_text(text, session_id):
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text
