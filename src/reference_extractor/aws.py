import boto3

from .abstract import AbstractReferenceExtractor
from . import utils


class AWSReferenceExtractor(AbstractReferenceExtractor):

    def __init__(self, aws_access_key_id: str, aws_access_key_secret: str):
        self._textract = boto3.client(
            "textract",
            region_name="us-east-1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_access_key_secret
        )

    def extract_references(self, paper_pdf_path: str) -> list[str]:
        response = self._get_response(paper_pdf_path)
        paragraphs = self._extract_paragraphs(response)
        return self._find_references(paragraphs)

    def _get_response(self, paper_pdf_path: str) -> dict:
        with open(paper_pdf_path, "rb") as f:
            return self._textract.analyze_document(
                Document={"Bytes": f.read()},
                FeatureTypes=["LAYOUT"]
            )

    def _extract_paragraphs(self, response: dict) -> list[str]:
        paragraphs = []

        for block in response["Blocks"]:
            if block["BlockType"] == "LAYOUT_TEXT":
                if "Relationships" in block:
                    parent_indent = block["Geometry"]["BoundingBox"]["Left"]
                    current_paragraph = []

                    for relationship in block["Relationships"]:
                        if relationship["Type"] == "CHILD":
                            for child_id in relationship["Ids"]:
                                child_block = next(
                                    (b for b in response["Blocks"] if b["Id"] == child_id),
                                    None
                                )
                                if child_block and child_block["BlockType"] == "LINE":
                                    child_indent = child_block["Geometry"]["BoundingBox"]["Left"]

                                    # If indent is same or less than parent, start a new paragraph
                                    if current_paragraph and child_indent <= parent_indent + 0.01:
                                        paragraphs.append(" ".join(current_paragraph))
                                        current_paragraph = []

                                    current_paragraph.append(child_block["Text"])

                    if current_paragraph:
                        paragraphs.append(" ".join(current_paragraph))

        return paragraphs

    def _find_references(self, paragraphs: list[str]) -> list[str]:
        return [
            p for p in paragraphs if utils.is_reference(p)
        ]
