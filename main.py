from flask import Flask, render_template, request
import requests
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

from jubilib import *

 

## matplotlib.use('Agg')    parte de solucion en stackoverflow
## a busqueda flask RuntimeError: main thread is not in main loop

## seleccion del host y port para
## Railway o local
# portname='PORT'
# if portname in os.environ:
#     portvalue=os.environ[portname]
#     hostvalue='0.0.0.0'
#     print(portname,' value is', portvalue,' ,  host is ',hostvalue)
# else:
#     portvalue=8000
#     hostvalue='127.0.0.1'
#     print(portname, 'does not exist using ', hostvalue, portvalue)

# exte='.png'
# prt=':'+str(portvalue)
# place='http://'+hostvalue+prt
# finame=place+'/'+'fig1'+exte
# print('archivo = ',finame)

app = Flask(__name__, static_folder='assets', static_url_path='/assets')


@app.route('/', methods=['POST','GET'])
def index():
     
    if request.method == 'GET':
        ## es la primera vez, calcula con argumentos default
                dato = jubiploter() 
        return render_template('index.html', indexarg=dato)

    if request.method == 'POST':
        if(request.form['aporte'] == '' or request.form['interes'] == '' or request.form['aumento'] == ''or request.form['periodo'] == ''):
            ## submit sin entrar datos
            return "<html><body> <h1>Invalid number</h1></body></html>" ## trae problemas mejorar
        else:
            aint=int(request.form['aporte'])
            bint=int(request.form['interes'])
            cint=int(request.form['aumento'])
            dint=int(request.form['periodo'])
            print(aint,bint,cint,dint)
            ## trabajo generar y salvar grafico
            dato=jubiploter(aint,bint,cint,dint)    
            
            
            return render_template('index.html', indexarg=dato )
    

@app.route('/about', methods=['POST','GET'])
def about():  
    
    return render_template('about.html', aboutarg='this and me')        

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
    
