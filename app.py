from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

###########     DB    ###################
engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/tutorials', methods=['GET'])
def get_list():
    videos = Video.query.all()
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
def update_list():
    new_one = request.json
    video = Video(**new_one)
    session.add(video)
    session.commit()
    item = {
        'id': video.id,
        'name': video.name,
        'description': video.description
    }
    return jsonify(item)


@app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
def update_tutorial(tutorial_id):
    # item = next((x for x in tutorials if x['id'] == tutorial_id), None)
    search = Video.query.filter(Video.id == tutorial_id).first()
    params = request.json
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    for key, value in params.items():
        setattr(search, key, value)
        session.commit()
    return params


@app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
def delete_list():
    return jsonify(tutorials)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)
