from flask import Flask, render_template, request
import pickle
import requests
import random


app = Flask(__name__)

# Load the model data
movies = pickle.load(open('/Users/sudipkhadka/Desktop/Content-Based-Recommendation-System/model/embedded_name.pkl', 'rb'))
similarity = pickle.load(open('/Users/sudipkhadka/Desktop/Content-Based-Recommendation-System/model/similarity.pkl', 'rb'))

# Define a custom Jinja2 filter to use zip in templates
@app.template_filter('zip')
def zip_filter(a, b):
    return zip(a, b)

def get_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=5c95d31c93eda9617b602d650a5379ec&language=en-US"
    response = requests.get(url).json()
    poster_path = response.get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""

def recommendation(name=None):
    if name:
        index = movies[movies['title'] == name].index[0]
        sim = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recomended_movie_name = [movies.iloc[i[0]].title for i in sim[1:8]]
        recomended_movie_posters = [get_poster(movies.iloc[i[0]].id) for i in sim[1:8]]
    else:
        sample_movies = movies.sample(60)
        recomended_movie_name = sample_movies['title'].tolist()
        recomended_movie_posters = [get_poster(movie_id) for movie_id in sample_movies['id'].tolist()]

    return recomended_movie_name, recomended_movie_posters

@app.route("/", methods=["GET", "POST"])
def home():
    selected_movie = None
    recommended_movies, recommended_posters = [], []
    
    # Handle form submission (POST request)
    if request.method == "POST":
        selected_movie = request.form.get("movie")
        if selected_movie:
            recommended_movies, recommended_posters = recommendation(selected_movie)
    
    # If no movie is selected, show random recommendations (GET request or initial page load)
    if not recommended_movies and not recommended_posters:
        recommended_movies, recommended_posters = recommendation()
    
    # Pass the recommended movies and posters to the template
    return render_template("index.html", movies=recommended_movies, posters=recommended_posters, movie_list=movies['title'].values)

if __name__ == "__main__":
    app.run(debug=True)
