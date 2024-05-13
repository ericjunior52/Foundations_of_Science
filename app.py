from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)


# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    actors = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    
    
# Create the database tables
db.create_all()


# Route to display a list of movies
@app.route('/movies')
def movies():
    movie_list = Movie.query.all()
    return render_template('movie/movies.html', movies=movie_list)


# Route to add new movie
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        actors = request.form['actors']
        publication_year = request.form['publication_year']
        new_movie = Movie(title=title, genre=genre, actors=actors, publication_year=publication_year)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('movies'))
    return render_template('movie/add_movie.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)