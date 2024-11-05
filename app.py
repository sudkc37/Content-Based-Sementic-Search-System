import pickle
import streamlit as st
import requests


def get_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(id)
    response = requests.get(url)
    response = response.json()
    poster_path = response['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommendation(name=None):
    if name:  # Recommendation based on the selected movie, we are using cosin similarity
        index = movies[movies['title'] == name].index[0]
        sim = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recomended_movie_name = []
        recomended_movie_posters = []
        for i in sim[1:8]:
            movie_id = movies.iloc[i[0]].id
            recomended_movie_posters.append(get_poster(movie_id))
            recomended_movie_name.append(movies.iloc[i[0]].title)
    else:  # Random recommendation if no movie is selected
        sample_movies = movies.sample(20)
        recomended_movie_name = sample_movies['title'].tolist()
        recomended_movie_posters = [get_poster(movie_id) for movie_id in sample_movies['id'].tolist()]
        
    return recomended_movie_name, recomended_movie_posters


st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; width: 100%; background-color: black; padding: 10px;">
        <iframe src="https://giphy.com/embed/d1FKUfoSClg4VbJS" style="width: 100%; height: 100%; min-height: 200px;" frameborder="0" allowfullscreen></iframe>
    </div>
    """,
    unsafe_allow_html=True
)


st.header("YourfavouriateMovies.com")
movies = pickle.load(open('/Users/sudipkhadka/Desktop/Content-Based-Recommendation-System/model/embedded_name.pkl', 'rb'))
similarity = pickle.load(open('/Users/sudipkhadka/Desktop/Content-Based-Recommendation-System/model/similarity.pkl', 'rb'))

recomendation_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown", [""] + list(recomendation_list)
)


if "initial_recommendations" not in st.session_state:
    st.session_state["initial_recommendations"] = recommendation()


if st.button('Show movies'):
    if selected_movie.strip() == "":
        recomended_movie_name, recomended_movie_posters = st.session_state["initial_recommendations"]
    else:
        recomended_movie_name, recomended_movie_posters = recommendation(selected_movie)
else:
    recomended_movie_name, recomended_movie_posters = st.session_state["initial_recommendations"]

# Display the movies in a grid layout
cols = st.columns(4)
for i in range(len(recomended_movie_name)):
    with cols[i % 4]:
        st.text(recomended_movie_name[i])
        st.image(recomended_movie_posters[i])


