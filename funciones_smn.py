from datetime import datetime

def separar_viento(campo_viento: str) -> tuple:
    partes = campo_viento.strip().split() #elimino los espacios innecesarios y divido la lista

    #verifico si hay elementos y si ese primer elemento es "calma"
    if len(partes) > 0 and partes[0].lower() == "calma":
        return ("Calma", 0.0)
    
    direccion = " ".join(partes[:-1])  #junta todo excepto el último elemento como dirección
    velocidad = float(partes[-1])     #la velocidad es el último elemento
    return (direccion, velocidad)

def leer_observaciones(ruta: str) -> dict:
    obervaciones = {}

    with open(ruta,"r", encoding="cp1252") as archivo:

        for linea in archivo:
            campos = linea.strip().split(";") #aisla cada renglón y delimita que un renglón termina cuando hay ";"

            if len(campos) == 10:
                ciudad = campos[0].strip() #obtiene el nombre de la ciudad

                direccion, velocidad = separar_viento(campos[8]) #separo el campo viento en direción y velocidad

                sen_term_texto = campos[6].strip()
                sensacion = None if sen_term_texto == "No se calcula" else float(sen_term_texto) # si dice "no se calcula" le asigna "None"

                humedad_texto = campos[7].strip().replace("%", "").strip()
                humedad_num = float(humedad_texto) if humedad_texto else 0.0

                obervaciones[ciudad] = {
                    "fecha":campos[1].strip(),                          #fecha de la observación
                    "hora":campos[2].strip(),                           #hora de la observación
                    "condicion":campos[3].strip(),                      #estado de tiempo (nublado,soleado,etc)
                    "visibilidad":campos[4].strip(),                    #visibilidad en km
                    "temperatura":float(campos[5].strip()),             #temperatura pasada a decimal
                    "sensacion_termica": sensacion,                     #sensción térmica
                    "humedad": humedad_num,                             #humedad
                    "direccion_viento":direccion,                       #dirección del viento
                    "velocidad_viento": velocidad,                      #velocidad del viento
                    "presion":campos[9].strip().strip("/").strip()      #presión atmosférica
                }
    return obervaciones

def cantidad_ciudades(observaciones: dict) -> int:
    return len(observaciones)

def cantidad_ciudades_completas(observaciones: dict) -> int:
    completas = 0
    for datos_ciudad in observaciones.values(): #recorre los "diccionarios internos"

        if datos_ciudad["sensacion_termica"] is not None: #si la sensación térmica no es None, la ciudad está completa
            completas += 1

    return completas

def top_n_ciudades(observaciones: dict, campo: str, n: int, descendente: bool = True) -> list:
    lista_ordenada = []
    
    for ciudad in observaciones: #recorre cada ciudad
        valor = observaciones[ciudad][campo] #obtiene el campo solicitado de la ciudad ("temperatura", "velocidad_viento", etc)

        if valor is not None: #filtra valores nulos
            lista_ordenada.append((valor, ciudad)) #agrega la tupla (valor, ciudad) a la lista
            
    lista_ordenada.sort(reverse=descendente) # ordena la lista si, si descendiente=True ordena de mayor a menor y viceversa
    
    resultado = []
    for valor, ciudad in lista_ordenada[:n]:
        resultado.append((ciudad, valor)) #invierte la tupla a (ciudad, valor) para tener una estructura más clara
        
    return resultado #devuelve la lista de los primeros N resultados

def mostrar_resumen(observaciones: dict) -> None:
    fechas_ordenables = [] #en esta lista se guardarán la fechas

    meses = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]
    for ciudad in observaciones: #en este for se recorren las ciudades para extraer la fecha de observación
        f = observaciones[ciudad]["fecha"]
        partes = f.replace("/", "-").split("-") #si las fechas tienen "/" las remplaza por "-" para poder dividirlas en dia-mes-año

        if len(partes) == 3: #verifica que l fecha tenga día, mes y año
            dia = int(partes[0].strip())        #convierte el dia en entero
            mes = partes[1].strip().lower()     #obtiene el mes en minúsculas
            anio = int(partes[2].strip())       #convierte el año a entero

            if mes in meses:        #este if obtiene el número del mes ya sea que esté en letras o en número
                num_mes = meses.index(mes) + 1
            else:
                num_mes = int(mes)

            fechaa= datetime(anio, num_mes, dia)
            fechas_ordenables.append((fechaa,f))

    if fechas_ordenables: #este if determina las fechas de inicio y finalización de las mediciones
        fechas_ordenables.sort()
        fecha_inicio = fechas_ordenables[0][1]
        fecha_fin = fechas_ordenables[-1][1]
        periodo_texto = f"periodo de observaciones: desde {fecha_inicio} hasta {fecha_fin}"
    else:
        periodo_texto = "periodo de observaciones: no disponible"

    print("===== RESUMEN DE OBSERVACIONES =====")
    print(periodo_texto)
    print("total de ciudades procesadas: ",cantidad_ciudades(observaciones))
    print("ciudades con datos completos: ", cantidad_ciudades_completas(observaciones))
    print("-" * 40)

    print("top 5 temperaturas más altas: ")
    for ciudad, temp in top_n_ciudades(observaciones, "temperatura",5, descendente=True):
        print(f"  -{ciudad}:  {temp}  °C")

    print("\ntop 5 temperaturas más bajas:")
    for ciudad, temp in top_n_ciudades(observaciones,"temperatura", 5, descendente=False):
        print(f"  -{ciudad}:  {temp}  °C")

    print("\ntop 5 vientos más fuertes:")
    for ciudad, viento in top_n_ciudades(observaciones,"velocidad_viento", 5,descendente=True):
        print(f"  -{ciudad}:  {viento}  km/h")

    print("\ntop 5 mayores humedades registradas:")
    for ciudad, hum in top_n_ciudades(observaciones, "humedad", 5, descendente=True):
        print(f"  -{ciudad}:  {int(hum)}%")

    print("\ntop 5 menores humedades registradas:")
    for ciudad, hum in top_n_ciudades(observaciones, "humedad", 5, descendente=False):
        print(f"  -{ciudad}:  {int(hum)}%")