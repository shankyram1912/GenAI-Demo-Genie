# Import libraries
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
from google.cloud.discoveryengine_v1.types import Session
import re

# @title Initializate Project configuration
project_id = "genai-e2e-demos"
location = "global" # Values: "global", "us", "eu"
engine_id = "globe-faq-search-homewifi_1741224854099"

def extract_session_lastforwardslash(text):
  """
  Extracts the last part (text or number) following a forward slash from a string.

  Args:
    text: The input string.

  Returns:
    The extracted part as a string, or None if no match is found.
  """
  match = re.search(r'/([^/]+)$', text)
  if match:
    return match.group(1)
  else:
    return None

def create_session(
    project_id: str,
    location: str,
    engine_id: str,
    user_pseudo_id: str,
) -> str:
    """Creates a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
        user_pseudo_id: A unique identifier for tracking visitors. For example, this
          could be implemented with an HTTP cookie, which should be able to
          uniquely identify a visitor on a single device.
    Returns:
        Session ID of the newly created Session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    session = client.create_session(
        # The full resource name of the engine
        parent=f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}",
        session=discoveryengine.Session(user_pseudo_id=user_pseudo_id),
    )

    return extract_session_lastforwardslash(session.name)


def list_sessions(
    project_id: str,
    location: str,
    engine_id: str,
    user_pseudo_id: str,
) -> discoveryengine.ListSessionsResponse:
    """Lists all sessions associated with a data store.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
    Returns:
        discoveryengine.ListSessionsResponse: The list of sessions.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    filter_arg = f'user_pseudo_id="{user_pseudo_id}"'

    # The full resource name of the engine
    parent = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}"

    response = client.list_sessions(
        request=discoveryengine.ListSessionsRequest(
            parent=parent,
            filter=filter_arg,  # Optional: Filter requests by userPseudoId or state
            order_by="update_time",  # Optional: Sort results
        )
    )
    return response

from google.cloud import discoveryengine_v1 as discoveryengine


def delete_session(
    project_id: str,
    location: str,
    engine_id: str,
    session_id: str,
) -> None:
    """Deletes a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
        session_id: The ID of the session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the session
    name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/sessions/{session_id}"

    client.delete_session(name=name)


def get_session(
    project_id: str,
    location: str,
    engine_id: str,
    session_id: str,
) -> discoveryengine.Session:
    """Retrieves a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
        session_id: The ID of the session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the session
    name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/sessions/{session_id}"

    session = client.get_session(name=name)
    return session


def list_all_sessions_for_pseudo_id(
    project_id: str,
    location: str,
    engine_id: str,
    user_pseudo_id: str    
):
  session_list = []
  for session in list_sessions(project_id, location, engine_id, user_pseudo_id):
    session_list.append(extract_session_lastforwardslash(session.name))
  return session_list

def delete_all_sessions_for_pseudo_id(
    project_id: str,
    location: str,
    engine_id: str,
    user_pseudo_id: str    
):
  for session_id in list_all_sessions_for_pseudo_id(project_id, location, engine_id, user_pseudo_id):
    try:
      delete_session(project_id, location, engine_id, session_id)
      print(f"Deleted session: {session_id}")
    except Exception as e:
      print(f"Error deleting session {session_id}: {e}")  

# @title Answer Query Function

def answer_query_homewifi(
    project_id: str,
    location: str,
    engine_id: str,
    query: str,
    user_pseudo_id: str,
    verbose: bool = False,
) -> discoveryengine.AnswerQueryResponse:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.ConversationalSearchServiceClient(
        client_options=client_options
    )

    # The full resource name of the Search serving config
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_serving_config"

    # Optional: Options for query phase
    # The `query_understanding_spec` below includes all available query phase options.
    # For more details, refer to https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/QueryUnderstandingSpec
    query_understanding_spec = discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec(
        query_rephraser_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryRephraserSpec(
            disable=False,  # Optional: Disable query rephraser
            max_rephrase_steps=1,  # Optional: Number of rephrase steps
        ),
        # Optional: Classify query types
        query_classification_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryClassificationSpec(
            types=[
                discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryClassificationSpec.Type.ADVERSARIAL_QUERY,
                discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryClassificationSpec.Type.NON_ANSWER_SEEKING_QUERY,
            ]  # Options: ADVERSARIAL_QUERY, NON_ANSWER_SEEKING_QUERY or both
        ),
    )

    # Optional: Options for answer phase
    # The `answer_generation_spec` below includes all available query phase options.
    # For more details, refer to https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/AnswerGenerationSpec
    answer_generation_spec = discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
        ignore_adversarial_query=False,  # Optional: Ignore adversarial query
        ignore_non_answer_seeking_query=False,  # Optional: Ignore non-answer seeking query
        ignore_low_relevant_content=False,  # Optional: Return fallback answer when content is not relevant
        model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
            model_version="gemini-1.5-flash-001/answer_gen/v2",  # Optional: Model to use for answer generation
        ),
        prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
            preamble="Give a detailed answer strictly based on information available.",  # Optional: Natural language instructions for customizing the answer.
        ),
        include_citations=True,  # Optional: Include citations in the response
        answer_language_code="en",  # Optional: Language code of the answer
    )

    try:
      last_session_id = list_all_sessions_for_pseudo_id(project_id, location, engine_id, user_pseudo_id)[-1]
      print(f"Found search sessions {last_session_id}")
      session_name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/sessions/{last_session_id}"
    except Exception as e:
      new_session_id = create_session(project_id, location, engine_id, user_pseudo_id)
      print(f"Cannot find any ongoing search sessions, creating new one {new_session_id}")
      session_name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/sessions/{new_session_id}"        

    # Initialize request argument(s)
    request = discoveryengine.AnswerQueryRequest(
        serving_config=serving_config,
        query=discoveryengine.Query(text=query),
        session=session_name,  # Optional: include previous session ID to continue a conversation
        query_understanding_spec=query_understanding_spec,
        answer_generation_spec=answer_generation_spec,
    )

    # Make the request
    response = client.answer_query(request)

    # Handle the response
    #if(verbose): print(response)
    return response
	
def faqsearch_homewifi(user_query: str, dfcx_session: str) -> str:
    user_pseudo_id = extract_session_lastforwardslash(dfcx_session)
    return answer_query_homewifi(project_id, location, engine_id, user_query, user_pseudo_id).answer.answer_text