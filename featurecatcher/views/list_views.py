from flask import Blueprint, url_for, current_app, Response, render_template, stream_with_context, jsonify
from werkzeug.utils import redirect
import datetime

from .. import db
from ..models import *


bp = Blueprint("list", __name__, url_prefix="/list")
secondsForNewVideo = 20


def parseVideoName(videoPath):
    return videoPath.split('/')[-1].split('.')[0]


@bp.route("/items")
def items():
    processed_videos = db.session.query(VideoList.id, VideoList.video_name, VideoList.is_processed) \
        .filter(VideoList.is_processed == 1).all()

    returnJson = list()
    for video in processed_videos:
        videoId = video[0]
        videoPath = video[1]
        tableName = parseVideoName(videoPath)
        VideoTable = getVideoTable(tableName)
        
        video_time = tableName[4:]
        person_count = db.session.query(VideoTable.person_id.distinct()).count()
        returnJson.append({'video_id' : videoId, 'video_time' : video_time, 'person_count' : person_count})

    return jsonify(returnJson), 200


@bp.route('/items/<int:video_id>')
def detail(video_id):
    """ return value is
        [
            {
                'person_id': n,
                'person_info_list' : [
                    {
                        'frame' : n
                        'millisec' : n
                        'age' : n
                        'gender' : s
                        'img_person' : s
                        'top_color' : n
                        'bottom_color' : n
                    },
                    {
                        ...
                    }
                ]
            },
            {
                'person_id' : n,
                ...
            },
            ...
        ]

    """
    video = VideoList.query.get_or_404(video_id)
    tableName = parseVideoName(video.video_name)
    VideoTable = getVideoTable(tableName)
    
    returnJson = list()

    people = db.session.query(VideoTable.person_id.distinct()).all()

    for person in people:
        personDict = dict()
        person_id = person[0]
        
        personDict['person_id'] = person_id
        personDict['person_info_list'] = list()
        personInfoList = VideoTable.query.filter(VideoTable.person_id == person_id).all()
        
        for personInfo in personInfoList:
            personDict['person_info_list'].append(
                {
                    'frame' : personInfo.frame,
                    'millisec' : personInfo.millisec,
                    'age' : personInfo.age,
                    'gender' : personInfo.gender,
                    'img_person' : personInfo.img_person,
                    'top_color' : personInfo.top_color,
                    'bottom_color' : personInfo.bottom_color
                }
            )
        
        returnJson.append(personDict)

    return jsonify(returnJson), 200