import base64
from datetime import datetime, timedelta
import json
from icalendar import Event, Calendar
from .scraper import get_schedule

ONE_HOUR = timedelta(hours=1)

def get_segment_id(string: str) -> str:
	"""
	For some godforsaken reason, instead of just making the ID the UUID,
	it's Base64-encoded JSON!

	eyJzZWdtZW50SUQiOiI1NTdhYmIwOC01ZmFjLTQyNGItYTUwNy1mYjRkODM0ZWNkNWYiLCJpc29ZZWFyIjoyMDIxLCJpc29XZWVrIjozNH0=

	to

	{"segmentID":"557abb08-5fac-424b-a507-fb4d834ecd5f","isoYear":2021,"isoWeek":34}

	I mean, I guess this is because the same segment can repeat over multiple weeks, but come on! Use a hash or something and then have all of this important stuff be somewhere else!
	"""
	return json.loads(base64.b64decode(string))["segmentID"]

def create_event(segment: dict, user: dict):
	event = Event()

	# Gotta strip the Z
	start_at = datetime.fromisoformat(segment["startAt"][:-1])
	event.add('dtstart', start_at)

	end_at = datetime.fromisoformat(segment["endAt"][:-1]) if segment["endAt"] else start_at + ONE_HOUR
	event.add('dtend', end_at)

	event.add("status", "CANCELLED" if segment["isCancelled"] else "CONFIRMED")

	profile_url = user["profileURL"]
	segment_id = get_segment_id(segment["id"])
	# https://www.twitch.tv/nyanners/schedule?seriesID=f97ab994-eec8-47a2-afec-bbb05cb480d5
	event.add('location', profile_url + "/schedule?seriesID=" + segment_id)
	
	event.add('summary', segment["title"])	

	games = ", ".join(map(lambda x: x["displayName"], segment["categories"]))
	event.add('description', f"Playing {games} @ {profile_url}. ")
	
	event.add('uid', segment["id"])
	return event

def get_calendar(streamer: str):
	data = get_schedule(streamer)
	user = data["user"]
	schedule_segments = user["channel"]["schedule"]["segments"]

	cal = Calendar()
	cal.add('prodid', '-//KAWCCO (@supersonichub1)/EN')
	cal.add('version', '2.0')
	cal.add('name', f"{user['displayName']}'s Schedule")
	cal.add("method", "PUBLISH")

	events = map(lambda x: create_event(x, user), schedule_segments)
	for event in events:
		cal.add_component(event)

	return cal
