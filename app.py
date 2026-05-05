#FLASK: Se encarga de recibir las visitas, procesar los datos y enviarlos al navegador usando templates.
from flask import Flask, render_template
# Importamos la función que creamos en el otro archivo
from data.analisis import analisis_finales

app = Flask(__name__)

@app.route('/')
def home():
    resultados = analisis_finales()  
    return render_template('principal.html', data=resultados) 

@app.route('/siglo20')
def pagina_siglo20():
    resultados = analisis_finales()
    return render_template('siglo20.html', data=resultados['siglo20'])

@app.route('/siglo21')
def pagina_siglo21():
    resultados = analisis_finales()
    return render_template('siglo21.html', data=resultados['siglo21'])

@app.route('/comparativa')
def pagina_comparativa():
    resultados = analisis_finales()
    return render_template('comparativa.html', data=resultados)

if __name__ == '__main__':
    app.run(debug=True)