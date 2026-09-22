from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola desde Vercel con Flask!"

@app.route('/about')
def about():
    return "Página Sobre Nosotros"
