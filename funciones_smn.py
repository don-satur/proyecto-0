from datetime import datetime

def separar_viento(campo_viento: str) -> tuple:
    partes = campo_viento.strip().split()

    if len(partes) > 0 and partes[0].lower() == "calma":
        return ("Calma", 0.0)
    
    direccion = " ".join(partes[:-1])
    velocidad = float(partes[-1]) 
    return (direccion, velocidad)

def leer_observaciones(ruta: str) -> dict:
    observaciones = {}

    with open(ruta, "r", encoding="cp1252") as archivo:

        for linea in archivo:
            campos = linea.strip().split(";")

            if len(campos) == 10:
                ciudad = campos[0].strip()
                direccion, velocidad = separar_viento(campos[8])

                sen_term_texto = campos[6].strip()
                sensacion = None if sen_term_texto == "No se calcula" else float(sen_term_texto)

                humedad_texto = campos[7].strip().replace("%", "").strip()
                humedad_num = float(humedad_texto) if humedad_texto else 0.0

                fecha_y_hora = parsear_fecha_hora(campos[1], campos[2])

                observaciones[ciudad] = {
                    "fecha_y_hora": fecha_y_hora,
                    "condicion": campos[3].strip(),
                    "visibilidad": campos[4].strip(),
                    "temperatura": float(campos[5].strip()),
                    "sensacion_termica": sensacion,
                    "humedad": humedad_num,
                    "direccion_viento": direccion,
                    "velocidad_viento": velocidad,
                    "presion": campos[9].strip().strip("/").strip()
                }

    return observaciones

def cantidad_ciudades(observaciones: dict) -> int:
    return len(observaciones)



def cantidad_ciudades_completas(observaciones: dict) -> int:
    completas = 0
    for datos_ciudad in observaciones.values():

        if datos_ciudad["sensacion_termica"] is not None:
            completas += 1

    return completas

def top_n_ciudades(observaciones: dict, campo: str, n: int, descendente: bool = True) -> list:
    lista_ordenada = []
    
    for ciudad in observaciones:
        valor = observaciones[ciudad][campo]

        if valor is not None:
            lista_ordenada.append((valor, ciudad))
            
    lista_ordenada.sort(reverse=descendente) 

    resultado = []
    for valor, ciudad in lista_ordenada[:n]:
        resultado.append((ciudad, valor)) 
        
    return resultado


def horarios_reportados(observaciones: dict) -> list:
    horarios = {
        datos["fecha_y_hora"].strftime("%H:%M") 
        for datos in observaciones.values() 
        if datos.get("fecha_y_hora")
    }
    return sorted(list(horarios))


def mostrar_resumen(observaciones: dict) -> None:

    fechas = [datos["fecha_y_hora"] for datos in observaciones.values() if datos.get("fecha_y_hora")]

    if fechas:
        fecha_inicio = min(fechas).strftime("%d/%m/%Y %H:%M")
        fecha_fin = max(fechas).strftime("%d/%m/%Y %H:%M")
        periodo_texto = f"periodo de observaciones: desde {fecha_inicio} hasta {fecha_fin}"
    else:
        periodo_texto = "periodo de observaciones: no disponible"

    print("===== RESUMEN DE OBSERVACIONES =====")
    print(periodo_texto)
    print("total de ciudades procesadas: ", cantidad_ciudades(observaciones))
    print("ciudades con datos completos: ", cantidad_ciudades_completas(observaciones))
    print("horarios reportados: ", ", ".join(horarios_reportados(observaciones)))
    print("-" * 40)

    print("top 5 temperaturas más altas: ")
    for ciudad, temp in top_n_ciudades(observaciones, "temperatura", 5, descendente=True):
        print(f"  -{ciudad}: {temp} °C")

    print("\ntop 5 temperaturas más bajas:")
    for ciudad, temp in top_n_ciudades(observaciones, "temperatura", 5, descendente=False):
        print(f"  -{ciudad}: {temp} °C")

    print("\ntop 5 vientos más fuertes:")
    for ciudad, viento in top_n_ciudades(observaciones, "velocidad_viento", 5, descendente=True):
        print(f"  -{ciudad}: {viento} km/h")

    print("\ntop 5 mayores humedades registradas:")
    for ciudad, hum in top_n_ciudades(observaciones, "humedad", 5, descendente=True):
        print(f"  -{ciudad}: {int(hum)}%")

    print("\ntop 5 menores humedades registradas:")
    for ciudad, hum in top_n_ciudades(observaciones, "humedad", 5, descendente=False):
        print(f"  -{ciudad}: {int(hum)}%")


def parsear_fecha_hora(fecha: str, hora: str) -> datetime:
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]

    partes_fecha = fecha.strip().replace("/", "-").split("-")
    dia = int(partes_fecha[0].strip())

    mes = partes_fecha[1].strip().lower()
    if mes in meses:
        num_mes = meses.index(mes) + 1
    else:
        num_mes = int(mes)

    anio = int(partes_fecha[2].strip())

    partes_hora = hora.strip().split(":")
    h = int(partes_hora[0].strip())
    m = int(partes_hora[1].strip()) if len(partes_hora) > 1 else 0
    return datetime(anio, num_mes, dia, h, m)