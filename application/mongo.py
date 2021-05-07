from typing import Any, Dict, List

import pymongo

DB = "books"
COLLECTION = "books"


class MongoBackend:
    def __init__(self, uri: str) -> None:
        self._client = pymongo.MongoClient(uri)

    def get_all_books(self) -> List[Dict[str, Any]]:
        return list(self._client[DB][COLLECTION].find({}, {"_id": 0}))

    def get_single_book(self, book_id: str) -> Dict[str, Any]:
        return self._client[DB][COLLECTION].find_one({"book_id": book_id}, {"_id": 0})

    def insert_one_book(self, data: Dict[str, Any]) -> None:
        self._client[DB][COLLECTION].insert_one(data)

    def update_one_book(self, book_id: str, data: Dict[str, Any]) -> None:
        data["book_id"] = book_id
        self._client[DB][COLLECTION].update({"book_id": book_id}, data, upsert=True)

    def delete_one_book(self, book_id: str) -> None:
        self._client[DB][COLLECTION].delete_one({"book_id": book_id})
