from django.http import HttpResponse
from django.template import Template, Context
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os

ruta_actual = os.getcwd()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="bd00121678b246fe83a836b53bfc88af",
                                               client_secret="457a6a70dc1b44af880652159e722471",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read user-top-read"))

top50 = sp.current_user_top_tracks(time_range='short_term', limit = 50)
nombresCanciones =[]
artistasCanciones =[]
urls_fotos_canciones = []
links_canciones = []
caracteristicas_canciones = []


acustividad_total = 0
concertividad_total = 0
cantable_total= 0
instrumentalidad_total = 0
ruido_total = 0
bailabilidad_total = 0
energia_total = 0

felicidad_total = 0
canciones_en_mayor = 0
canciones_en_menor = 0

for i, cancion in enumerate(top50['items']):
    id_cancion = cancion['id']
    nombresCanciones.append('['+(str)(i+1)+'] : ' + cancion['name'])
    artistasCanciones.append(cancion['artists'][0]['name'])
    urls_fotos_canciones.append(cancion['album']['images'][1]['url'])
    links_canciones.append(cancion['external_urls']['spotify'])
    caracteristicas_canciones.append(sp.audio_features(id_cancion)[0])

caracteristicas_canciones = pd.DataFrame(caracteristicas_canciones, index = nombresCanciones)

for i in caracteristicas_canciones.index:
    
    acustividad_total += caracteristicas_canciones['acousticness'][i]
    concertividad_total += caracteristicas_canciones['liveness'][i]
    cantable_total += caracteristicas_canciones['speechiness'][i]
    instrumentalidad_total += caracteristicas_canciones['instrumentalness'][i]
    ruido_total += caracteristicas_canciones['loudness'][i]
    bailabilidad_total += caracteristicas_canciones['danceability'][i]
    energia_total += caracteristicas_canciones['energy'][i]
    felicidad_total+= caracteristicas_canciones['valence'][i]
    
    if caracteristicas_canciones['mode'][i] == 1:
        canciones_en_mayor+=1
    else:
        canciones_en_menor+=1
cantidad_canciones = len(nombresCanciones)

porcentaje_acustividad = round((acustividad_total/cantidad_canciones)*100,2)
porcentaje_concertividad = round((concertividad_total/cantidad_canciones)*100,2)
porcentaje_cantable = round((cantable_total/cantidad_canciones)*100,2)
porcentaje_instrumentalidad = round((instrumentalidad_total/cantidad_canciones)*100,2)
porcentaje_ruido = round((ruido_total/cantidad_canciones)*100,2)
porcentaje_bailable = round((bailabilidad_total/cantidad_canciones)*100,2)
porcentaje_energia = round((energia_total/cantidad_canciones)*100,2)
porcentaje_felicidad = round((felicidad_total/cantidad_canciones)*100,2)
    
usuario = sp.current_user();
nombre_usuario = usuario['display_name']

foto_usuario= usuario['images']
url_foto_usuario = foto_usuario[0]['url']

canciones_en_mayor= str(canciones_en_mayor)
canciones_en_menor= str(canciones_en_menor)

def top50(request):
    
    pagina_top50= open (ruta_actual+"/spotify/paginas/top50.html")
    plantilla_top50 = Template(pagina_top50.read())
    pagina_top50.close()
    canciones = zip(nombresCanciones,artistasCanciones, urls_fotos_canciones,links_canciones)
    ctx = Context({
    "canciones":canciones, 
    "foto_usuario":url_foto_usuario, 
    "nombre_usuario":nombre_usuario,
    "canciones_en_mayor":canciones_en_mayor,
    "canciones_en_menor":canciones_en_menor,
    "cantidad_canciones": cantidad_canciones,
    "acustividad": porcentaje_acustividad,
    "concertividad" : porcentaje_concertividad,
    "cantables" : porcentaje_cantable,
    "instrumentales": porcentaje_instrumentalidad,
    "bailables": porcentaje_bailable,
    "energeticas": porcentaje_energia,
    "felices": porcentaje_felicidad})
    retorno = plantilla_top50.render(ctx)

    return HttpResponse(retorno)

