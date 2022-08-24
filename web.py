from multiprocessing.spawn import import_main_path
from flask import Flask,url_for
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
    # return "<p> Hello, world</p>"
    artists = Artists.query.all()
    formatted =[]
    for i in artists:
        target = url_for("artist",artist_id=i.id,song_name=i.name)
        link = f"<a href='{target}'>{i.name}</a>"
        formatted.append(f"<li>{link}<li>")
    print(formatted)
    return "<ul>"+"".join(formatted)+"<ul>"

@app.route("/artist/<int:artist_id>")
# def artist(artist_id):
#     return f"<p> I got {artist_id}</p>"
def artist(artist_id):
    artist = Artists.query.filter_by(id = artist_id).first()
    formatted = []
    for song in artist.songs:
        target = url_for("song", song_id=song.id,song_name = song.name)
        link = f'<a href="{target}">{song.name}</a>'
        formatted.append(f"<li>{link}</li>")
    songs_list = "".join(formatted)
    return f"""
<center><h2>Songs by <em>{artist.name}</em></h2></center>
<ol>
{songs_list}
</ol>
"""

@app.route("/song/<int:song_id>")
# def song(song_id):
#     return f"<p> I got {song_id}</p>"

@app.route('/song/<int:song_id><string:song_name>')
def song(song_id,song_name):
    lyrics=Songs.query.filter_by(id=song_id)
    for lyric in lyrics:
        lyrics = lyric.lyrics.replace("\n","<br>")
    return f"""
        <center><h2><em>{song_name}</em><h2></center>
        <center<h3>{lyrics}</h3>
        </center>
        </ol>
        """