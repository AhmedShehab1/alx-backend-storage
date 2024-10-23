#!/usr/bin/env python3
"""
11-schools_by_topic
"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of schools having a specific topic"""
    return list(mongo_collection.find({"topics": topic}))

if __name__ == "__main__":
    schools_by_topic(mongo_collection, topic)
