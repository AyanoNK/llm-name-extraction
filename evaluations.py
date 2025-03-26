from llm import llm_inference
from prompts import SELF_EVALUATION_PROMPT
from typing import Optional


def response_self_check_llm_version(evals: list[dict]) -> list[dict]:
    """Given the previous inference,
    check if the names are present in a given sentence
    """
    responses = []
    # TODO: since this is I/O bound, we can parallelize this
    for evaluation in evals:
        parsed_query = SELF_EVALUATION_PROMPT.format(
            sentence=evaluation["sentence"], names=", ".join(evaluation["names"])
        )
        llm_response = llm_inference(prompt=parsed_query)
        response_str = llm_response.get("results")[0].get("outputText")
        response = {
            "query": evaluation["sentence"],
            "names": evaluation["names"],
            "names_ok": response_str.strip().replace('"', "").lower() == "true",
        }
        responses.append(response)

    return responses


def evaluate_self_check_accuracy(results: list[dict]) -> float:
    """Metric to evaluate the self check
    Metric: percentage of names that are correct
    Why: to know how many names are correct in the given sentences

    Args:
        results (list[dict]): List of results from the self check

    Returns:
        float: Percentage of names that are correct
    """
    self_check_acc = sum([1 for x in results if x["names_ok"]]) / len(results)
    return float(self_check_acc) * 100


def find_in_ground_truth(ground_truth: list[dict], query: str) -> Optional[list[str]]:
    """Find the names in the ground truth"""
    for element in ground_truth:
        if element["sentence"] == query:
            return element
    return None


def evaluate_correctness(
    experimental_data: list[dict], ground_truth: list[dict]
) -> float:
    """Given the previous inference,
    check if the names are present in a given sentence
    """
    results = []
    correct = 0
    for evaluation in experimental_data:
        ground_truth_record = find_in_ground_truth(ground_truth, evaluation["sentence"])
        if not ground_truth_record:
            continue

        result = {
            "query": evaluation["sentence"],
            "names": evaluation["names"],
            "names_ok": False,
        }

        if set(ground_truth_record["names"]) == set(evaluation["names"]):
            correct += 1
            result["names_ok"] = True

        results.append(result)

    return {
        "results": results,
        "accuracy": correct / len(experimental_data) * 100,
        "method": "Correctness from ground truth",
    }
