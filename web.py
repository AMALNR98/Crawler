from gzip import READ
from multiprocessing.spawn import import_main_path
from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

app =Flask("lyrics")
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///lyrics'
db=SQLAlchemy(app)

class Artists(db.Model):
    __tablename__="artists"
    id=db.Column(db.Integer, primary_key = True)
    name =db.Column(db.String)
    songs = db.relationship("Songs",back_populates="artist")

    def __repr__(self):
        return f"Artists('{self.name}')"

class Songs(db.Model):
    __tablename__="songs"
    id=db.Column(db.Integer, primary_key = True)
    name =db.Column(db.String)
    lyrics =db.Column(db.String)
    artist_id =db.Column(db.Integer, db.ForeignKey("artists.id"),nullable=False)
    artist = db.relationship("Artists", back_populates='songs')

    def __repr__(self):
        return f"Songs('{self.name}')"

@app.route("/")
def index():
    artist = Artists.query.all()
    nartist = len(artist)
    # formatted = []
    # for artist in artists:
    #     target = url_for("artist", artist_id = artist.id)
    #     link = f'<a href = "{target}">{artist.name}</a>'
    #     formatted.append(f"<li>{link}</li>")
    #     artists = "".join(formatted)
    #     print(artists)
    return render_template('index.html',artists=artist, no_artists = nartist)

@app.route("/artist/<int:artist_id>")
# def artist(artist_id):
#     return f"<p> I got {artist_id}</p>"
def artist(artist_id):
    songs_ = Songs.query.filter_by(artist_id = artist_id).all()
    nsongs=len(songs_)
    # artist = Artists.query.get(artist_id)

    # formatted = []
    # for i in songs:
    #     target = url_for("song", song_id = i.id)
    #     link = f'<a href = "{target}">{i.name}</a>'
    #     formatted.append(f"<li>{link}</li>")
    #     songs = "".join(formatted)
    # return "<ul>" + "".join(formatted) + "</ul>"
    return render_template('song.html',songs= songs_,no_songs=nsongs)
@app.route("/song/<int:song_id>")
def song(song_id):
    song = Songs.query.filter_by(id = song_id).first()

    lyrics = song.lyrics.replace("\n","<br>")
    return render_template('lyrics.html', song_name =song.name, lyrics=lyrics)