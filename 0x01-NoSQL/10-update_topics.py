#!/usr/bin/env python3
"""
10-update_topics
"""


def update_topics(mongo_collection, name, topics):
    """updates the topics of a school document by its name"""
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )

if __name__ == "__main__":
    update_topics(mongo_collection, name, topics)
