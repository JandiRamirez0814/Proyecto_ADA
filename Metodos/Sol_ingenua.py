#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog


def seleccionar_archivos():
    ruta_archivos = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivos:
        datos = leer_datos_desde_archivo(ruta_archivos)
        if datos:
            num_equipos, min_partidos, max_partidos, distancias = datos
            calendario = generar_calendario(num_equipos, min_partidos, max_partidos, distancias)

            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Número de equipos: {num_equipos}\n")
            output_text.insert(tk.END, f"Mínimo de partidos: {min_partidos}\n")
            output_text.insert(tk.END, f"Máximo de partidos: {max_partidos}\n")
            output_text.insert(tk.END, "Calendario generado:\n")

            for fecha, partidos in enumerate(calendario, start=1):
                output_text.insert(tk.END, f"Fecha {fecha}: {' '.join(map(str, partidos))}\n")
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Error al generar el calendario.")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No se seleccionó ningún archivo.")


def leer_datos_desde_archivo(ruta):
    try:
        with open(ruta, 'r') as archivo:
            lineas = archivo.readlines()
            num_equipos = int(lineas[0].strip())
            min_partidos = int(lineas[1].strip())
            max_partidos = int(lineas[2].strip())
            distancias = [list(map(int, linea.strip().split())) for linea in lineas[3:]]
            return num_equipos, min_partidos, max_partidos, distancias
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None


def generar_calendario(num_equipos, min_partidos, max_partidos, distancias):
    calendario = [[0] * num_equipos for _ in range(2 * (num_equipos - 1))]
    partidos_jugados = [[False] * num_equipos for _ in range(num_equipos)]

    fecha = 0
    while fecha < 2 * (num_equipos - 1):
        equipos_restantes = list(range(1, num_equipos + 1))

        for equipo_local in range(1, num_equipos + 1):
            if calendario[fecha][equipo_local - 1] == 0:
                partidos_positivos = 1

                for _ in range(partidos_positivos):
                    equipos_contrincantes = [equipo for equipo in equipos_restantes if
                                             equipo != equipo_local and not partidos_jugados[equipo_local - 1][
                                                 equipo - 1]]

                    if equipos_contrincantes:
                        equipo_contrincante = min(equipos_contrincantes,
                                                  key=lambda e: distancias[equipo_local - 1][e - 1])

                        calendario[fecha][equipo_local - 1] = equipo_contrincante
                        calendario[fecha][equipo_contrincante - 1] = -equipo_local

                        partidos_jugados[equipo_local - 1][equipo_contrincante - 1] = True
                        partidos_jugados[equipo_contrincante - 1][equipo_local - 1] = True

                        if equipo_local in equipos_restantes:
                            equipos_restantes.remove(equipo_local)
                        if equipo_contrincante in equipos_restantes:
                            equipos_restantes.remove(equipo_contrincante)
                    else:
                        break

        while equipos_restantes:
            equipo_local = equipos_restantes.pop(0)
            equipo_contrincante = equipos_restantes.pop(0)

            calendario[fecha][equipo_local - 1] = equipo_contrincante
            calendario[fecha][equipo_contrincante - 1] = -equipo_local

            partidos_jugados[equipo_local - 1][equipo_contrincante - 1] = True
            partidos_jugados[equipo_contrincante - 1][equipo_local - 1] = True

        fecha += 1

    for fecha in range(num_equipos - 1, 2 * (num_equipos - 1)):
        for equipo in range(num_equipos):
            calendario[fecha][equipo] = -calendario[fecha - (num_equipos - 1)][equipo]

    return calendario


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generador y Verificador de Calendario")

    button = tk.Button(root, text="Cargar Archivo", command=seleccionar_archivos)
    button.pack(pady=20)

    output_text = tk.Text(root, height=20, width=50)
    output_text.pack(pady=20)

    root.mainloop()
