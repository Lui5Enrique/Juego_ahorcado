import random
from flask import Flask, request, session, render_template_string, redirect, url_for

app = Flask(__name__)
# Una clave secreta es necesaria para que Flask "recuerde" la partida entre cada clic
app.secret_key = "super_secreta_ingenieria" 

PALABRAS = ['python', 'java', 'docker', 'linux', 'algoritmo', 'computacion', 'servidor']

# Aquí escribimos el diseño de nuestra página web en HTML y un poco de CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ahorcado Web en Docker</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9;}
        h1 { color: #0db7ed; }
        .palabra { font-size: 3em; letter-spacing: 10px; margin: 20px; font-weight: bold; }
        .mensaje { color: #ff4b4b; font-size: 1.2em; font-weight: bold; height: 30px;}
        .letras { margin-top: 20px; color: #555; }
        input { font-size: 1.5em; width: 60px; text-align: center; text-transform: lowercase; }
        button { font-size: 1.5em; cursor: pointer; background-color: #0db7ed; color: white; border: none; padding: 5px 20px; border-radius: 5px;}
    </style>
</head>
<body>
    <h1>Juego del Ahorcado</h1>
    
    <div class="palabra">{{ estado_palabra }}</div>
    <h2>Intentos restantes: {{ intentos }}</h2>
    
    <div class="mensaje">{{ mensaje }}</div>
    
    {% if juego_terminado %}
        <form action="/reiniciar" method="post">
            <button type="submit">Jugar de nuevo</button>
        </form>
    {% else %}
        <br>
        <form action="/" method="post">
            <input type="text" name="letra" maxlength="1" autofocus required autocomplete="off">
            <button type="submit">Adivinar</button>
        </form>
        <div class="letras">Letras usadas: <strong>{{ letras_usadas | join(', ') }}</strong></div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    # Si es una partida nueva, preparamos las variables
    if 'palabra_secreta' not in session:
        session['palabra_secreta'] = random.choice(PALABRAS)
        session['letras_adivinadas'] = []
        session['intentos'] = 6
        session['mensaje'] = "¡Ingresa tu primera letra!"

    mensaje = session.get('mensaje', '')
    session['mensaje'] = "" 
    
    # Si el usuario envió una letra desde el formulario web
    if request.method == "POST":
        letra = request.form.get('letra', '').lower()
        
        if len(letra) != 1 or not letra.isalpha():
            mensaje = "Ingresa una letra válida."
        elif letra in session['letras_adivinadas']:
            mensaje = "Ya intentaste con esa letra."
        else:
            session['letras_adivinadas'].append(letra)
            session.modified = True
            
            if letra in session['palabra_secreta']:
                mensaje = "¡Correcto!"
            else:
                session['intentos'] -= 1
                mensaje = "Letra incorrecta."

    # Construir la palabra con guiones bajos o letras reveladas
    estado_palabra = ""
    for letra in session['palabra_secreta']:
        if letra in session['letras_adivinadas']:
            estado_palabra += letra + " "
        else:
            estado_palabra += "_ "

    # Revisar si ya ganó o perdió
    juego_terminado = False
    if "_" not in estado_palabra:
        mensaje = "🎉 ¡Felicidades! Eres un experto. 🎉"
        juego_terminado = True
    elif session['intentos'] <= 0:
        mensaje = f"💀 ¡Te ahorcaron! La palabra era: {session['palabra_secreta'].upper()}"
        estado_palabra = " ".join(session['palabra_secreta'])
        juego_terminado = True

    # Enviar toda esta información a nuestro diseño HTML
    return render_template_string(
        HTML_TEMPLATE, 
        estado_palabra=estado_palabra.strip(), 
        intentos=session['intentos'],
        mensaje=mensaje,
        letras_usadas=session['letras_adivinadas'],
        juego_terminado=juego_terminado
    )

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    session.clear() # Borramos la memoria para empezar fresco
    return redirect(url_for('index'))

if __name__ == "__main__":
    # host="0.0.0.0" es CRUCIAL en Docker para que la red funcione hacia afuera
    app.run(host="0.0.0.0", port=5000)
