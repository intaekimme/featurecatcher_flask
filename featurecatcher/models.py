from featurecatcher import db
from flask import current_app


def getVideoTable(tableName):
    tabledict = {
        "__table_args__": {"extend_existing": True},
        "id": db.Column(db.Integer, primary_key=True),
        "person_id": db.Column(db.Integer, nullable=False),
        "frame": db.Column(db.Integer, nullable=False),
        "millisec": db.Column(db.Integer, nullable=False),
        "age": db.Column(db.Integer, nullable=False),
        "gender": db.Column(db.String(10), nullable=False),
        "img_person": db.Column(db.String(100), nullable=False),
        "top_color": db.Column(db.Integer, nullable=False),
        "bottom_color": db.Column(db.Integer, nullable=False),
    }

    newModel = type(tableName, (db.Model,), tabledict)
    return newModel


def getVideoListTable(tableName="video_list"):
    tabledict = {
        "__table_args__": {"extend_existing": True},
        "id": db.Column(db.Integer, primary_key=True),
        "video_name": db.Column(db.String(100), nullable=False),
        "is_processed": db.Column(db.Integer, nullable=False),
    }

    newModel = type(tableName, (db.Model,), tabledict)
    return newModel


class VideoList(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(100), nullable=False)
    is_processed = db.Column(db.Integer, nullable=False)


with current_app.app_context():
    if not db.get_engine().dialect.has_table(db.get_engine(), 'video_list'):
        db.create_all()
        db.session.commit()
    else:
        VideoList = getVideoListTable()