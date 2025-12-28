import os
import json
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")

credentials_info = json.loads(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info
)


def _convert_value(v):
    """
    Converts Dialogflow parameter values to native Python types
    """
    if hasattr(v, "list_value"):
        return [_convert_value(i) for i in v.list_value.values]
    if hasattr(v, "string_value"):
        return v.string_value
    if hasattr(v, "number_value"):
        return int(v.number_value)
    if hasattr(v, "bool_value"):
        return v.bool_value
    return None


def detect_intent_and_params(text, session_id):
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    intent = response.query_result.intent.display_name

    # ✅ SAFE conversion (no protobuf helpers)
    raw_params = response.query_result.parameters
    parameters = {}

    for key, value in raw_params.items():
        parameters[key] = _convert_value(value)

    return intent, parameters
