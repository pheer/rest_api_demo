import logging.config

from flask import Flask, Blueprint

from rest_api_demo import settings
from rest_api_demo.api import api
from rest_api_demo.api.categories import ns as blog_categories_namespace
from rest_api_demo.api.posts import ns as blog_posts_namespace
from rest_api_demo.database import db

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SERVER_HOST'] = settings.FLASK_SERVER_HOST
    flask_app.config['SERVER_PORT'] = settings.FLASK_SERVER_PORT
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://%s:%d/api/ <<<<<', settings.FLASK_SERVER_HOST, settings.FLASK_SERVER_PORT)
    app.run(host=settings.FLASK_SERVER_HOST, port=settings.FLASK_SERVER_PORT, debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
