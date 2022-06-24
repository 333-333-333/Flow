import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="bd00121678b246fe83a836b53bfc88af",
                                               client_secret="457a6a70dc1b44af880652159e722471",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read user-top-read"))

top50 = sp.current_user_top_tracks(time_range='short_term', limit = 50)

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

canciones = top50['items']
ids_canciones = []
nombres_canciones = []
caracteristicas_canciones = []

for cancion in canciones:
    id_cancion = cancion['id']
    nombre_cancion = cancion['name']
    caracteristica_cancion = sp.audio_features(id_cancion)

    ids_canciones.append(id_cancion)
    nombres_canciones.append(nombre_cancion)
    caracteristicas_canciones.append(caracteristica_cancion[0])

top50_df = pd.DataFrame(caracteristicas_canciones, index = nombres_canciones)
top50_df = top50_df[["id", "acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","valence"]]

for ind in top50_df.index:
    
    acustividad_total += top50_df['acousticness'][ind]
    concertividad_total += top50_df['liveness'][ind]
    cantable_total += top50_df['speechiness'][ind]
    instrumentalidad_total += top50_df['instrumentalness'][ind]
    ruido_total += top50_df['loudness'][ind]
    bailabilidad_total += top50_df['danceability'][ind]
    energia_total += top50_df['energy'][ind]
    felicidad_total+= top50_df['valence'][ind]
    
    if top50_df['mode'[ind]] == 1:
        canciones_en_mayor+=1
    else:
        canciones_en_menor+=1

porcentaje_acustividad = (acustividad_total/len(top50_df.index)) * 100
porcentaje_concertividad = (concertividad_total/len(top50_df.index)) * 100
porcentaje_cantable = (cantable_total/len(top50_df.index)) * 100
porcentaje_instrumentalidad = (instrumentalidad_total/len(top50_df.index)) * 100
porcentaje_ruido = (ruido_total/len(top50_df.index)) * 100
porcentaje_bailabilidad = (bailabilidad_total/len(top50_df.index)) * 100
porcentaje_energia = (energia_total/len(top50_df.index)) * 100
porcentaje_felicidad = (felicidad_total/len(top50_df.index)) * 100




