import streamlit as st
import pickle
import pandas as pd
import requests
import time

# 🔹 Use TMDB v3 API key here
API_KEY = "680acd18e76f0d111634e1d0030063e6"

# 🔹 Fetch movie poster using API key in URL
@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w154" + data['poster_path']
    except Exception as e:
        # Log silently (for debugging only)
        print(f"Poster fetch failed for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/300x450?text=No+Image"

# 🔹 Recommender function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        time.sleep(0.5)  # Prevent API overload
    return recommended_movies, recommended_movies_posters

# 🔹 Load data
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# 🔹 Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(3)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"<h4 style='text-align: center; font-size: 16px;'>{names[idx]}</h4>", unsafe_allow_html=True)
            st.image(posters[idx])

