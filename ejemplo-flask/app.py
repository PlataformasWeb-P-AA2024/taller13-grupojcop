from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__, template_folder='templates')
user = 'oliver2002'
password = '123'

@app.route("/")
def index():     
    return render_template("index.html")

@app.route("/crearedificio", methods=['GET', 'POST'])
def crear_edificio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        tipo = request.form['tipo']

        r = requests.post('http://127.0.0.1:8000/api/edificios/', 
                          data={'nombre': nombre, 
                                'direccion': direccion, 
                                'ciudad': ciudad, 
                                'tipo': tipo}, 
                          auth=(user, password))
                          
        if r.status_code == 201:
            return redirect(url_for('los_edificios'))
        else:
            return f"Error al crear el edificio: {r.status_code}"

    return render_template("crearedificio.html")

@app.route("/editaredificio/<int:id>", methods=['GET', 'POST'])
def editar_edificio(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        tipo = request.form['tipo']

        r = requests.put(f'http://127.0.0.1:8000/api/edificios/{id}/', 
                          data={'nombre': nombre, 
                                'direccion': direccion, 
                                'ciudad': ciudad, 
                                'tipo': tipo}, 
                          auth=(user, password))
                          
        if r.status_code == 200:
            return redirect(url_for('los_edificios'))
        else:
            return f"Error al editar el edificio: {r.status_code}"

    r = requests.get(f'http://127.0.0.1:8000/api/edificios/{id}/', auth=(user, password))
    if r.status_code == 200:
        edificio = r.json()
        edificio['id'] = id
        return render_template("editaredificio.html", edificio=edificio)
    else:
        return f"Error al obtener los datos del edificio: {r.status_code}"

@app.route("/eliminaredificio/<int:id>", methods=['GET', 'POST', 'DELETE'])
def eliminar_edificio(id):
    r = requests.delete(f'http://127.0.0.1:8000/api/edificios/{id}/', auth=(user, password))
    
    if r.status_code == 204:
        return redirect(url_for('los_edificios'))
    else:
        return f"Error al eliminar el edificio: {r.status_code}"


@app.route("/creardepartamento", methods=['GET', 'POST'])
def crear_departamento():
    if request.method == 'POST':
        nombre = request.form['nombre']
        costo = request.form['costo']
        numero = request.form['numero']
        edificio_url = request.form['edificio']

        r = requests.post('http://127.0.0.1:8000/api/departamentos/', 
                          data={'nombre_completo_propietario': nombre, 
                                'costo_departamento': costo, 
                                'numero_cuartos': numero, 
                                'edificio': edificio_url}, 
                          auth=(user, password))
                          
        if r.status_code == 201:
            return redirect(url_for('los_departamentos'))
        else:
            return f"Error al crear el departamento: {r.status_code}"

    r = requests.get('http://127.0.0.1:8000/api/edificios/', auth=(user, password))
    edificios = json.loads(r.content)['results']
    
    return render_template("creardepartamento.html", edificios=edificios)

@app.route("/editardepartamento/<int:id>", methods=['GET', 'POST'])
def editar_departamento(id):
    r1 = requests.get("http://127.0.0.1:8000/api/edificios/", auth=(user, password))
    edificios = json.loads(r1.content)['results']
    if request.method == 'POST':
        nombre = request.form['nombre']
        costo = request.form['costo']
        numero = request.form['numero']
        edificio_url = request.form['edificio']

        r = requests.put(f'http://127.0.0.1:8000/api/departamentos/{id}/', 
                          data={'nombre_completo_propietario': nombre, 
                                'costo_departamento': costo, 
                                'numero_cuartos': numero, 
                                'edificio': edificio_url}, 
                          auth=(user, password))
                          
        if r.status_code == 200:
            return redirect(url_for('los_departamentos'))
        else:
            return f"Error al editar el departamento: {r.status_code}"

    r = requests.get(f'http://127.0.0.1:8000/api/departamentos/{id}/', auth=(user, password))
    if r.status_code == 200:
        departamento = r.json()
        departamento['id'] = id
        edificio = obtener_edificio(departamento['edificio'])
        return render_template("editardepartamento.html", departamento=departamento, edificio=edificio, edificios=edificios)
    else:
        return f"Error al obtener los datos del departamento: {r.status_code}"
    
@app.route("/eliminardepartamento/<int:id>", methods=['GET', 'POST', 'DELETE'])
def eliminar_departamento(id):
    r = requests.delete(f'http://127.0.0.1:8000/api/departamentos/{id}/', auth=(user, password))
    
    if r.status_code == 204:
        return redirect(url_for('los_departamentos'))
    else:
        return f"Error al eliminar el departamento: {r.status_code}"

@app.route("/losedificios")
def los_edificios():
    r = requests.get("http://127.0.0.1:8000/api/edificios/", auth=(user, password))
    edificios = json.loads(r.content)['results']
    numero_edificios = json.loads(r.content)['count']
    
    for edificio in edificios:
        edificio['id'] = int(edificio['url'].rstrip('/').split('/')[-1])
        
    return render_template("losedificios.html", edificios=edificios, 
                           numero_edificios=numero_edificios)


@app.route("/losdepartamentos")
def los_departamentos():
    r = requests.get("http://127.0.0.1:8000/api/departamentos/", auth=(user, password))
    departamentos = json.loads(r.content)['results']
    for departamento in departamentos:
        departamento['id'] = int(departamento['url'].rstrip('/').split('/')[-1])
    numero_departamentos = json.loads(r.content)['count']
    datos2 = []
    for d in departamentos:
        datos2.append({
            'id': d['id'],
            'nombre_completo_propietario': d['nombre_completo_propietario'],
            'costo_departamento': d['costo_departamento'],
            'numero_cuartos': d['numero_cuartos'],
            'edificio': obtener_edificio(d['edificio'])
        })

    return render_template("losdepartamentos.html", departamentos=datos2,
                        numero_departamentos=numero_departamentos)


def obtener_edificio(url):
    r = requests.get(url, auth=(user, password))
    nombre_edificio = json.loads(r.content)['nombre']
    return nombre_edificio

app.run()