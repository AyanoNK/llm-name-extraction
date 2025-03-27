"""Main file to run the LLM model"""

import datetime
import json
from collections.abc import Callable


from llm import llm_inference
from cli import parser
from prompts import NAME_EXTRACTOR_PROMPT
from evaluations import (
    evaluate_self_check_accuracy,
    response_self_check_llm_version,
    evaluate_correctness,
)


def save_to_json(data: dict):
    """Take the list and save it to a JSON file

    Args:
        data (list[dict]): List of dictionaries to save to a JSON file
    """
    filename = "evaluations/output_{datetime}.json".format(
        datetime=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    )
    with open(filename, "w", encoding="utf-8") as report_file:
        report_file.write(json.dumps(data))


def run_for_txt(filename: str) -> dict:
    """Run the LLM model with the given queries

    Args:
        queries (list[str]): List of queries to send to the LLM model
    """
    print("Reading queries from a .txt file")
    queries = []
    with open(filename, "r", encoding="utf-8") as txt_file:
        user_lines = txt_file.readlines()
        user_lines = [query.strip() for query in user_lines if query.strip()]
        queries = user_lines

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
    self_evaluated = response_self_check_llm_version(responses)
    accuracy = evaluate_self_check_accuracy(self_evaluated)
    results = {
        "results": self_evaluated,
        "accuracy": accuracy,
        "method": "LLM-based Accuracy",
    }
    return results


def run_for_json(filename: str) -> dict:
    """Run the LLM model with the given queries

    Args:
        queries (list[str]): List of queries to send to the LLM model
    """
    print("Reading queries from a .json file")

    with open(filename, "r", encoding="utf-8") as json_file:
        queries = json.load(json_file)

    responses = []

    if not queries:
        return responses

    # TODO: since this is I/O bound, we can parallelize this
    for query in queries:
        parsed_query = NAME_EXTRACTOR_PROMPT.format(sentence=query.get("sentence"))
        llm_response = llm_inference(prompt=parsed_query)
        response_str = llm_response.get("results")[0].get("outputText")
        response = {
            "sentence": query.get("sentence"),
            "names": response_str.strip().replace('"', "").split(", "),
        }
        responses.append(response)

    # self evaluate the responses
    self_evaluated = evaluate_correctness(
        experimental_data=responses, ground_truth=queries
    )
    return self_evaluated


def run_for_str(query: str) -> dict:
    """Run the LLM model with the given query

    Args:
        query (str): Query to send to the LLM model
    """
    print("Running the LLM model with a single query")
    parsed_query = NAME_EXTRACTOR_PROMPT.format(sentence=query)
    llm_response = llm_inference(prompt=parsed_query)
    response_str = llm_response.get("results")[0].get("outputText")
    response = {
        "sentence": query,
        "names": response_str.strip().replace('"', "").split(", "),
    }
    return response


method_mapper: dict[str, Callable[[str]]] = {
    "json": run_for_json,
    "txt": run_for_txt,
    "str": run_for_str,
}

if __name__ == "__main__":
    args = parser.parse_args()
    single_query = args.single_query
    list_queries = args.list_queries
    export = args.export

    user_queries = [single_query]
    runner_payload = single_query

    if single_query:
        func: Callable = method_mapper.get("str", None)

    elif list_queries:
        filetype = list_queries.split(".")[-1]
        func: Callable = method_mapper.get(filetype, None)
        if not func:
            raise ValueError("Please provide a valid file format (.txt or .json)")
        runner_payload = list_queries

    run_result = func(runner_payload)

    print(run_result)
    if export:
        save_to_json(run_result)
