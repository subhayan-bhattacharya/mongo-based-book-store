from typing import Any, Dict, Tuple
import flask
import flask_restful
import mongo
import uuid


class Books(flask_restful.Resource):
    def __init__(self, backend: mongo.MongoBackend) -> None:
        self._backend = backend

    def get(self):
        all_books = self._backend.get_all_books()
        return all_books

    def post(self) -> Tuple[Dict[str, str], int]:
        data = flask.request.get_json()
        data["book_id"] = str(uuid.uuid1())
        self._backend.insert_one_book(data=data)
        return {"message": "Successfully inserted the book"}, 201


class Book(flask_restful.Resource):
    def __init__(self, backend: mongo.MongoBackend) -> None:
        self._backend = backend

    def get(self, book_id: str) -> Dict[str, Any]:
        book = self._backend.get_single_book(book_id=book_id)
        if book is None:
            return {"message": "No such book exist!!"}
        return book

    def delete(self, book_id: str) -> None:
        self._backend.delete_one_book(book_id=book_id)
        return {"message": "Successfully deleted the book"}
