# LLM Name Extraction

This repository is to extract the names of the LLM students from the LLM website.
The names are extracted using an AWS Bedrock integration using boto3/botocore libraries.

## Installation

1. Clone the repository
2. Create a virtual environment

```bash
python3 -m venv env
```

3. Activate the virtual environment

```bash
source env/bin/activate
```

4. Install the requirements

```bash
pip install -r requirements.txt
```

5. Set up the AWS credentials via env vars by copying the `.env.example` file to `.env` and filling in the necessary information.

## Usage

To call the function using a single sentence, use the following command:

```bash
python main.py --single-query "Robert is an amazing teacher."
# or
python main.py -sq "Robert is an amazing teacher."
```

To call the function using a file, use the following command:

```bash
python main.py --list-queries "path/to/file.txt"
# or
python main.py -lq "path/to/file.txt"
```

Get further information by running the help command

```bash
python main.py --help
```

> [!IMPORTANT]
> The file should be a .txt file.

You can also export the output to a JSON file using the following command:

```bash
python main.py -sq "Robert is an amazing teacher." --export
# or
python main.py -lq "path/to/file.txt" --export
```

The file will be saved in the `evaluations/` directory.

## Metric explanation

### Metric

LLM-based accuracy metric. Based on the LLM response, the number of correct predictions divided by the total number of predictions are calculated.

### Reasoning

LLM based accuracy metric is used because it is a simple metric for beginner/small projects such as this one. It gives a clear indication of how well the model is performing by providing the percentage of correct predictions.

In this case, the accuracy metric will tell us how many of the extracted names are correct compared to the total number of names extracted.

### Shortcomings

The accuracy metric does not take into account the false positives and false negatives. It treats all errors equally, which may not be the case in real-world scenarios. For example, in this case, a false positive (incorrectly extracted name) may be more severe than a false negative (missed name).

Moreover, because the evaluation is done by an LLM as well, the accuracy metric may not be the best metric to use. The LLM may have a bias towards the names they know, which may not be representative of the entire dataset.
