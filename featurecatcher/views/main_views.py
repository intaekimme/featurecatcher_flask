from flask import Blueprint, url_for, current_app, Response, render_template, stream_with_context
from werkzeug.utils import redirect
import cv2
import datetime

from .. import db, savePath
from ..models import VideoList


bp = Blueprint("main", __name__, url_prefix="/")
secondsForNewVideo = 20


@bp.route("/")
def index():
    """Video streaming home page."""
    # now = datetime.datetime.now()
    # timeString = now.strftime("%Y-%m-%d %H:%M:%S")
    # templateData = {"title": "Image Streaming", "time": timeString}
    # return render_template("index.html", **templateData)
    return render_template("content.html")


def compareSeconds(t1, t2, secondsLimit):
    """t1, t2 should be datetime.datetime class \n
    t2 should be the time measured later than t1"""
    assert type(t1) == type(t2) == datetime.datetime and t2 > t1
    assert secondsLimit > 0

    retval = False
    if (t2 - t1).total_seconds() > secondsLimit:
        retval = True

    return retval


def videoWriterFactory(now, codec, fps=30, width=640, height=480):
    """param(now) should be datetime.datetime class"""
    assert type(now) == datetime.datetime
    filename = "{path}/out_{time}.mp4".format(
        path=savePath, time=now.strftime("%Y-%m-%d_%H:%M:%S")
    )
    return filename, cv2.VideoWriter(filename, codec, fps, (width, height))


def gen_frames():
    cap = cv2.VideoCapture(-1)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("frame width: %d, frame height: %d, fps: %d" % (width, height, fps))

    codec = cv2.VideoWriter_fourcc(*"x264")

    t1 = datetime.datetime.now()
    out_name, out = videoWriterFactory(t1, codec)

    while cap.isOpened():
        t2 = datetime.datetime.now()
        if compareSeconds(t1, t2, secondsForNewVideo):
            out.release()
            out_name, out = videoWriterFactory(t2, codec)
            t1 = t2

            # add video description to video list table
            video_list = VideoList(video_name=out_name, is_processed=0)
            print("add video_list table : {file_name}".format(file_name=out_name))
            db.session.add(video_list)
            db.session.commit()

        ret, image = cap.read()
        out.write(image)

        ret, buffer = cv2.imencode(".jpg", image)
        frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    cap.release()
    out.release()


@bp.route("/video_feed")
def video_feed():

    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        stream_with_context(gen_frames()),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )
