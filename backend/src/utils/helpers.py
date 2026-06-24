import os
import re

def load_document(input_path: str):
    
    if not os.path.exists(input_path):
       raise FileNotFoundError(f'The directory {input_path} does not exist!')
    
    with open(input_path, 'r', encoding='utf-8') as f:
        document = f.read()
    
    return document
    
def clean_document(document: str):
    document = document.strip()

    return document

def save_document(document: str,
                  output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(document)
        
def preprocessing_document(input_path: str,
                           output_path: str):
    document = load_document(input_path)
    document = clean_document(document)
    save_document(document, output_path)