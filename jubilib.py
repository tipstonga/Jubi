import sys
import openpyxl  
import numpy as np
import pandas as pd
import datetime
import random

import matplotlib
from matplotlib import pyplot as plt 

## vector de tonos de azul
bb=[(0,0,1,.3),(0,0,1,.5),(0,0,1,.7),(0,0,1,.9)]  #r g b alpha
## vector de tonos de cyan
cc=[(0,1,1,.3),(0,1,1,.5),(0,1,1,.7),(0,1,1,.9)]  #r g b alpha
## vector de tonos de green
gg=[(0,.4,0,.3),(0,.4,0,.5),(0,.4,0,.7),(0,.4,0,.9)]  #r g b alpha
## vector de tonos de rojo
rr=[(1,0,0,.3),(1,0,0,.5),(1,0,0,.7),(1,0,0,.9)]  #r g b alpha
## vector de tonos de magenta
mm=[(1,0,1,.3),(1,0,1,.5),(1,0,1,.7),(1,0,1,.9)]  #r g b alpha

## 

##------------------------------------
## Clase portadora de los valores clave
## elimina declarar global y compacta procesos
class Hu :
    h=[0.70, 0.82, 1.00, 999999.0] ## %s interesantes con infinito
    hn=[0, 0, 0]    ## n meses en que retorno pasa % interesante del salario
    hs=[0, 0, 0]    ## haber correspondiente al retorno 
    hi=0            ## indice del % interesante y correspondiente n y s
    totex=''        ## acumulaa la impresión de resultados
    
    def toteclear(self) :
        self.totex=''
        
    def reinit(self) :
        self.hn=[0, 0, 0]   
        self.hs=[0, 0, 0]  
        self.hi=0
        
    def hdehi(self) :
        return self.h[self.hi]

    def update(self,ene,sal,hbeta, capcorte) :
        self.hn[self.hi]=ene
        self.hs[self.hi]=self.h[self.hi]*sal
        self.totex = self.totex +self.cototex(self,ene,sal,hbeta,capcorte)+'\n '
##      paso a buscar nivel de haberes siguiente
        self.hi += 1
        
    def cototex(self,ene,sal,hbeta,capcorte) :
        meses= ' '+str(ene%12)
        coto = 'con % aporte ' +  str(int(hbeta*100)).center(3) 
        coto = coto +' en '+str(int(ene/12))+'a y '+meses[-2:]+'m'
        coto = coto +(' haber '+ str(round(self.h[self.hi]*sal,2)).ljust(5,'0')[0:4]).center(15)

        coto = coto +': '+(str(int(self.h[self.hi]*100)).rjust(10))[-4:]+' % '
        coto = coto +' del salario '+str(round(sal,2))
        coto = coto +' ,  capital acumulado '+ str(round(capcorte,2)) 
        return coto  
        
## fin de la clase Hu
##------------------------        
        
## Info : aumento en 30 años por categorid ded.excl. 1.79
##      por antiguedad en 25 años 2.2 , total 3.93         
"""  
Calculo de la evolucion del capital y del salario
Evaluacion de retornos mensuales

"""
def calcaum(beta,interesmensual,salario,pctaum=0,intervaum=0) :

    capvec=[0]
    captime=[0]
    cap=0
    erre=1+interesmensual

    Hu.reinit(Hu)
    
    for n in range(1,361) :
        ## evolucion del ahorro
        apmes= salario*beta
        capvec.append((capvec[n-1])*(erre)+apmes)
        captime.append(n/12)
        cap=capvec[n]

        ## aumento del salario 
        if n%intervaum == 0    :
            salario=salario*(1+pctaum)
            
        ## control de renta
        if cap*interesmensual >= salario*Hu.hdehi(Hu)  :
            Hu.update(Hu,n,salario,beta,cap)
            
    return captime,capvec,salario
##-----------------------------

def dibniveles(tx,vecy,cocc) :    

    if Hu.hi >0 :
        nivel_70=vecy[Hu.hn[0]]
        tx.axhline(nivel_70, label= "jubi 70%",
                        color =gg[cocc],linestyle = 'dotted')
    if Hu.hi >1 :
        nivel_82=vecy[Hu.hn[1]]
        tx.axhline(nivel_82, label= "jubi 82%",
                    color =mm[cocc],linestyle = 'dotted')
    if Hu.hi >2 :
        nivel_100 =vecy[Hu.hn[2]]
        tx.axhline(nivel_100, label= "jubi 100%",
                    color =rr[cocc],linestyle = 'dashed')
    
    return tx
##-----------------------------
"""
 jubilacion y aportes

"""
def jubiploter(indato=20 ,intanual=6,pctaum=0, intervaum=60):

    interesmensual=-1+(1+intanual/100)**(1/12)
    #print ("interes anual",intanual, "int mes", interesmensual) 

    Sal=1
   
    ## recorrido del porcentaje de aporte mensual 
    ncurvas = 4
    split = 2
    arango= range(indato,indato-1+ncurvas*split,split)
    lastarango=arango[-1]

    ##    
    Hu.toteclear(Hu)
    ##
    fig,ax= plt.subplots()
    
    for pct in   arango :
        icc=arango.index(pct)
        beta = 1.0*pct/100
        salario=Sal
        
        cx,cy , newsal = calcaum(beta,interesmensual,salario,pctaum,intervaum)
               
        ax.plot(cx,cy,color =bb[icc],label="% aporte" + str(pct))

        ax=dibniveles(ax,cy,icc)
        
    plt.legend()
    plt.grid()
    plt.xlabel("años de aportes")
    plt.ylabel("capital acumulado [ salario inicial = 1 ]")
    plt.title("Jubilación: Años,Aportes,Haberes")
    
    #print('salvo grafico sin mostrar')

    plt.savefig('assets/figUno.png')  

    plt.close() ## solucion al problema RuntimeError: main thread is not in main loop 
    
    if len(Hu.totex) >0 :
        testu=Hu.totex
    else :
        testu='El haber máximo obtenible no alcanza el porcentaje buscado'
        
    """ print("aporte= ",round(newsal*beta,3),
          "salario final= ",round(newsal,3),
          "renta final= ",round(cy[360]*interesmensual,3)
          ) """
      


    return [ indato, intanual, int(pctaum*100), intervaum,
     testu,round(newsal*beta,3),round(newsal,3),
     round(cy[360]*interesmensual,3)]
##-----------------------------

if __name__ == "__main__":
    jubiploter()
    
