#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Jandi Ramirez, Paula Lemus, Camilo Viedma
# Creation date: 2023-12-01
# Edition date: 2023-12-18

# Description: Generador de calendario de partidos de fútbol optimizado

import tkinter as tk
from tkinter import filedialog

def elegir_archivo():
    """
    Permite al usuario seleccionar un archivo y genera un calendario a partir de los datos del archivo.
    
    :param ruta: La ruta del archivo.
    :type ruta: str
    :return: El calendario generado.
    :rtype: list
    """
    ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo:
        datos = leer_datos_desde_archivo(ruta_archivo)
        """ 
        :param datos: Los datos leídos del archivo.
        :type datos: tuple
        """
        if datos:
            n_equipos, min_partidos, max_partidos, distancias = datos
            calendario = generar_calendario(n_equipos, min_partidos, max_partidos, distancias)
            
            # Limpiar el área de texto y mostrar el calendario
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Número de equipos: {n_equipos}\n")
            output_text.insert(tk.END, f"Mínimo de partidos: {min_partidos}\n")
            output_text.insert(tk.END, f"Máximo de partidos: {max_partidos}\n")
            output_text.insert(tk.END, "Calendario generado:\n")
            """ 
            :param calendario: El calendario generado.
            :type calendario: list
            """
            for fecha, partidos in enumerate(calendario, start=1):
                """ 
                :param fecha: La fecha.
                :type fecha: int
                :param partidos: Los partidos de la fecha.
                :type partidos: list
                """
                output_text.insert(tk.END, f"Fecha {fecha}: {' '.join(map(str, partidos))}\n")
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Error al generar el calendario.")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No se seleccionó ningún archivo.")


def leer_datos_desde_archivo(ruta):
    """
    Lee los datos de un archivo.

    :param ruta: La ruta del archivo.
    :type ruta: str
    :return: Los datos leídos del archivo.
    :rtype: tuple
    """
    try:
        with open(ruta, 'r') as archivo:
            """ 
            :param archivo: El archivo.
            :type archivo: file
            :return: Los datos leídos del archivo.
            :rtype: tuple
            """
            lineas = archivo.readlines()
            
            # Leer el número de equipos y los límites de partidos
            n_equipos = int(lineas[0].strip())
            min_partidos = int(lineas[1].strip())
            max_partidos = int(lineas[2].strip())
            
            """ 
            :param n_equipos: El número de equipos en el torneo.
            :type n_equipos: int
            :param min_partidos: El número mínimo de partidos que un equipo debe jugar.
            :type min_partidos: int
            :param max_partidos: El número máximo de partidos que un equipo puede jugar.
            :type max_partidos: int
            """

            # Leer la matriz de distancias
            distancias = [list(map(int, linea.strip().split())) for linea in lineas[3:]]
            """ 
            :param distancias: Una matriz de distancias entre los equipos.
            :type distancias: list
            """

            return n_equipos, min_partidos, max_partidos, distancias
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def generar_calendario_desde_archivo(ruta):
    """
    Genera un calendario a partir de los datos de un archivo.

    :param ruta: La ruta del archivo.
    :type ruta: str
    :return: El calendario generado.
    :rtype: list
    """
    datos = leer_datos_desde_archivo(ruta)
    """ 
    :param datos: Los datos leídos del archivo.
    :type datos: tuple
    """
    if datos:
        n_equipos, min_partidos, max_partidos, distancias = datos
        calendario = generar_calendario(n_equipos, min_partidos, max_partidos, distancias)
        """ 
        :param calendario: El calendario generado.
        :type calendario: list
        """
        return calendario
    else:
        return None



def generar_calendario(n_equipos, min_partidos, max_partidos, distancias):
    """
    Genera un calendario para un torneo de equipos.

    :param n_equipos: El número de equipos en el torneo.
    :type n_equipos: int
    :param min_partidos: El número mínimo de partidos que un equipo debe jugar.
    :type min_partidos: int
    :param max_partidos: El número máximo de partidos que un equipo puede jugar.
    :type max_partidos: int
    :param distancias: Una matriz de distancias entre los equipos.
    :type distancias: list
    :return: El calendario del torneo.
    :rtype: list
    """
    if n_equipos % 2 != 0:
        n_equipos += 1  # Asegurarse de que el número de equipos sea par

    calendario = [[0] * n_equipos for _ in range(2 * (n_equipos - 1))]
    partidos_jugados = [[False] * n_equipos for _ in range(n_equipos)]

    """
    :param calendario: El calendario del torneo.
    :type calendario: list
    :param partidos_jugados: Una matriz que indica si un equipo ha jugado contra otro.
    :type partidos_jugados: list
    """
    for fecha in range(n_equipos - 1):
        equipos_restantes = list(range(1, n_equipos + 1))
        """
        :param equipos_restantes: Una lista de equipos que aún no han sido emparejados.
        :type equipos_restantes: list
        """

        for equipo_local in range(1, n_equipos + 1):
            """
            :param equipo_local: El equipo local.
            :type equipo_local: int
            """
            if calendario[fecha][equipo_local - 1] == 0:
                partidos_positivos = 1
                """
                :param partidos_positivos: El número de partidos positivos que un equipo debe jugar.
                :type partidos_positivos: int
                """
                for _ in range(partidos_positivos):
                    equipos_contrincantes = [equipo for equipo in equipos_restantes if equipo != equipo_local and not partidos_jugados[equipo_local - 1][equipo - 1]]
                    """
                    :param equipos_contrincantes: Una lista de equipos que aún no han jugado contra el equipo local.
                    :type equipos_contrincantes: list
                    """
                    
                    if equipos_contrincantes:
                        equipo_contrincante = min(equipos_contrincantes, key=lambda e: distancias[equipo_local - 1][e - 1])
                        """ 
                        :param equipo_contrincante: El equipo contrincante.
                        :type equipo_contrincante: int
                        """
                    
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

        # Nueva parte: emparejar equipos restantes
        while equipos_restantes:
            equipo_local = equipos_restantes.pop(0)
            equipo_contrincante = equipos_restantes.pop(0)
            """ 
            :param equipo_contrincante: El equipo contrincante.
            :type equipo_contrincante: int
            """

            calendario[fecha][equipo_local - 1] = equipo_contrincante
            calendario[fecha][equipo_contrincante - 1] = -equipo_local

            partidos_jugados[equipo_local - 1][equipo_contrincante - 1] = True
            partidos_jugados[equipo_contrincante - 1][equipo_local - 1] = True

    # Partidos negativos (invertir partidos positivos para la segunda mitad del calendario)
    for fecha in range(n_equipos - 1, 2 * (n_equipos - 1)):
        for equipo in range(n_equipos):
            """ 
            :param equipo: El equipo.
            :type equipo: int"""
            calendario[fecha][equipo] = -calendario[fecha - (n_equipos - 1)][equipo]

    return calendario

def imprimir_calendario(calendario, n_equipos, min_partidos, max_partidos):
    """
    Imprime el calendario del torneo.

    :param calendario: El calendario del torneo.
    :type calendario: list
    :param n_equipos: El número de equipos en el torneo.
    :type n_equipos: int
    :param min_partidos: El número mínimo de partidos que un equipo debe jugar.
    :type min_partidos: int
    :param max_partidos: El número máximo de partidos que un equipo puede jugar.
    :type max_partidos: int
    """
    print(f"Número de equipos: {n_equipos}")
    print(f"Mínimo de partidos: {min_partidos}")
    print(f"Máximo de partidos: {max_partidos}")
    
    for fecha, partidos in enumerate(calendario, start=1):
        """ 
        :param fecha: La fecha.
        :type fecha: int"""
        print(f"Fecha {fecha}:", ' '.join(map(str, partidos)))
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generador y Verificador de Calendario")

    # Botón para cargar archivo
    button = tk.Button(root, text="Cargar Archivo", command=elegir_archivo)
    button.pack(pady=20)

    # Widget Text para mostrar el calendario y resultados
    output_text = tk.Text(root, height=20, width=50)
    output_text.pack(pady=20)

    # Lanzar la interfaz gráfica
    root.mainloop()#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Jandi Ramirez, Paula Lemus, Camilo Viedma
# Creation date: 2023-12-01
# Edition date: 2023-12-18

# Description: Generador de calendario de partidos de fútbol

import tkinter as tk
from tkinter import filedialog

def elegir_archivo():
    """
    Permite al usuario seleccionar un archivo y genera un calendario a partir de los datos del archivo.

    :param ruta: La ruta del archivo.
    :type ruta: str
    :return: El calendario generado.
    :rtype: list
    """
    ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo:
        datos = leer_datos_desde_archivo(ruta_archivo)
        """ 
        :param datos: Los datos leídos del archivo.
        :type datos: tuple
        """
        if datos:
            n_equipos, min_partidos, max_partidos, distancias = datos
            calendario = generar_calendario(n_equipos, min_partidos, max_partidos, distancias)

            # Limpiar el área de texto y mostrar el calendario
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Número de equipos: {n_equipos}\n")
            output_text.insert(tk.END, f"Mínimo de partidos: {min_partidos}\n")
            output_text.insert(tk.END, f"Máximo de partidos: {max_partidos}\n")
            output_text.insert(tk.END, "Calendario generado:\n")
            """ 
            :param calendario: El calendario generado.
            :type calendario: list
            """
            for fecha, partidos in enumerate(calendario, start=1):
                """ 
                :param fecha: La fecha.
                :type fecha: int
                :param partidos: Los partidos de la fecha.
                :type partidos: list
                """
                output_text.insert(tk.END, f"Fecha {fecha}: {' '.join(map(str, partidos))}\n")
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Error al generar el calendario.")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No se seleccionó ningún archivo.")


def leer_datos_desde_archivo(ruta):
    """
    Lee los datos de un archivo.

    :param ruta: La ruta del archivo.
    :type ruta: str
    :return: Los datos leídos del archivo.
    :rtype: tuple
    """
    try:
        with open(ruta, 'r') as archivo:
            """ 
            :param archivo: El archivo.
            :type archivo: file
            :return: Los datos leídos del archivo.
            :rtype: tuple
            """
            lineas = archivo.readlines()

            # Leer el número de equipos y los límites de partidos
            n_equipos = int(lineas[0].strip())
            min_partidos = int(lineas[1].strip())
            max_partidos = int(lineas[2].strip())

            """ 
            :param n_equipos: El número de equipos en el torneo.
            :type n_equipos: int
            :param min_partidos: El número mínimo de partidos que un equipo debe jugar.
            :type min_partidos: int
            :param max_partidos: El número máximo de partidos que un equipo puede jugar.
            :type max_partidos: int
            """

            # Leer la matriz de distancias
            distancias = [list(map(int, linea.strip().split())) for linea in lineas[3:]]
            """ 
            :param distancias: Una matriz de distancias entre los equipos.
            :type distancias: list
            """

            return n_equipos, min_partidos, max_partidos, distancias
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def generar_calendario_desde_archivo(ruta):
    """
    Genera un calendario a partir de los datos de un archivo.

    :param ruta: La ruta del archivo.
    :type ruta: str
    :return: El calendario generado.
    :rtype: list
    """
    datos = leer_datos_desde_archivo(ruta)
    """ 
    :param datos: Los datos leídos del archivo.
    :type datos: tuple
    """
    if datos:
        n_equipos, min_partidos, max_partidos, distancias = datos
        calendario = generar_calendario(n_equipos, min_partidos, max_partidos, distancias)
        """ 
        :param calendario: El calendario generado.
        :type calendario: list
        """
        return calendario
    else:
        return None



def generar_calendario(n_equipos, min_partidos, max_partidos, distancias):
    """
    Genera un calendario para un torneo de equipos.

    :param n_equipos: El número de equipos en el torneo.
    :type n_equipos: int
    :param min_partidos: El número mínimo de partidos que un equipo debe jugar.
    :type min_partidos: int
    :param max_partidos: El número máximo de partidos que un equipo puede jugar.
    :type max_partidos: int
    :param distancias: Una matriz de distancias entre los equipos.
    :type distancias: list
    :return: El calendario del torneo.
    :rtype: list
    """
    if n_equipos % 2 != 0:
        n_equipos += 1  # Asegurarse de que el número de equipos sea par

    calendario = [[0] * n_equipos for _ in range(2 * (n_equipos - 1))]
    partidos_jugados = [[False] * n_equipos for _ in range(n_equipos)]

    """
    :param calendario: El calendario del torneo.
    :type calendario: list
    :param partidos_jugados: Una matriz que indica si un equipo ha jugado contra otro.
    :type partidos_jugados: list
    """
    for fecha in range(n_equipos - 1):
        equipos_restantes = list(range(1, n_equipos + 1))
        """
        :param equipos_restantes: Una lista de equipos que aún no han sido emparejados.
        :type equipos_restantes: list
        """

        for equipo_local in range(1, n_equipos + 1):
            """
            :param equipo_local: El equipo local.
            :type equipo_local: int
            """
            if calendario[fecha][equipo_local - 1] == 0:
                partidos_positivos = 1
                """
                :param partidos_positivos: El número de partidos positivos que un equipo debe jugar.
                :type partidos_positivos: int
                """
                for _ in range(partidos_positivos):
                    equipos_contrincantes = [equipo for equipo in equipos_restantes if equipo != equipo_local and not partidos_jugados[equipo_local - 1][equipo - 1]]
                    """
                    :param equipos_contrincantes: Una lista de equipos que aún no han jugado contra el equipo local.
                    :type equipos_contrincantes: list
                    """

                    if equipos_contrincantes:
                        equipo_contrincante = min(equipos_contrincantes, key=lambda e: distancias[equipo_local - 1][e - 1])
                        """ 
                        :param equipo_contrincante: El equipo contrincante.
                        :type equipo_contrincante: int
                        """

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

        # Nueva parte: emparejar equipos restantes
        while equipos_restantes:
            equipo_local = equipos_restantes.pop(0)
            equipo_contrincante = equipos_restantes.pop(0)
            """ 
            :param equipo_contrincante: El equipo contrincante.
            :type equipo_contrincante: int
            """

            calendario[fecha][equipo_local - 1] = equipo_contrincante
            calendario[fecha][equipo_contrincante - 1] = -equipo_local

            partidos_jugados[equipo_local - 1][equipo_contrincante - 1] = True
            partidos_jugados[equipo_contrincante - 1][equipo_local - 1] = True

    # Partidos negativos (invertir partidos positivos para la segunda mitad del calendario)
    for fecha in range(n_equipos - 1, 2 * (n_equipos - 1)):
        for equipo in range(n_equipos):
            """ 
            :param equipo: El equipo.
            :type equipo: int"""
            calendario[fecha][equipo] = -calendario[fecha - (n_equipos - 1)][equipo]

    return calendario

def imprimir_calendario(calendario, n_equipos, min_partidos, max_partidos):
    """
    Imprime el calendario del torneo.

    :param calendario: El calendario del torneo.
    :type calendario: list
    :param n_equipos: El número de equipos en el torneo.
    :type n_equipos: int
    :param min_partidos: El número mínimo de partidos que un equipo debe jugar.
    :type min_partidos: int
    :param max_partidos: El número máximo de partidos que un equipo puede jugar.
    :type max_partidos: int
    """
    print(f"Número de equipos: {n_equipos}")
    print(f"Mínimo de partidos: {min_partidos}")
    print(f"Máximo de partidos: {max_partidos}")

    for fecha, partidos in enumerate(calendario, start=1):
        """ 
        :param fecha: La fecha.
        :type fecha: int"""
        print(f"Fecha {fecha}:", ' '.join(map(str, partidos)))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generador y Verificador de Calendario")

    # Botón para cargar archivo
    button = tk.Button(root, text="Cargar Archivo", command=elegir_archivo)
    button.pack(pady=20)

    # Widget Text para mostrar el calendario y resultados
    output_text = tk.Text(root, height=20, width=50)
    output_text.pack(pady=20)

    # Lanzar la interfaz gráfica
    root.mainloop()