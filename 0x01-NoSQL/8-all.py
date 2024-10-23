#!/usr/bin/env python3
"""
8-all
"""

def list_all(mongo_collection):
    """Lists all documents in a collection"""
    documents = mongo_collection.find()
    return list(documents) if documents else []

if __name__ == "__main__":
    list_all(mongo_collection)
