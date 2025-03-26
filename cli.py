"""ClI parser for the integration tests."""

import argparse

parser = argparse.ArgumentParser(prog="integration_tests_parser")


query_type_group = parser.add_mutually_exclusive_group(required=True)
query_type_group.add_argument(
    "--single-query",
    "-sq",
    help="Single query string to send to the API.",
    type=str,
)

query_type_group.add_argument(
    "--list-queries",
    "-lq",
    help=".txt file location to send to the API.",
    type=str,
)


parser.add_argument(
    "--export",
    help="Output file to save the results.",
    action="store_true",
    default=False,
)
