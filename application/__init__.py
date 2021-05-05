"""Flask application using the application factory pattern."""

import os
import pathlib

import flask
import flask_restful
from dotenv import load_dotenv

import application.mongo as mongo
import application.resources as resources

# load the environment from the file app.env in the project directory
basedir = pathlib.Path(__file__).parent.parent
load_dotenv(basedir / "app.env")


def init_app():
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)
    # Initialize the resources
    api.add_resource(
        resources.Books,
        "/books",
        resource_class_kwargs={
            "backend": mongo.MongoBackend(uri=os.getenv("MONGODB_URI"))
        },
    )

    api.add_resource(
        resources.Book,
        "/book/<string:book_id>",
        resource_class_kwargs={
            "backend": mongo.MongoBackend(uri=os.getenv("MONGODB_URI"))
        },
    )

    return app
