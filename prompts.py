"""
This module contains the prompts for the different tasks in the project.
"""

NAME_EXTRACTOR_PROMPT = """
Please provide the names of the people mentioned in the following sentences.
Skip company names and other non-person names.
Skip famous character names.
Only output the names of the people mentioned in the sentence.
Remove any extra spaces and punctuation.

# examples
## input
sentence: "John and Mary went to the park."
## output
"John, Mary"

## input
sentence: "The dog barked at the cat."
## output
""

## input
sentence: "Diego sat on the mat."
## output
"Diego"

## input
sentence: "Donald Trump's administration was crazy at his time at Apple."
## output
"Donald Trump"

## input
sentence: {sentence}
## output
"""


# Issue: if a name is missing, this test might not catch it
SELF_EVALUATION_PROMPT = """
You are an evaluator in charge of verifying if the names given to you are people's names, and appear in a sentence.
Given a sentence and a list of names, verify that all the names are from people, and that they appear in the sentence.


# examples
## input
sentence: "John and Mary went to the park."
names: "John, Mary"
## output
"True"
## reasoning
Both names are people's names and they appear in the sentence.

## input
sentence: "The dog barked at the cat."
names: "John, Mary"
## output
"False"
## reasoning
The names do not appear in the sentence.

## input
sentence: "Diego sat on the mat while talking to Angela."
names: "Diego, Angela, John"
## output
"False"
## reasoning
The name "John" does not appear in the sentence.

## input
sentence: "Mariani, who appears in the Valentine movies, had a terrible accident."
names: "Mariani, who appears in the Valentine movies"
## output
"False"
## reasoning
The name "who appears in the Valentine movies" is not a person's name.

## input
sentence: {sentence}
names: {names}
## output
"""
