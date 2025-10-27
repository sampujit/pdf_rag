from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader

def load_all_documents(data_dir: str) -> List[Any]:

    data_path = Path(data_dir).resolve()
    print(f"[DEBUG] Data Path: {data_path}")
    document = []

    pdf_files = list(data_path.glob('**/*.pdf'))
    print(f"[DEBUG] Found {len(pdf_files)} PDF Files: {[str(f) for f in pdf_files]}")
    for pdf_file in pdf_files:
        print(f"[DEBUG] Loading PDF: {pdf_file}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f"[DEBUG] LOaded {len(loaded)} PDF docs from {pdf_file}")
            document.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load PDF {pdf_file}: {e}")

    return document