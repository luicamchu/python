'''
Módulo avistamientos
Adaptación del notebook a proyecto: Toñi Reina
'''
import csv
from datetime import date, datetime
import math
from typing import NamedTuple
from collections import Counter, defaultdict
from coordenadas import Coordenadas, distancia_harvesine, redondear
from parsers import parse_datetime
import statistics
import locale

## Definición de tipos
Avistamiento = NamedTuple('Avistamiento', [
    ('fechahora', datetime),
    ('ciudad', str),
    ('estado', str),
    ('forma', str),
    ('duracion', int),
    ('comentarios', str),
    ('ubicacion', Coordenadas)
])

## 1. Operaciones de carga de datos
### 1.1 Función de lectura de datos
# Función de lectura que crea una lista de avistamientos
def parseFechahora(fecha:str) -> datetime:
    return datetime.strptime(fecha, "%m/%d/%Y %H:%M")

def lee_avistamientos(fichero :str) -> list[Avistamiento]:
    '''
    Lee un fichero de entrada y devuelve una lista de tuplas. 
    Para convertir la cadena con la fecha y la hora al tipo datetime, usar
        datetime.strptime(fecha_hora,'%m/%d/%Y %H:%M')    
    
    @param fichero: ruta del fichero csv que contiene los datos en codificación utf-8 
    @type fichero: str
    @return: lista de tuplas con la información de los avistamientos 
    @rtype: [Avistamiento(datetime, str, str, str, str, int, str, Coordenadas(float, float))]   
    '''
    result:list = []
    with open(fichero, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)
        for cadena_fecha,city,state,shape,duration,comments,latitude,longitude in reader:
            fecha = parseFechahora(cadena_fecha)
            duration = int(duration)
            coordenadas = Coordenadas(float(latitude), float(longitude))
            registro = Avistamiento(fecha, city, state, shape, duration, comments, coordenadas)
            result.append(registro)
    return result
        

### 2.1 Número de avistamientos producidos en una fecha
def numero_avistamientos_fecha(avistamientos: list[Avistamiento], fecha: datetime.date) -> int:
    ''' Avistamientos que se han producido en una fecha
    
    Toma como entrada una lista de avistamientos y una fecha.
    Devuelve el número de avistamientos que se han producido en esa fecha.

    @param avistamientos: lista de avistamientos
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param fecha: fecha del avistamiento 
    @type fecha: datetime.date
    @return:  Número de avistamientos producidos en la fecha 
    @rtype: int
    
    '''
    contador = 0
    if isinstance(fecha, date):
        for a in avistamientos:
            if fecha is None or a.fechahora.date() == fecha:
                contador+=1
    else:
        print("")
    return contador


# Por comprensión
def numero_avistamientos_fecha2(avistamientos: list[Avistamiento], fecha: datetime.date) -> int:
    contador = 0
    if isinstance(fecha, date):
        contador = sum(1 for a in avistamientos if fecha is None or a.fechahora.date() == fecha)
    else:
        print("")
    return contador

### 2.2 Número de formas observadas en un conjunto de estados
def formas_estados(avistamientos: list[Avistamiento], estados: set[str]) -> int:
    ''' 
    Devuelve el número de formas distintas observadas en avistamientos 
    producidos en alguno de los estados especificados.
    @param avistamientos: lista de tuplas con la información de los avistamientos
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float)))]
    @param estados: conjunto de estados para los que se quiere hacer el cálculo 
    @type estados: {str}
    @return: Número de formas distintas observadas en los avistamientos producidos
         en alguno de los estados indicados por el parámetro "estados"
    @rtype: int
    '''
    result = 0
    set_shapes = set()
    if estados:
        for a in avistamientos:
            if a.estado in estados:
                set_shapes.add(a.forma)
    else:
        print()
    return len(set_shapes)

def formas_estados2(avistamientos: list[Avistamiento], estados: set[str]) -> int:
    # Por comprensión
    pass
    
### 2.3 Duración total de los avistamientos en un estado
def duracion_total(avistamientos: list[Avistamiento], estado: str) -> int:
    ''' 
    Devuelve la duración total de los avistamientos de un estado. 
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float)))]
    @param estado: estado para el que se quiere hacer el cálculo
    @type estado: str
    @return: duración total en segundos de todos los avistamientos del estado 
    @rtype: int
    '''
    pass

def duracion_total2(avistamientos: list[Avistamiento], estado: str) -> int:
    ## Por compresión
    duracion = sum(a.duracion for a in avistamientos if a.estado == estado)
    return duracion



### 2.4 Avistamientos cercanos a una ubicación
def avistamientos_cercanos_ubicacion(avistamientos: list[Avistamiento], ubicacion: Coordenadas, radio: float) -> set[Avistamiento]:
    ''' 
    Devuelve el conjunto de avistamientos cercanos a una ubicación.
    @param avistamientos: lista de tuplas con la información de los avistamientos
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float)))]
    @param ubicacion: coordenadas de la ubicación para la cual queremos encontrar avistamientos cercanos 
    @type ubicacion: Coordenadas (float, float)
    @param radio: radio de distancia
    @param radio: float
    @return:Conjunto de avistamientos que se encuentran a una distancia
         inferior al valor "radio" de la ubicación dada por el parámetro "ubicacion" 
    @rtype: {Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))}
    '''
    conjunto_avistamientos = set()
    for a in avistamientos:
        if distancia_harvesine(a.ubicacion, ubicacion) < radio:
            conjunto_avistamientos.add(a)
    return conjunto_avistamientos
    
def avistamientos_cercanos_ubicacion2(avistamientos: list[Avistamiento], ubicacion: Coordenadas, radio: float) -> set[Avistamiento]:
    ## Por compresión
    res = { a for a in avistamientos if distancia_harvesine(a.ubicacion, ubicacion) < radio}
    return res

## Operaciones con máximos y mínimos
### 3.1 Avistamiento de una forma con mayor duración

def avistamiento_mayor_duracion(avistamientos: list[Avistamiento], forma: str) -> Avistamiento:
    '''
    Devuelve el avistamiento de mayor duración de entre todos los
    avistamientos de una forma dada.
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param forma: forma del avistamiento 
    @type forma: str
    @return:  avistamiento más largo de la forma dada
    @rtype: Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))
    '''
    mayor_duracion = None
    lista_av_forma = []
    
    for a in avistamientos:
        if (a.forma == forma):
            lista_av_forma.append(a)
    
    if len(lista_av_forma) > 0:
        mayor_duracion = max(lista_av_forma, key=lambda x:x.duracion)
        
    return mayor_duracion
def avistamiento_mayor_duracion2(avistamientos: list[Avistamiento], forma: str) -> Avistamiento:
    # Por comprension
    res = max((a for a in avistamientos if a.forma == forma), key=lambda x:x.duracion)
    return res

### 3.2 Avistamiento cercano a un punto con mayor duración
def avistamiento_cercano_mayor_duracion(avistamientos: list[Avistamiento], coordenadas: Coordenadas, radio: float = 0.5) -> tuple[int, str]:
    '''
    Devuelve la duración y los comentarios del avistamiento que más 
    tiempo ha durado de aquellos situados en el entorno de las
    coordenadas que se pasan como parámetro de entrada.
    El resultado debe ser una tupla de la forma (duración, comentarios)
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param coordenadas: tupla con latitud y longitud
    @type coordenadas: Coordenadas (float, float)
    @param radio: radio de búsqueda
    @type radio: float
    @return: duración y comentarios del avistamiento más largo en el entorno de las coordenadas comentarios del avistamiento más largo
    @rtype: int, str
    '''
    res = None
    av_cercanos = []
    for a in avistamientos:
        if distancia_harvesine(a.ubicacion, coordenadas) < radio:
            av_cercanos.append(a)
    if len(av_cercanos) > 0:
        res = max(av_cercanos)
    return res


def avistamiento_cercano_mayor_duracion2(avistamientos: list[Avistamiento], coordenadas: Coordenadas, radio: float = 0.5) -> tuple[int, str]:
    # Por comprensión
    pass


### 3.3 Avistamientos producidos entre dos fechas

def avistamientos_fechas(avistamientos: list[Avistamiento], fecha_inicial: date|None =None, fecha_final: date|None =None) -> list[Avistamiento]:
    '''
    Devuelve una lista con los avistamientos que han tenido lugar
    entre fecha_inicial y fecha_final (ambas inclusive). La lista devuelta
    estará ordenada de los avistamientos más recientes a los más antiguos.
    
    Si fecha_inicial es None se devolverán todos los avistamientos
    hasta fecha_final.
    Si fecha_final es None se devolverán todos los avistamientos desde
    fecha_inicial.
    Si ambas fechas son None se devolverá la lista de 
    avistamientos completa. 
    
    Usar el método date() para obtener la fecha de un objeto datetime.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param fecha_inicial: fecha a partir de la cual se devuelven los avistamientos
    @type fecha_inicial:datetime.date
    @param fecha_final: fecha hasta la cual se devuelven los avistamientos
    @type fecha_final: datetime.date
    @return: lista de tuplas con la información de los avistamientos en el rango de fechas
    @rtype: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    '''
    # Solución 1: usando datetime.min/max
    if (fecha_inicial is None):
        fecha_inicial = datetime.min.date()
    if (fecha_final is None):
        fecha_final = datetime.max.date()
        
    lista = [a for a in avistamientos if fecha_inicial <= a.fechahora.date() < fecha_final]
    lista.sort(reverse=True)
    return lista

def avistamientos_fechas2(avistamientos: list[Avistamiento], fecha_inicial: date|None =None, fecha_final: date|None =None) -> list[Avistamiento]:
    # Solución 2: usando una función auxiliar : fecha_en_rango
    pass

def fecha_en_rango(fecha, fecha_inicial=None, fecha_final=None) -> bool:
    '''Función que devuelve True si la fecha está en el rango (fecha_inicial, fecha_final). 
    Si fecha_inicial es None, devuelve True si fecha es inferior a fecha_fin
    Si fecha_final es None, devuelve True si fecha es superior a fecha_inicio

    :param fecha: fecha de la que se quiere hacer la comprobación
    :type fecha: datetime.date
    :param fecha_inicial: fecha inicial del rango, defaults to None
    :type fecha_inicial: datetime.date, optional
    :param fecha_final: fecha final del rango, defaults to None
    :type fecha_final: datetime.date, optional
    :return: True si la fecha está en el rango
    :rtype: bool
    '''
    pass
    
### 3.4 Avistamiento de un año con el comentario más largo
def comentario_mas_largo(avistamientos: list[Avistamiento], anyo: int, palabra: str) -> Avistamiento:
    ''' 
    Devuelve el avistamiento cuyo comentario es el más largo, de entre
    los avistamientos observados en el año dado por el parámetro "anyo"
    y cuyo comentario incluya la palabra recibida en el parámetro "palabra".
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param anyo: año para el que se hará la búsqueda 
    @type anyo: int
    @param palabra: palabra que debe incluir el comentario del avistamiento buscado 
    @type palabra: str
    @return: avistamiento con el comentario más largo
    @rtype: Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))
    '''    
    res = None
    lista = []
    for a in avistamientos:
        if a.fechahora.year == anyo and palabra in a.comentarios:
            lista.append(a)
    if len(lista) > 0:
        res = max(lista, key=lambda x:len(x.comentarios))
    return res
    
def comentario_mas_largo2(avistamientos: list[Avistamiento], anyo: int, palabra: str) -> Avistamiento:
    # Por comprensión
    pass


### 3.5 Media de días entre avistamientos consecutivos
def media_dias_entre_avistamientos(avistamientos: list[Avistamiento], anyo: int | None = None) -> float:
    ''' 
    Devuelve la media de días transcurridos entre dos avistamientos consecutivos.
    Si año es distinto de None, solo se contemplarán los avistamientos del año
    especificado para hacer el cálculo.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param anyo: año para el que se hará la búsqueda 
    @type anyo: int
    @return: media de días transcurridos entre avistamientos. Si no se puede realizar el
    cálculo, devuelve None 
    @rtype:-float
    '''    
    pass

def dias_entre_fechas(fechas: list[datetime.date]) -> list[int]:
    '''Función auxiliar. Con zip

    :param fechas: lista de fechas
    :type fechas: [datetime.date]
    '''
    dias = {}
    for f1, f2 in zip(fechas, fechas[1:]):
        dias_entre_f1_y_f2 = (f2 - f1).days
        dias.append(dias_entre_f1_y_f2)
    return dias

def dias_entre_fechas2(fechas: list[datetime.date]) -> list[int]:
    ## Por compresión y con zip
    pass

def dias_entre_fechas3(fechas: list[datetime.date]) -> list[int]:
    # Con range e índices
    pass

def dias_entre_fechas4(fechas) -> list[int]:
    # Con range y por compresión
    pass

## 4 Operaciones con diccionarios

### 4.1 Avistamientos por fecha
def avistamientos_por_fecha(avistamientos: list[Avistamiento]) -> dict[datetime.date, set[Avistamiento]]:
    ''' 
    Devuelve un diccionario que indexa los avistamientos por fechas
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return diccionario en el que las claves son las fechas de los avistamientos 
         y los valores son conjuntos con los avistamientos observados en esa fecha
    @rtype {datetime.date: {Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))}}
    '''
    # Con dict
    a_por_fecha = {}
    for a in avistamientos:
        f = a.fechahora.date()
        if f in a_por_fecha:
            a_por_fecha[f].add(a)
    return a_por_fecha


def avistamientos_por_fecha2(avistamientos: list[Avistamiento]) -> dict[datetime.date, set[Avistamiento]]:
    # Con defaultdict
    pass


### 4.2 Formas de avistamientos por mes
def formas_por_mes(avistamientos: list[Avistamiento]) -> dict[str, set[str]]:
    ''' 
    Devuelve un diccionario que indexa las distintas formas de avistamientos
    por los nombres de los meses en que se observan.
    Por ejemplo, para el mes "Enero" se asociará un conjunto con todas las
    formas distintas observadas en dicho mes.
    
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: diccionario en el que las claves son los nombres de los meses 
         y los valores son conjuntos con las formas observadas en cada mes
    @rtype {str: {str}}
    '''
    # Establecemos la configuración local de la hora al formato
    # que esté definido en el ordenador del usuario
    locale.setlocale(locale.LC_TIME, '')

    forma_mes = {}
    for a in avistamientos:
        clave = a.fechahora.strftime("%B").capitalize()# B es una mascara
        if clave in forma_mes:
            forma_mes[clave].add(a.forma)
        else:
            forma_mes[clave] = {a.forma}
    return forma_mes

def formas_por_mes2(avistamientos: list[Avistamiento]) -> dict[str, set[str]]:
    # Con defaultdict    
    # Establecemos la configuración local de la hora al formato
    # que esté definido en el ordenador del usuario
    locale.setlocale(locale.LC_TIME, '')

    pass

### 4.3 Número de avistamientos por año
def numero_avistamientos_por_año(avistamientos: list[Avistamiento]) -> dict[int, int]:
    '''
    Devuelve el número de avistamientos observados en cada año.
             
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: diccionario en el que las claves son los años
         y los valores son el número de avistamientos observados en ese año
    @rtype: {int: int}
    '''
    # Con dict
    num_av_por_año = {}
    for a in avistamientos:
        anyo = a.fechahora.year
        if anyo in num_av_por_año:
            num_av_por_año[anyo] += 1
        else: 
            num_av_por_año[anyo] = 0
    return num_av_por_año

def numero_avistamientos_por_año2(avistamientos: list[Avistamiento]) -> dict[int, int]:
    # Con Counter
    return Counter(a.fechahora.year for a in avistamientos)

def numero_avistamientos_por_año3(avistamientos: list[Avistamiento]) -> dict[int, int]:
    # Con defaultdict
    pass

### 4.4 Número de avistamientos por mes del año
def num_avistamientos_por_mes(avistamientos: list[Avistamiento]) -> dict[str, int]:
    '''
    Devuelve el número de avistamientos observados en cada mes del año.
    
    Usar la expresión .date().month para obtener el número del mes de un objeto datetime.
    
    Usar como claves los nombres de los doce meses con la inicial en mayúsculas:

    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return:diccionario en el que las claves son los nombres de los meses y 
         los valores son el número de avistamientos observados en ese mes
    @rtype: {str: int}
    '''
    # Con dict
    # Establecemos la configuración local de la hora al formato
    # que esté definido en el ordenador del usuario
    locale.setlocale(locale.LC_TIME, '')
    res = dict()
    for a in avistamientos:
        clave = a.fechahora.strftime("%B").capitalize()
        if clave in res:
            res[clave] += 1
        else:
            res[clave] = 1
    return res

def num_avistamientos_por_mes2(avistamientos: list[Avistamiento]) -> dict[str, int]:
    # Con Counter
    # Establecemos la configuración local de la hora al formato
    # que esté definido en el ordenador del usuario
    locale.setlocale(locale.LC_TIME, '')

    pass

def num_avistamientos_por_mes3(avistamientos: list[Avistamiento]) -> dict[str, int]:
    # Con defaultdict
    # Establecemos la configuración local de la hora al formato
    # que esté definido en el ordenador del usuario
    locale.setlocale(locale.LC_TIME, '')
    pass

### 4.5 Coordenadas con mayor número de avistamientos

def coordenadas_mas_avistamientos(avistamientos: list[Avistamiento]) -> Coordenadas: 
    '''
    Devuelve las coordenadas enteras que se corresponden con 
    la zona donde más avistamientos se han observado.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]

    @return: Coordenadas (sin decimales) que acumulan más avistamientos
    @rtype: Coordenadas(float, float)
       
    En primer lugar construiremos un diccionario cuyas claves sean las coordenadas 
    enteras obtenidas a partir de las coordenadas de los avistamientos, y
    cuyos valores sean el número de avistamientos observados en esas coordenadas.
    Después obtendremos el máximo de los elementos del diccionario según el valor
    del elemento.
    '''   
    pass

def coordenadas_mas_avistamientos2(avistamientos: list[Avistamiento]) -> Coordenadas: 
    #Alternativa con Counter
    pass

def coordenadas_mas_avistamientos3(avistamientos: list[Avistamiento]) -> Coordenadas: 
    #Con defaultdict e items para el cálculo del max
    pass

### 4.6 Hora del día con mayor número de avistamientos
def hora_mas_avistamientos(avistamientos: list[Avistamiento]) -> int:
    ''' 
    Devuelve la hora del día (de 0 a 23) con mayor número de avistamientos
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: hora del día en la que se producen más avistamientos
    @rtype: int
       
    En primer lugar construiremos un diccionario cuyas claves sean las horas del
    día en las que se han observado avistamientos, y cuyos valores sean el número
    de avistamientos observados en esa hora.
    Después obtendremos el máximo de los elementos del diccionario según el valor
    del elemento.
    '''
    pass

def hora_mas_avistamientos2(avistamientos: list[Avistamiento]) -> int:
    # Alternativa usando Counter
    pass


### 4.7 Longitud media de los comentarios por estado

def longitud_media_comentarios_por_estado(avistamientos: list[Avistamiento]) -> dict[str, float]:
    '''
    Devuelve un diccionario en el que las claves son los estados donde se
    producen los avistamientos y los valores son la longitud media de los
    comentarios de los avistamientos en cada estado.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: diccionario que almacena la longitud media de los comentarios (valores)
         por estado (claves)
    @rtype: {str: float}
            
    En primer lugar creamos un diccionario que agrupe los avistamientos por estado.
    Esto lo hacemos usando una función auxiliar.
    En segundo lugar, creamos un diccionario a partir del primero, en el que se
    calcule la media. Para definir este diccionario usamos una función
    auxiliar que calcule la media de una lista de Avistamientos
    '''
    pass


def agrupa_avistamientos_por_estado(avistamientos: list[Avistamiento]) -> dict[str, list[Avistamiento]]:
    '''Devuelve un diccionari en el que las claves son los estados, 
    y los valores listas de avistamientos de ese estado

    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: Un diccionario con estados y listas de avistamientos de ese estado
    @rtype: {str:[Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]}
    '''
    pass


def longitud_media_comentarios(avistamientos: list[Avistamiento]) -> float:
    '''Dada una lista de avistamientos, devuelve la longitud media de los
    comentarios de esa lista

    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: La longitud media de los comentarios de la lista
    @rtype: float
    '''
    pass

### 4.8 Porcentaje de avistamientos por forma
def porc_avistamientos_por_forma(avistamientos: list[Avistamiento]) -> dict[str, float]:
    '''
    Devuelve un diccionario en el que las claves son las formas de los
    avistamientos, y los valores los porcentajes de avistamientos con cada forma.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return:  diccionario que almacena los porcentajes de avistamientos (valores)
         por forma (claves)
    @rtype: {str: float}
            
    En primer lugar crearemos un diccionario cuyas claves sean las formas
    y cuyos valores sean el número de avistamientos de esa forma.
    Después crearemos un segundo diccionario con las mismas claves y cuyos valores
    resulten de dividir los valores del diccionario anterior por el número
    total de avistamientos, para obtener los porcentajes.
    '''  
    pass


def porc_avistamientos_por_forma2(avistamientos: list[Avistamiento]) -> dict[str, float]:
    # Solución alternativa con Counter
    pass

### 4.9 Avistamientos de mayor duración por estado
def avistamientos_mayor_duracion_por_estado(avistamientos: list[Avistamiento], n: int=3) -> dict[str, list[Avistamiento]]:
    '''
    Devuelve un diccionario que almacena los n avistamientos de mayor duración 
    en cada estado, ordenados de mayor a menor duración.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param n: número de avistamientos a almacenar por cada estado 
    @type n: int
    @return: diccionario en el que las claves son los estados y los valores son listas 
         con los "n" avistamientos de mayor duración de cada estado,
         ordenados de mayor a menor duración
            -> {str: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]}
            
    En primer lugar crearemos un diccionario de agrupación cuyas claves sean los estados
    y cuyos valores sean listas con los avistamientos observados en ese estado.
    Para ello usamos la función auxiliar que definimos en el apartado 4.7.
    Después crearemos un segundo diccionario cuyas claves sean los estados
    y cuyos valores sean las mismas listas, pero en orden de mayor a menor
    duración y recortadas a "limite" elementos.
    '''
    pass

def avistamientos_mayor_duracion_por_estado2(avistamientos: list[Avistamiento], n: int=3) -> dict[str, list[Avistamiento]]:
    # Usando una definición por compresión
    pass


### 4.10 Año con más avistamientos de una forma
def año_mas_avistamientos_forma(avistamientos: list[Avistamiento], forma: str) -> int:
    '''
    Devuelve el año en el que se han observado más avistamientos
    de una forma dada.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param forma: forma del avistamiento 
    @type: str
    @return: año con mayor número de avistamientos de la forma dada
    @rtype: int
            
    
    En primer lugar se crea un diccionario con filtro cuyas claves sean los años
    y cuyos valores sean el número de avistamientos observados en ese año,
    utilizando la función ya definida numero_avistamientos_por_año.
    Luego, se calcula el máximo del diccionario según los valores.
    '''
    pass

def año_mas_avistamientos_forma2(avistamientos: list[Avistamiento], forma: str) -> int:
    # con Counter
    pass

### 4.11 Estados con mayor número de avistamientos
def estados_mas_avistamientos(avistamientos: list[Avistamiento], n: int=5) -> list[tuple[str, int]]:
    '''
    Devuelve una lista con los estados en los que se han observado
    más avistamientos, junto con el número de avistamientos,
    ordenados de mayor a menor número de avistamientos.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param n: número de estados a devolver 
    @type n: int  
    @return: lista con los estados donde se han observado más avistamientos,
         junto con el número de avistamientos, en orden decreciente
         del número de avistamientos y con un máximo de "limite" estados.
    @rtype: [(str, int)]
            
    En primer lugar crearemos un diccionario cuyas claves sean los estados
    y cuyos valores sean el número de avistamientos observados en ese estado.
    Después crearemos una lista con las claves del diccionario, ordenadas según
    sus respectivos valores en orden decreciente. Finalmente, recortaremos
    esta lista a "limite" elementos.
    '''
    pass

def estados_mas_avistamientos2(avistamientos: list[Avistamiento], n: int=5) -> list[tuple[str, int]]:
    #Con most commons
    numero_avistamientos_estado = Counter (a.estado for a in avistamientos)
    estados = numero_avistamientos_estado.most_common(n)
    return estados
      
### 4.12 Duración total de los avistamientos de cada año en un estado dado
def duracion_total_avistamientos_año(avistamientos: list[Avistamiento], estado: str) -> dict[int, int]:
    '''
    Devuelve un diccionario que almacena la duración total de los avistamientos 
    en cada año, para un estado dado.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param estado: nombre del estado
    @type estado: str
    @return: diccionario en el que las claves son los años y los valores son números 
         con la suma de las duraciones de los avistamientos observados ese año
         en el estado dado
    @rtype: {int: int}

    Se crea un diccionario con filtro cuyas claves sean los años
    y cuyos valores sean la suma de las duraciones de todos los avistamientos
    observados en ese año.
    '''
    pass


def duracion_total_avistamientos_año2(avistamientos: list[Avistamiento], estado: str) -> dict[int, int]:
    #Con defaultdict
    pass

### 4.13 Fecha del avistamiento más reciente de cada estado
def avistamiento_mas_reciente_por_estado(avistamientos: list[Avistamiento]) -> dict[str, datetime]:
    '''
    Devuelve un diccionario que almacena la fecha del último avistamiento
    observado en cada estado.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return:  diccionario en el que las claves son los estados y los valores son 
         las fechas del último avistamientos observado en ese estado.
    @rtype: {str: datetime.datetime}
            
    En primer lugar crearemos un diccionario cuyas claves sean los estados
    y cuyos valores sean listas con los avistamientos observados en ese estado.
    Para ello usamos la función auxiliar  definida en el apartado 4.7
    Después crearemos un segundo diccionario cuyas claves sean los estados y
    cuyos valores sean los valores máximos de las listas, según el campo fechahora.
    '''
    pass