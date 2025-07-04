import boto3

from .abstract import AbstractReferenceExtractor


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
        return self._extract_references_from_response(response)

    def _get_response(self, paper_pdf_path: str) -> dict:
        with open(paper_pdf_path, "rb") as f:
            return self._textract.analyze_document(
                Document={"Bytes": f.read()},
                FeatureTypes=["LAYOUT"]
            )

    def _extract_references_from_response(self, response: dict) -> list[str]:
        paragraphs = []

        for block in response["Blocks"]:
            if block["BlockType"] == "LAYOUT_TEXT":
                # Get child relationships to find the actual text
                if "Relationships" in block:
                    for relationship in block["Relationships"]:
                        if relationship["Type"] == "CHILD":
                            child_text = []
                            for child_id in relationship["Ids"]:
                                # Find the child block
                                child_block = next(
                                    (b for b in response["Blocks"] if b["Id"] == child_id),
                                    None
                                )
                                if child_block and child_block["BlockType"] == "LINE":
                                    child_text.append(child_block["Text"])

                            if child_text:
                                paragraphs.append(" ".join(child_text))

        return paragraphs
