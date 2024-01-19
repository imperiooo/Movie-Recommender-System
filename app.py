import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

def fetch_poster(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movie_id = movies.iloc[movie_index].movie_id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=befe539efcf7dafb3840ff692d3af06c&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + str(data['poster_path'])

def get_movie(arr):
    names = []
    for i in arr:
        names.append(movies.loc[i, 'title'])
    return names

def get_names(ans,movie):
    movie_index = movies[movies['title'] == movie].index[0]
    l = []
    for i in ans:
        indices = np.where(similarity[movie_index] == i)[0]
        l.extend(indices)
    return l

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = sorted(similarity[movie_index], reverse = True)
    l = get_names(distance[1:6], movie)
    ans = get_movie(l)
    recommend_movies = []
    recommend_poster = []
    for i in ans:
        recommend_movies.append(i)
        recommend_poster.append(fetch_poster(i))
    return recommend_movies,recommend_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?', movies['title'].values)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
