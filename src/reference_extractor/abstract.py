from abc import ABC, abstractmethod


class AbstractReferenceExtractor(ABC):

    @abstractmethod
    def extract_references(self, paper_pdf_path: str) -> list[str]:
        raise NotImplementedError
