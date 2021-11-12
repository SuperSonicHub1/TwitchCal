from flask import Blueprint, request, url_for, redirect, Response, render_template, abort
from .calendar import get_calendar

views = Blueprint("views", __name__, url_prefix="/")

@views.route('/')
def index():
	return render_template("index.html")

@views.route("/goto")
def goto():
	streamer = request.args.get("streamer")
	if not streamer:
		abort(400)
	return redirect(url_for("views.cal", streamer=streamer))

@views.route('/<streamer>.ics')
def cal(streamer: str):
	streamer = streamer.strip().lower()
	cal = get_calendar(streamer)
	return Response(response=cal.to_ical(), mimetype="text/calendar")
