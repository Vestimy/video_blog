from flask import Flask, jsonify, request
from .config import Config
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from celery import Celery
from flask_cors import CORS

import logging

app = Flask(__name__)
app.config.from_object(Config)
client = app.test_client()

###########     DB    ###################
engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager()

docs = FlaskApiSpec()

cors = CORS(resources={
    r"/*": {"origins": Config.CORS_ALLOWED_ORIGINS}
})
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})
from .models import *
Base.metadata.create_all(bind=engine)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_heandler = logging.FileHandler('log/api.log')
    file_heandler.setFormatter(formatter)
    logger.addHandler(file_heandler)

    return logger


logger = setup_logger()
celery = Celery(
    __name__,
    broker='amqp://async_python:12345@localhost:5672',
    backend='rpc://'
)
celery.conf.task_routes = {
    'pipeline.*': {'queue': 'pipeline'}
}


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from .main.views import videos
from .users.views import users

app.register_blueprint(videos)
app.register_blueprint(users)

docs.init_app(app)
jwt.init_app(app)
