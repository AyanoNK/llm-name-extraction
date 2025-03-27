from unittest.mock import patch
import pytest

from main import run_for_str


@pytest.mark.parametrize(
    "query, return_string, expected_list",
    (
        ("What is Robert's name?", "Robert, Mary", ["Robert", "Mary"]),
        ("Diego is a wonderful person.", "Diego", ["Diego"]),
        ("No one is here.", "", [""]),
    ),
)
@patch("main.llm_inference")
def test_str_impl(mock_llm_inference, query, return_string, expected_list):
    """Test the llm_inference function"""

    mock_llm_inference.return_value = {"results": [{"outputText": return_string}]}

    # Call the function with the mock
    result = run_for_str(query)
    assert result["names"] == expected_list
