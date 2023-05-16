import requests
import streamlit as st
from CSS_styles import apply_styles
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = "91338b7f94f789d802932916cc246ea6" # Tu api key de tmdb

API_URL = "https://pimlops-richardl.onrender.com/recomendacion/"

def obtener_recomendaciones(pelicula):
    """
    Esta función realiza una solicitud a la API desarrollada y alojada en Render para obtener recomendaciones de películas.
    
    """
    url = API_URL + pelicula
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        movie = Movie()
        peliculas_recomendadas = []
        for titulo in data['lista recomendada']:
            search = movie.search(titulo)
            if search:
                pelicula_recomendada = {
                    "titulo": search[0].title,
                    "poster": "https://image.tmdb.org/t/p/w500" + search[0].poster_path,
                    "vote_average": search[0].vote_average,
                    "release_date": search[0].release_date
                }
                peliculas_recomendadas.append(pelicula_recomendada)

        return peliculas_recomendadas
    else:
        st.error(f"Error: {response.status_code}")
        
        
apply_styles()

title_placeholder = st.empty()
title_placeholder.markdown("<h1 style='text-align: center;'>SISTEMA DE RECOMENDACIÓN DE PELICULAS</h1>", unsafe_allow_html=True) 
st.sidebar.image("icon.png", width=300)
st.sidebar.title("Pelicula de Referencia")
st.sidebar.write("")
pelicula = st.sidebar.text_input("Ingrese el nombre de la película:")

if st.sidebar.button("Recomendar", key="recomendar", on_click=None, args=None, kwargs=None, help=None):
    if pelicula:
        title_placeholder.markdown("<h1 style='text-align: left;'>Sistema de Recomendación de Peliculas</h1>", unsafe_allow_html=True)
        st.sidebar.write(f"Pelicula selecionada: **{pelicula}**.")
        movie = Movie()
        search = movie.search(pelicula)
        if search:
            poster = "https://image.tmdb.org/t/p/w500" + search[0].poster_path
            st.sidebar.image(poster,width=300) 
        
        recomendaciones = obtener_recomendaciones(pelicula)
        if recomendaciones:
            st.title("Películas recomendadas:")
            movie_number = 1
            for recomendacion in recomendaciones:
                titulo = recomendacion["titulo"]
                poster = recomendacion["poster"]
                vote_average = recomendacion["vote_average"]
                release_date = recomendacion["release_date"]
                release_year = release_date.split("-")[0]
                st.markdown(f"**{movie_number}# {titulo} ({release_year})**")
                st.write(f"(Puntuación: {round(vote_average,1)})")
                if poster:
                    st.image(poster)
                else:
                    st.write("No se encontró el poster de la película.")
                movie_number += 1
                
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.markdown("[Link del Repositorio](https://github.com/caozrich/ML_DevOps-Movie-Recomendation-System)")            
