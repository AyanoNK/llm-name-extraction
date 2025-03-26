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
