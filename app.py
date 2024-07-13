import streamlit as st
import pickle
import pandas as pd
import requests


# Function to get movie poster
def poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=92ffee9cdb0e7145f4e8e33507d72f40&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(poster(movie_id))
    return recommend_movies, recommend_movies_posters


# Load the movie data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page configuration
st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .css-18e3th9 {
            padding-top: 2rem;
        }
        .stButton button {
            background-color: #1DB954;
            color: white;
        }
        .movie-title {
            text-align: center;
            color: #1DB954;
            font-size: 20px;
        }
        .movie-poster {
            display: flex;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)

# Page title and description
st.title('🎬 Movie Recommender System')
st.markdown("""
    ### Discover Your Perfect Movie Match!
    Select a movie you like, and we'll recommend similar movies that you might enjoy.
""")

# Movie selection
selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

# Recommendation button
if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    st.markdown("### Recommended Movies")
    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"<div class='movie-title'>{name}</div>", unsafe_allow_html=True)
            st.image(poster, use_column_width=True, caption=name, output_format='JPEG')

# Sidebar with additional information
st.sidebar.header("About")
st.sidebar.markdown("""
    This Movie Recommender System uses a collaborative filtering algorithm to suggest movies 
    based on your preferences. Select a movie to get started and discover new favorites!
""")
st.sidebar.image("https://via.placeholder.com/150?text=Movie+Recommender", use_column_width=True)

# Footer
st.markdown("""
    <style>
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
