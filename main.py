"""Main file to run the LLM model"""

import datetime
import json


from llm import llm_inference
from cli import parser
from prompts import NAME_EXTRACTOR_PROMPT
from evaluations import self_check


def save_to_json(data: list[dict]):
    """Take the list and save it to a JSON file

    Args:
        data (list[dict]): List of dictionaries to save to a JSON file
    """
    filename = "evaluations/output_{datetime}.json".format(
        datetime=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    )
    with open(filename, "w", encoding="utf-8") as report_file:
        results = {
            "results": data,
        }
        report_file.write(json.dumps(results))


def run(queries: list[str]) -> list[dict]:
    """Run the LLM model with the given queries

    Args:
        queries (list[str]): List of queries to send to the LLM model
    """

    responses = []

    if not queries:
        return responses

    # TODO: since this is I/O bound, we can parallelize this
    for query in queries:
        parsed_query = NAME_EXTRACTOR_PROMPT.format(sentence=query)
        llm_response = llm_inference(prompt=parsed_query)
        response_str = llm_response.get("results")[0].get("outputText")
        response = {
            "sentence": query,
            "names": response_str.strip().replace('"', "").split(", "),
        }
        responses.append(response)

    # self evaluate the responses
    self_evaluated = self_check(responses)
    return self_evaluated


if __name__ == "__main__":
    args = parser.parse_args()
    single_query = args.single_query
    list_queries = args.list_queries
    export = args.export

    user_queries = [single_query]

    if list_queries:
        with open(list_queries, "r", encoding="utf-8") as f:
            user_queries = f.readlines()
            user_queries = [query.strip() for query in user_queries if query.strip()]

    run_result = run(user_queries)

    print(run_result)
    if export:
        save_to_json(run_result)
