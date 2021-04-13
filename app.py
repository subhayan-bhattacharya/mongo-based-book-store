import resources
import flask
import os
import flask_restful
import mongo

app = flask.Flask(__name__)
api = flask_restful.Api(app)


api.add_resource(
    resources.Books,
    "/books",
    resource_class_kwargs={"backend": mongo.MongoBackend(uri=os.getenv("URI"))},
)

api.add_resource(
    resources.Book,
    "/book/<string:book_id>",
    resource_class_kwargs={"backend": mongo.MongoBackend(uri=os.getenv("URI"))},
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
