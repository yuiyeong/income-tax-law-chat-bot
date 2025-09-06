from importlib.resources import as_file, files

from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class IncomeTaxLawDocumentLoader:
    PACKAGE_NAME = "tax_bot"

    SIZE_CHUNK = 2048
    SIZE_OVERLAP = 1024

    def __init__(self, law_filepath: str):
        with as_file(files(self.PACKAGE_NAME).joinpath(law_filepath)) as file_path:
            self.loader = Docx2txtLoader(file_path=file_path)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.SIZE_CHUNK,
            chunk_overlap=self.SIZE_OVERLAP,
        )

    def load_and_split(self) -> list[Document]:
        return self.loader.load_and_split(text_splitter=self.splitter)

    @classmethod
    def create_from_asset(cls) -> "IncomeTaxLawDocumentLoader":
        return cls(law_filepath="assets/income_tax_law.docx")
