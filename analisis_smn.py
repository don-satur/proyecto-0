from funciones_smn import leer_observaciones, mostrar_resumen

def main():
    archivo_1 = "datos/observaciones_smn.txt" #archivo_1 son los datos del primer archivo de datos
    archivo_2 = "datos/observaciones2_smn.txt" #archivos_2 son los datos del segundo archivo de datos

    print(" >>> primera seana <<< ")
    datos_s1 = leer_observaciones(archivo_1) #resumen del primer archivo
    mostrar_resumen(datos_s1)

    print()

    print(" >>> segunda semana <<< ")
    datos_s2 = leer_observaciones(archivo_2) #resumen del segundo archivo
    mostrar_resumen(datos_s2)

if __name__ == "__main__":
    main