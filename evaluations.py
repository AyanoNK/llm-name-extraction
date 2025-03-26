from llm import llm_inference
from prompts import SELF_EVALUATION_PROMPT


def self_check(evals: list[dict]) -> list[dict]:
    """Given the previous inference,
    check if the names are present in a given sentence
    """
    responses = []
    # TODO: since this is I/O bound, we can parallelize this
    for evaluation in evals:
        parsed_query = SELF_EVALUATION_PROMPT.format(
            sentence=evaluation["sentence"], names=evaluation["names"]
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
