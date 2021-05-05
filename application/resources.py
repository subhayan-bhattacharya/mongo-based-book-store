import os
import uuid
from typing import Any, Dict, Tuple, List

import flask
import flask_restful

import application.mongo as mongo


class Base(flask_restful.Resource):
    def __init__(self, backend: mongo.MongoBackend) -> None:
        self._backend = backend
        self._base_uri = os.getenv("BASE_URI")

    def add_hyper_link_to_book(self, book: Dict[str, Any]) -> Dict[str, Any]:
        book_id = book.pop("book_id")
        book["_link"] = f"{self._base_uri}/book/{book_id}"
        return book


class Books(Base):
    def get(self) -> List[Dict[str, Any]]:
        all_books = [
            self.add_hyper_link_to_book(book) for book in self._backend.get_all_books()
        ]
        return all_books

    def post(self) -> Tuple[List[Dict[str, Any]], int]:
        data = flask.request.get_json()
        data["book_id"] = str(uuid.uuid1())
        self._backend.insert_one_book(data=data)
        return [
            self.add_hyper_link_to_book(book) for book in self._backend.get_all_books()
        ], 201


class Book(Base):
    def get(self, book_id: str) -> Dict[str, Any]:
        book = self._backend.get_single_book(book_id=book_id)
        if book is None:
            return {"message": "No such book exist!!"}
        return self.add_hyper_link_to_book(book)

    def delete(self, book_id: str) -> List[Dict[str, Any]]:
        self._backend.delete_one_book(book_id=book_id)
        return [
            self.add_hyper_link_to_book(book) for book in self._backend.get_all_books()
        ]
