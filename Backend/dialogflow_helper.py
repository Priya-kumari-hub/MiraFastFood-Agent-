import os
import json
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# ---------------- CONFIG ----------------
PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")

credentials_info = json.loads(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info
)

# ---------------- MAIN FUNCTION ----------------
def detect_intent_and_params(text: str, session_id: str):
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(
        text=text,
        language_code="en"
    )

    query_input = dialogflow.QueryInput(
        text=text_input
    )

    response = session_client.detect_intent(
        request={
            "session": session,
            "query_input": query_input
        }
    )

    intent = response.query_result.intent.display_name

    # Convert parameters safely
    parameters = {}
    proto_params = response.query_result.parameters

    for key in proto_params:
        value = proto_params[key]

        # Repeated fields
        if hasattr(value, "__iter__") and not isinstance(value, str):
            parameters[key] = list(value)
        else:
            parameters[key] = value

    return intent, parameters
