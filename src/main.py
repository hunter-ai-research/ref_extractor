import sys

import config
from reference_extractor import AWSReferenceExtractor

from handler import handle_references


def check_usage() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Bad usage")


def main() -> None:
    try:
        check_usage()
    except:
        print("Usage: python ./src/main.py [path to research pdf]")
        return

    if not all([config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY]):
        print("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables")
        return

    extractor = AWSReferenceExtractor(config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY)
    references = extractor.extract_references(sys.argv[1])

    handle_references(references)


if __name__ == "__main__":
    main()
