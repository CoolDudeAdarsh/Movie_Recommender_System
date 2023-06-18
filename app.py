import pandas as pd
import streamlit as st
import pickle
import requests
import numpy as np

# here i am loading my first_half and second half pickle file
first_half = pickle.load(open('first_half.pkl','rb'))
second_half = pickle.load(open('second_half.pkl','rb'))
similarity = np.concatenate((first_half,second_half))
# my part code over here

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=631018f04bc93b7cac'
                            '4c94bd9cb1bef0'.format(movie_id))
    data = response.json()
    print(data)
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies=[]
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommend_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommend_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies,recommend_movies_poster



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
'Let us pick a Movie for you.......',
movies['title'].values)


if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)

    col1, col2, col3, col4,col5  = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
