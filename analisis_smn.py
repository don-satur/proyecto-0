from funciones_smn import leer_observaciones, mostrar_resumen

if __name__ == "__main__":   #uso el if __name__ == "__main__" para que el mismo programa verifique si el archivo se está ejecutando directamente o no
    archivo_1 = "observaciones_smn.txt" #archivo_1 son los datos del primer archivo de datos
    archivo_2 = "observaciones2_smn.txt" #archivos_2 son los datos del segundo archivo de datos

    print(" >>> primera seana <<< ")
    datos_s1 = leer_observaciones(archivo_1) #resumen del primer archivo
    mostrar_resumen(datos_s1)

    print()

    print(" >>> segunda semana <<< ")
    datos_s2 = leer_observaciones(archivo_2) #resumen del segundo archivo
    mostrar_resumen(datos_s2)