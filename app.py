from flask import Flask, jsonify, request
from config import Config
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config.from_object(Config)
client = app.test_client()

###########     DB    ###################
engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/tutorials', methods=['GET'])
@jwt_required
def get_list():
    user_id = get_jwt_identity()
    videos = Video.query.filter(Video.user_id == user_id).all()
    serialised = []
    for video in videos:
        item = {
            'id': video.id,
            'name': video.name,
            'description': video.description
        }
        serialised.append(item)
    return jsonify(serialised)


@app.route('/tutorials', methods=['POST'])
@jwt_required
def update_list():
    user_id = get_jwt_identity()
    new_one = request.json
    video = Video(user_id=user_id, **new_one)
    session.add(video)
    session.commit()
    item = {
        'id': video.id,
        'user_id': user_id,
        'name': video.name,
        'description': video.description
    }
    return jsonify(item)


@app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
@jwt_required
def update_tutorial(tutorial_id):
    user_id = get_jwt_identity()
    # item = next((x for x in tutorials if x['id'] == tutorial_id), None)
    search = Video.query.filter(Video.id == tutorial_id,
                                Video.user_id == user_id
                                ).first()
    params = request.json
    if not search:
        return {'message': 'No tutorials with this id'}, 400
    for key, value in params.items():
        setattr(search, key, value)
        session.commit()
    serialised = {
        'id': search.id,
        'name': search.name,
        'description': search.description
    }
    return serialised


@app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
@jwt_required
def delete_list(tutorial_id):
    user_id = get_jwt_identity()
    search = Video.query.filter(Video.id == tutorial_id,
                                Video.user_id == user_id).first()
    if not search:
        return {'message': 'No tutorials with this id'}, 400
    session.delete(search)
    session.commit()
    return '', 204


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authentificate(**params)
    token = user.get_token()

    return {'access_token': token}


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
