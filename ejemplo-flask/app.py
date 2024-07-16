from flask import Flask, render_template
import requests
import json

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello_world():
    import requests

    headers = {
        'Authorization': 'Token YOUR_TOKEN_HERE'
    }

    # GET
    r = requests.get("http://127.0.0.1:8000/api/edificios/", auth=('oliver2002', '123'))
    r.content

    # POST
    r = requests.post('http://127.0.0.1:8000/api/edificios/', 
                      data = {'nombre':'Edificio Torre', 
                              'direccion':'Av 25', 
                              'ciudad':'Cuenca', 
                              'tipo':'residencial'}, 
                      auth=('oliver2002', '123'))
    print(r)

    # PUT
    r = requests.put('http://127.0.0.1:8000/api/edificios/1', 
                      data = {'nombre':'Edificio Torre', 
                              'direccion':'Av 25', 
                              'ciudad':'Cuenca', 
                              'tipo':'residencial'}, 
                      auth=('oliver2002', '123'))
    print(r)

    # DELETE
    r = requests.delete('http://127.0.0.1:8000/api/edificios/1/', auth=('oliver2002', '123'))
    print(r)

    return "<p>Flask residencial</p>"

@app.route("/crearedificio")
def crear_edificio():
    import requests

    if requests.method == 'POST':
        nombre = requests.form['nombre']
        direccion = requests.form['direccion']
        ciudad = requests.form['ciudad']
        tipo = requests.form['tipo']
        
        headers = {
            'Authorization': 'Token YOUR_TOKEN_HERE'
        }

        # POST
        r = requests.post('http://127.0.0.1:8000/api/edificios/', 
                          data={'nombre': nombre, 
                                'direccion': direccion, 
                                'ciudad': ciudad, 
                                'tipo': tipo}, 
                          auth=('oliver2002', '123'))

    return render_template("crearedificio.html")

@app.route("/losedificios")
def los_edificios():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/edificios/",
            auth=('oliver2002', '123'))
    edificios = json.loads(r.content)['results']
    numero_edificios = json.loads(r.content)['count']
    return render_template("losedificios.html", edificios=edificios,
    numero_edificios=numero_edificios)


@app.route("/losdepartamentos")
def los_departamentos():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/departamentos/",
            auth=('oliver2002', '123'))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    return render_template("losdepartamentos.html", datos=datos,
    numero=numero)


@app.route("/lostelefonosdos")
def los_telefonos_dos():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/numerosts/",
            auth=('oliver2002', '123'))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    datos2 = []
    for d in datos:
        datos2.append(

        {
        'telefono':d['telefono'],
        'tipo':d['tipo'],
        'estudiante': obtener_estudiante(d['estudiante'])}
        # http://127.0.0.1:8000/api/estudiantes/4/
        # René
        )
    return render_template("lostelefonosdos.html", datos=datos2,
    numero=numero)

# funciones ayuda
def obtener_edificio(url):
    r = requests.get(url, auth=('oliver2002', '123'))
    nombre_edificio = json.loads(r.content)['nombre']
    return nombre_edificio


app.run()
