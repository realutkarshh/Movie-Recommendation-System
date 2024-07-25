import streamlit as st
import pickle
import pandas as pd
import requests

#https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg

def fetch_image(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkY2VjNTM0MmQzNTZlMWYwYzdiZjk0ZGU1ZGZjMTYyYSIsIm5iZiI6MTcyMTkyMTA2NS4yNDYxOTMsInN1YiI6IjY2YTI2YjA0NTJkNWIzNDEyMTgwZjRlZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.b0N_UL80kig1vAzrxH_CI_9QR1EHEFbOcTGk__AFm3c"
    }

    response = requests.get(url, headers=headers)
    response = response.json()
    return str("https://image.tmdb.org/t/p/w500/" + response["poster_path"])

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    final_recommendation = []
    movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        final_recommendation.append(movies.iloc[i[0]].title)
        movie_posters.append(fetch_image(movie_id))

    return final_recommendation, movie_posters

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    st.write("You Might Like")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.write(names[0])

    with col2:
        st.image(posters[1])
        st.write(names[1])

    with col3:
        st.image(posters[2])
        st.write(names[2])

    with col4:
        st.image(posters[3])
        st.write(names[3])

    with col5:
        st.image(posters[4])
        st.write(names[4])

