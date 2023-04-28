from flask import Flask, render_template
import requests
import numpy as numpy
import os
import matplotlib
import matplotlib.pyplot as plt

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
    ## trabajo generar y salvar grafico
    print('genero grafico')
    plt.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])
    plt.xlabel('Months')
    plt.ylabel('Books Read')
    print('salvo grafico sin mostrar')
    ## plt.show()
    ## plt.savefig('https://fullpublic-production.up.railway.app/figUno.png')
    ## plt.savefig('figUno.png')
    plt.savefig('assets/figUno.png') ## problemas despues de enviar !!!!!!!!!!!!!!!!!!
    
    ## trabajo basico web videos
    # datosObtenidos = requests.get('https://api.dailymotion.com/videos?channel=sport&limit=10')
    # datosFormatoJSON = datosObtenidos.json()
    # print(datosFormatoJSON)
    # print("version unob -----------")

    # # return render_template('index.html',datos=datosFormatoJSON['list'],fname=finame)
    # return render_template('index.html', datos=datosFormatoJSON['list'])
    return render_template('index.html', dato = 22)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
