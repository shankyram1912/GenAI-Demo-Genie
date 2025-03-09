# Import libraries
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

# @title Initializate Project configuration
project_id = "genai-e2e-demos"
location = "global" # Values: "global", "us", "eu"
engine_id = "globe-faq-search-homewifi_1741224854099"

def answer_query_homewifi(
    project_id: str,
    location: str,
    engine_id: str,
    query: str,
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
            preamble="Give a detailed answer.",  # Optional: Natural language instructions for customizing the answer.
        ),
        include_citations=True,  # Optional: Include citations in the response
        answer_language_code="en",  # Optional: Language code of the answer
    )

    # Initialize request argument(s)
    request = discoveryengine.AnswerQueryRequest(
        serving_config=serving_config,
        query=discoveryengine.Query(text=query),
        session=None,  # Optional: include previous session ID to continue a conversation
        query_understanding_spec=query_understanding_spec,
        answer_generation_spec=answer_generation_spec,
    )

    # Make the request
    response = client.answer_query(request)

    # Handle the response
    if(verbose): print(response)
    return response
	
def faqsearch_homewifi(user_query: str) -> str:
    return answer_query_homewifi(project_id, location, engine_id, user_query).answer.answer_text	
