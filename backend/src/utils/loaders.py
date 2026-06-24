from langchain_community.document_loaders import TextLoader
import os

def load_document(doc_path: str):
    print(f'Loading document from {doc_path}')
    
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f'The file does not exist!')
    
    loader = TextLoader(
        file_path = doc_path,
        encoding = 'utf-8'
    )
    
    document = loader.load()
    
    return document