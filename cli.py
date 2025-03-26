"""ClI parser for the integration tests."""

import argparse

parser = argparse.ArgumentParser("integration_tests_parser")


group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--single-query",
    "-sq",
    help="Single query string to send to the API.",
    type=str,
)

group.add_argument(
    "--list-queries",
    "-lq",
    help=".txt file location to send to the API.",
    type=str,
)
