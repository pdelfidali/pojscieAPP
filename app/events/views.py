from app.models import Artist, Event, Location, City
from flask import render_template
from . import events


@events.route('/artist/<int:aid>', methods=['GET'])
def show_artist(aid):
    artist = Artist.query.filter_by(aid=aid).first()
    return render_template('artist.html', artist=artist)

@events.route('/events/<int:page_num>', methods=['GET'])
def show_eventlist(page_num):
    events = Event.query.paginate(per_page=5, page=page_num, error_out=True)
    return render_template('events.html', events=events)

@events.route('/event/<int:eid>', methods=['GET'])
def show_event(eid):
    event = Event.query.filter_by(eid=eid).first()
    artist = Artist.query.filter_by(aid=event.artists_aid).first()
    location = Location.query.filter_by(lid=event.lid).first()
    city = City.query.filter_by(cid=location.cid).first()
    return render_template('event.html', event=event, artist=artist, location=location, city=city)