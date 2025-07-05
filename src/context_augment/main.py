#!/usr/bin/env python3

from pathlib import Path
import os
import argparse
import context_augment.core as core
import pickle
from shared.consts import CACHE_FILE_NAME

supported_extensions = [".md", ".markdown", ".html", ".txt"]

def load_documents(docs_path:str):
    docs = []

    for filename in os.listdir(docs_path):
        if any(filename.endswith(ext) for ext in supported_extensions):
            filepath = os.path.join(docs_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                docs.append({
                    "id": filename,
                    "text": text
                })

    return docs


def main():
    parser = argparse.ArgumentParser(description="Process documents and create embeddings")
    parser.add_argument("--docs-dir", required=True, help="Directory containing documents to process")
    parser.add_argument("--output-dir", required=True, help="Directory to save the output cache file")
    
    args = parser.parse_args()

    docs_dir = args.docs_dir
    output_dir = args.output_dir

    docs = load_documents(docs_dir)  # Pass docs_dir to your context_augment

    print(f"Found {len(docs)} documents to embed. Embedding...")

    all_chunks = core.embed_documents(docs)

    cache_path = Path(output_dir) / CACHE_FILE_NAME

    with open(cache_path, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"Cache file written to {cache_path}")

if __name__ == "__main__":
    main()
