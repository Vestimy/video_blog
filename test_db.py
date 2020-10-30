from models import Video, session

def new_post():
    new = Video(name='Test1', description='Test first')
    session.add(new)
    session.commit()

    test = Video.query.all()

    f