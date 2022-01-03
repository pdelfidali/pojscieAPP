from app.models import Artist
from flask import render_template
from . import events


@events.route('/artist/<string:name>', methods=['GET'])
def show_artist(name):
    artist = Artist.query.filter_by(name=name).first()
    return render_template('artist.html', artist=artist)
