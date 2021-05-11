import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Tuple

import flask
import flask_restful

import application.mongo as mongo


class Base(flask_restful.Resource):
    def __init__(self, backend: mongo.MongoBackend) -> None:
        self._base_uri = os.getenv("BASE_URI")
        self._backend = backend

    def add_hyper_link_to_book(self, book: Dict[str, Any]) -> Dict[str, Any]:
        book_id = book.pop("book_id")
        book["_link"] = f"{self._base_uri}/book/{book_id}"
        book["published_year"] = datetime.strftime(book["published_year"], "%Y")
        return book


class Books(Base):
    def get(self) -> Tuple[List[Dict[str, Any]], int]:
        all_books = [
            self.add_hyper_link_to_book(book) for book in self._backend.get_all_books()
        ]
        return all_books, 200

    def post(self) -> Tuple[List[Dict[str, Any]], int]:
        data = flask.request.get_json()
        data["book_id"] = str(uuid.uuid1())
        data["published_year"] = datetime.strptime(str(data["published_year"]), "%Y")
        self._backend.insert_one_book(data=data)
        return [
            self.add_hyper_link_to_book(book) for book in self._backend.get_all_books()
        ], 201


class Book(Base):
    def get(self, book_id: str) -> Tuple[Dict[str, Any], int]:
        book = self._backend.get_single_book(book_id=book_id)
        if book is None:
            return {"message": "No such book exist!!"}, 400
        return self.add_hyper_link_to_book(book), 200

    def put(self, book_id: str) -> Tuple[Dict[str, Any], int]:
        data = flask.request.get_json()
        if self._backend.get_single_book(book_id=book_id) is None:
            return {"message": "No such book exist!!"}, 400
        data["published_year"] = datetime.strptime(str(data["published_year"]), "%Y")
        self._backend.update_one_book(book_id=book_id, data=data)
        return (
            self.add_hyper_link_to_book(self._backend.get_single_book(book_id=book_id)),
            200,
        )

    def delete(self, book_id: str) -> Tuple[Dict[str, Any], int]:
        if self._backend.get_single_book(book_id=book_id) is None:
            return {"message": "No such book exist!!"}, 400
        self._backend.delete_one_book(book_id=book_id)
        return {"message": "Book deleted !!"}, 200
