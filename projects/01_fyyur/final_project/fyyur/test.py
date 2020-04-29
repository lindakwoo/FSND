class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    
    def __repr__(self):
        return f'<Venue {self.start_time}>'


OR TRY BELOW:

past_shows = db.Column(db.ARRAY(db.String))
upcoming_shows = db.Column(db.ARRAY(db.String))


        class Venue(db.Model):
__tablename__ = 'Venue'   
id = db.Column(db.Integer, primary_key=True)   
name = db.Column(db.String)  
city = db.Column(db.String(120))    
state = db.Column(db.String(120))    
address = db.Column(db.String(120))    
phone = db.Column(db.String(120))    
image_link = db.Column(db.String(500))   
facebook_link = db.Column(db.String(120))   
genres = db.Column(db.String(120))    
website = db.Column(db.String(200))   
seeking_talent = db.Column(db.Boolean)   
seeking_description = db.Column(db.String(500)) 
show = db.relationship("Show", backref="venue", lazy=True)

class Artist(db.Model):    
__tablename__ = 'Artist'    
id = db.Column(db.Integer, primary_key=True)   name = db.Column(db.String)    
city = db.Column(db.String(120))    
state = db.Column(db.String(120))    
phone = db.Column(db.String(120))    
genres = db.Column(db.String(120))    
image_link = db.Column(db.String(500))    
facebook_link = db.Column(db.String(120))   
website = db.Column(db.String(200))   
seeking_venue = db.Column(db.Boolean)   
seeking_description = db.Column(db.String(500)) 
show = db.relationship('Show', backref="artist", lazy=True)
‌
class Show(db.Model):    
__tablename__ = 'Show'    
id = db.Column(db.Integer, primary_key=True)   time = db.Column(db.String(20))    
venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))    
artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))    
start_time = db.Column(db.DateTime)


# Returns an integer value representing how many results matched
numberOfUpcomingShows = db.session.query(Venue).join(Shows, Shows.venue_id == Venue.id).filter(Shows.date>now).count()
# Returns a list of upcoming shows. You could then use 'for show in listOfUpcomingShows:' to go through each show.
listOfUpcomingShows = db.session.query(Venue).join(Shows, Shows.venue_id == Venue.id).filter(Shows.date>now).all()
# Returns the PostgreSQL query for this.
numUpcomingShows = db.session.query(Venue).join(Shows, Shows.venue_id == Venue.id).filter(Shows.date>now)

