# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:03:34 2015

@author: Kevin
"""
import random
from matplotlib.pyplot import plot,show,scatter

#un individuo es una pareja (x1,x2) definida de dicha forma
#nuestro fitness seran las funciones


largo = 6 #La longitud del material genetico de cada individuo
num = 10 #La cantidad de individuos que habra en la poblacion
percentage = 0.5 #Cuantos individuos se seleccionan para reproduccion
mutation_chance = 0.2 #La probabilidad de que un individuo mute

def fitness(individuo):
    x1 = individuo[0]
    x2 = individuo[1]
    #suponemos que todos los individuos son parejas
    func = 15*x1+30*x2+4*x1*x2-2*x1**2-4*x2**2
    return func
    
    
def constraint(individuo):
    x1 = individuo[0]
    x2 = individuo[1]
    #suponemos que todos los individuos son parejas
    val = x1 +2*x2 <= 30
    val = val and x1>=0 and x2>=0
    return val
    
    
#def fitness(individuo):
#    x1 = individuo[0]
#    x2 = individuo[1]
#    #suponemos que todos los individuos son parejas
#    func = 3*x1+5*x2
#    return func
#    
#    
#def constraint(individuo):
#    x1 = individuo[0]
#    x2 = individuo[1]
#    #suponemos que todos los individuos son parejas
#    val = x1 <= 4
#    val = val and 2*x2<= 12
#    val = val and 3*x1+2*x2<=18
#    val = val and x1>=0 and x2>=0
#    return val
    

#def fitness(individuo):
#    x1 = individuo[0]
#    x2 = individuo[1]
#    #suponemos que todos los individuos son parejas
#    func = 5*x1-x1**2+8*x2-2*x2**2
#    return func
#    
#    
#def constraint(individuo):
#    x1 = individuo[0]
#    x2 = individuo[1]
#    #suponemos que todos los individuos son parejas
#    val = 3*x1+2*x2<=6
#    val = val and x1>=0 and x2>=0
#    return val


def bitfield(n):
    #bits escritos de derecha a izquierda
    #   <-------------------------------.
    return [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part 
    
def toInt(n):
    #n escrito de derecha a izquierda
    # <----------------------.
    val = 0
    for i in range(len(n)):
        val += n[i]*2**(len(n)-1-i)
    return val


 
def individual(minimo, maximo):
    """
        Crea un individual
    """
    individuo = [random.randint(minimo,maximo),random.randint(minimo,maximo)]#crear un nuevo individuo
    while (not constraint(individuo)):#mientras no se cumplan las condiciones
        individuo = [random.randint(minimo,maximo),random.randint(minimo,maximo)]
        #creamos un nuevo individuo
    return individuo
 
def crearPoblacion():
    """
        Crea una poblacion nueva de individuos
    """
    return [individual(0,20) for i in range(num)]
 
def calcularFitness(individuo):
    """
        Calcula el fitness de un individuo concreto.
    """
    return fitness(individuo)
    
    
def rectificar(array):
        
    if len(array)<largo:
        narray = [0 for i in range(largo)]
        for i in range(len(array)):
            narray[largo-len(array)+i] = array[i]
        return narray
    
    if len(array)>largo:
        return array[len(array)-largo:len(array)]
    
    return array
   
def reproduction(xind):
    padre = xind[0]
    madre = xind[1]

    condicion = False
    nindividuo = []
    while not condicion:    
    
        individuo = [[0 for i in range(largo)],[0 for i in range(largo)]]#vector lleno de 0
        punto1 = random.randint(1,largo-1) #Se elige un punto para hacer el intercambio x1
        punto2 = random.randint(1,largo-1)#se elige un punto para hacer el intercambio x2
        
        padrex1 = rectificar(bitfield(padre[0]))#x1 del padre
        padrex2 = rectificar(bitfield(padre[1]))#x2 del padre
        
        madrex1 = rectificar(bitfield(madre[0]))#x1 del padre
        madrex2 = rectificar(bitfield(madre[1]))#x2 del padre
        
        #mezcla 1
        individuo[0][:punto1] = padrex1[:punto1]
        individuo[0][punto1:] = madrex1[punto1:]
        
        #mezcla 2
        individuo[1][:punto2] = padrex2[:punto2]
        individuo[1][punto2:] = madrex2[punto2:]
        
        
        
        nindividuo = [toInt(individuo[0]),toInt(individuo[1])]
        
        condicion = constraint(nindividuo)
    
    
    
    return nindividuo
 
def selection_and_reproduction(population):
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
 
        Por ultimo muta a los individuos.
 
    """
    puntuados = [ (calcularFitness(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    puntuados = [i[1] for i in sorted(puntuados)] #Ordena los pares ordenados y se queda solo con el array de valores
    population = puntuados
    
    pressure = int(largo*percentage)#numero de individuos a crusar
    if pressure <= 2:
        pressure = 3
    
 
    selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
 
 
 
    #Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population)-pressure):
        padre = random.sample(selected, 2) #Se eligen dos padres
         
        population[i] = reproduction(padre)#se crea un nuevo individuo
 
    return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven
 



    
 
def mutation(population):
    """
        Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria 
        alcanzarse la solucion.
    """
    
    pressure = int(largo*percentage)#numero de individuos a crusar
    if pressure <= 2:
        pressure = 3
        
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance: #Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
        
            condicion = False
            individuo = []
            while not condicion:
                punto1 = random.randint(1,largo-1) #Se elgie un punto al azar
                punto2 = random.randint(1,largo-1) #se elige un punto al azar
                
                individuo = population[i]
                indix1 = rectificar(bitfield(individuo[0]))#array de bits
                indix2 = rectificar(bitfield(individuo[1]))#array de bits
                
                indix1[punto1] = 1-indix1[punto1]
                indix2[punto2] = 1-indix2[punto2]
                individuo = [toInt(indix1),toInt(indix2)]
                
                condicion = constraint(individuo)
 
 
            #Se aplica la mutacion
            population[i] = individuo
 
    return population
    
def dispersion(poblacion,color):
    x = []
    y = []
    for i in poblacion:
        x.append(i[0])
        y.append(i[1])
        
    scatter(x,y,s=50,color=color)
    show()
 
 
population = crearPoblacion()#Inicializar una poblacion
print "Poblacion Inicial:"
for i in population:#Se muestra la poblacion inicial
    print "\t"+str(i)+" fitness: "+str(fitness(i))
 

#Se evoluciona la poblacion
iteraciones = 100
n = 0
condition = False
for i in range(iteraciones):
    
    population = selection_and_reproduction(population)
    population = mutation(population)
    color = ""+str(1-1.0/iteraciones*(n+1))
    if n%10 == 0 and condition:
        dispersion(population,color)
    n += 1
 

print "\nPoblacion Final:"
for i in population:#Se muestra la poblacion inicial
    print "\t"+str(i)+" fitness: "+str(fitness(i))
 
