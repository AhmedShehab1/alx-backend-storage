#!/usr/bin/env python3
"""
12-log_stats
"""
from pymongo import MongoClient


def log_stats():
    """
    provides some stats about nginx logs
    stored in MongoDB
    """
    client = MongoClient()
    db = client.logs
    nginx_collection = db.nginx

    total_logs = nginx_collection.count_documents({})

    method_count = {
        'GET': nginx_collection.count_documents({"method": "GET"}),
        'POST': nginx_collection.count_documents({"method": "POST"}),
        'PUT': nginx_collection.count_documents({"method": "PUT"}),
        'PATCH': nginx_collection.count_documents({"method": "PATCH"}),
        'DELETED': nginx_collection.count_documents({"method": "DELETE"}),
    }

    status_check = nginx_collection.count_documents({"method": "GET", 
                                                     "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
