from flask import Flask, render_template, jsonify
import random, math

app = Flask(__name__)

# Coordenadas de las ciudades
ciudades_coords = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754, -103.346253),
    'Monterrey': (25.691611, -100.321838),
    'QuintanaRoo': (21.163111, -86.802315),
    'Michohacan': (19.701400, -101.208296),
    'Aguascalientes': (21.876410, -102.264386),
    'CDMX': (19.432713, -99.133183),
    'QRO': (20.597194, -100.386670)
}
nombres_ciudades = list(ciudades_coords.keys())
coordenadas = [ciudades_coords[n] for n in nombres_ciudades]

# Funciones para TSP + Tabú
def distancia(ciudad1, ciudad2):
    return math.sqrt((ciudad1[0] - ciudad2[0])**2 + (ciudad1[1] - ciudad2[1])**2)

def longitud_ruta(ruta, coords):
    return sum(distancia(coords[ruta[i]], coords[ruta[(i + 1) % len(ruta)]]) for i in range(len(ruta)))

def generar_vecinos(ruta):
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i + 1, len(ruta)):
            vecino = ruta[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append((vecino, (ruta[i], ruta[j])))
    return vecinos

def busqueda_tabu(coords, iteraciones=200, tamaño_tabu=15):
    ruta_actual = list(range(len(coords)))
    random.shuffle(ruta_actual)
    mejor_ruta = ruta_actual[:]
    mejor_distancia = longitud_ruta(mejor_ruta, coords)

    lista_tabu = []

    for _ in range(iteraciones):
        vecinos = generar_vecinos(ruta_actual)
        vecinos = sorted(vecinos, key=lambda x: longitud_ruta(x[0], coords))

        for vecino, movimiento in vecinos:
            if movimiento not in lista_tabu:
                ruta_actual = vecino
                distancia_actual = longitud_ruta(ruta_actual, coords)

                if distancia_actual < mejor_distancia:
                    mejor_ruta = ruta_actual[:]
                    mejor_distancia = distancia_actual

                lista_tabu.append(movimiento)
                if len(lista_tabu) > tamaño_tabu:
                    lista_tabu.pop(0)
                break

    return mejor_ruta, mejor_distancia

# Rutas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolver')
def resolver_tsp():
    mejor_ruta_idx, mejor_distancia = busqueda_tabu(coordenadas)
    mejor_ruta_nombres = [nombres_ciudades[i] for i in mejor_ruta_idx]
    coords_ruta = [ciudades_coords[n] for n in mejor_ruta_nombres]

    return jsonify({
        'ruta': mejor_ruta_nombres,
        'distancia': round(mejor_distancia, 4),
        'coordenadas': coords_ruta
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
