from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def index(request):
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="bd00121678b246fe83a836b53bfc88af",
                                               client_secret="457a6a70dc1b44af880652159e722471",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read user-top-read"))

    top10 = sp.current_user_top_tracks(time_range='short_term', limit = 10)
    retorno=""
    for i, item in enumerate(top10['items']):
        indice = (str) (i+1)
        retorno+= " [" + indice + ": " + item['name'] + " || " + item['artists'][0]['name'] + "] "

    return HttpResponse(retorno)

