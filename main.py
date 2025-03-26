"""Main file to run the LLM model"""

from llm import llm_inference
from cli import parser


def run(queries: list[str]):
    """Run the LLM model with the given queries

    Args:
        queries (list[str]): List of queries to send to the LLM model
    """

    responses = []

    if not queries:
        return responses

    for query in queries:
        llm_response = llm_inference(query)
        response_str = llm_response.get("results")[0].get("outputText")
        response = {
            "query": query,
            "response": response_str.strip(),
        }
        responses.append(response)

    return responses


if __name__ == "__main__":
    args = parser.parse_args()
    single_query = args.single_query
    list_queries = args.list_queries

    user_queries = [single_query]

    if list_queries:
        with open(list_queries, "r", encoding="utf-8") as f:
            user_queries = f.readlines()
            user_queries = [query.strip() for query in user_queries if query.strip()]

    run_result = run(user_queries)
    print(run_result)
