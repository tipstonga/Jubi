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

##
hab=[0.70, 0.82, 1.00, 999999.0] # porcentajes y trick pct_ret 
nhab=[0, 0, 0]  # mes en que se supera el porcentaje mes_ret 
shab=[0, 0, 0]  # haberes del porcentaje sal_ret 
ihab=0          # indice del porcentaje  ipct_ret   
## 

## Calculo de la evolucion del capital y del salario
## Evaluacion de retornos mensuales

def calcaum(beta,interesmensual,salario,pctaum=0,intervaum=0) :

    capvec=[0]
    captime=[0]
    cap=0
    erre=1+interesmensual
    tasaaum=1+pctaum/100

    global hab,nhab,shab,ihab
##    global ihab
##
    hab=[0.70, 0.82, 1.00, 999999.0] # porcentajes y trick pct_ret 
    nhab=[0, 0, 0]  # mes en que se supera el porcentaje mes_ret 
    shab=[0, 0, 0]  # haberes del porcentaje sal_ret 
    ihab=0          # indice del porcentaje  ipct_ret   
## 

    
    for n in range(1,361) :
        apmes= salario*beta
        capvec.append((capvec[n-1])*(erre)+apmes)
        captime.append(n/12)
        cap=capvec[n]
         
        if n%intervaum == 0    :
            salario=salario*tasaaum

        if cap*interesmensual >= hab[ihab]*salario  :
            nhab[ihab]=n
            shab[ihab]=hab[ihab]*salario
##          paso a buscar nivel siguiente
            ihab += 1
 
 
    return captime,capvec,salario
##-----------------------------
def dibniveles(tx,crit,vecy,cocc,lastarg) :
    if crit<1e-6 :
        if lastarg : 
            tx.axhline(140, label= "jubi 70%",color = 'g',linestyle = 'dotted')        
            tx.axhline(164, label= "jubi 82%",color = 'c',linestyle = 'dotted')
            tx.axhline(200,label= "jubi 100%",color = 'r',linestyle = 'dashed')
        return tx 

    if ihab>0 :
            nivel_70=vecy[nhab[0]]
            tx.axhline(nivel_70, label= "jubi 70%",
                        color =cc[cocc],linestyle = 'dotted')
    if ihab>1 :
        nivel_82=vecy[nhab[1]]
        tx.axhline(nivel_82, label= "jubi 82%",
                    color =gg[cocc],linestyle = 'dotted')
    if ihab>2 :
        nivel_100 =vecy[nhab[2]]
        tx.axhline(nivel_100, label= "jubi 100%",
                    color =rr[cocc],linestyle = 'dashed')
    
    return tx 
"""
 jubilacion y aportes

"""
def jubiploter(pctini=20 ,intanual=6,pctaum=0, intervaum=60):

    interesmensual=-1+(1+intanual/100)**(1/12)
    print ("interes anual",intanual, "int mes", interesmensual) 

    Sal=1

    icc=0  ## indice de los tonos de colores para secuenciarlos
   
    ## recorrido del porcentaje de aporte mensual 
    ncurvas = 4
    split = 2
    arango= range(pctini,pctini-1+ncurvas*split,split)
    lastarango=arango[-1]

    ##    
    
    fig,ax= plt.subplots()
    icc=0
    for pct in   arango :
        beta = 1.0*pct/100
        salario=Sal
        cx,cy , newsal = calcaum(beta,interesmensual,salario,pctaum,intervaum)
               
        ax.plot(cx,cy,color =bb[icc],label="% aporte" + str(pct))

        ax=dibniveles(ax,pctaum,cy,icc,pct==lastarango)

        icc += 1

        
    plt.legend()
    plt.grid()
    plt.xlabel("años de aportes")
    plt.ylabel("capital acumulado [ salario inicial = 1 ]")
    plt.title("Jubilación: Años,Aportes,Haberes")

    print('salvo grafico sin mostrar')

    plt.savefig('assets/figUno.png')  

    plt.close() ## solucion al problema RuntimeError: main thread is not in main loop 
    

    
    print("aporte",newsal*beta," y salario",newsal, "final")

    return [ pctini, intanual, pctaum, intervaum, round(newsal*0.82,2), round(newsal,2)]

if __name__ == "__main__":
    jubiploter()
    
