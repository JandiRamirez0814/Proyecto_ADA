import tkinter as tk
from tkinter import filedialog
import random

class Nodo:
    def __init__(self, dato=None, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente

class Calendario:
    def __init__(self, n):
        self.n = n
        self.matriz = [[None] * n for _ in range(2 * (n-1))]
        for i in range(2 * (n - 1)):
            for j in range(n):
                self.matriz[i][j] = Nodo()
    def __str__(self):
        output = ""
        for fila in self.matriz:
            for nodo in fila:
                actual = nodo.siguiente
                while actual:
                    output += f"{actual.dato} "
                    actual = actual.siguiente
                output += "\n"
        matrix_output = "\n".join(output.splitlines())
        return matrix_output

def cargar_entrada(archivo):
    with open(archivo, 'r') as f:
        n = int(f.readline().strip())
        M_in = int(f.readline().strip())
        M_ax = int(f.readline().strip())
        D = [list(map(int, line.split())) for line in f.readlines()]
    return n, M_in, M_ax, D

def generar_calendario(n, M_in, M_ax, D, max_intentos=10):
    listaim=""
    for _ in range(max_intentos):
        calendario = Calendario(n)

        equipos_disponibles = list(range(1, n + 1))

        for fecha in range(2 * (n - 1)):
            equipos_asignados = random.sample(equipos_disponibles, n)

            for j in range(n):
                equipo_local = equipos_asignados[j]
                equipo_visitante = equipos_asignados[(j + fecha) % n]
                if fecha > 0 and calendario.matriz[fecha - 1][j].siguiente.dato == -equipo_visitante:
                    equipo_local, equipo_visitante = equipo_visitante, equipo_local
                calendario.matriz[fecha][j].siguiente = Nodo(equipo_local)
                calendario.matriz[fecha][j].siguiente.siguiente = Nodo(-equipo_visitante)
                
            listaim+=str(calendario.matriz[i][j].dato)+" "
        listaim+="\n"
    print(listaim)
    #imprimir calendario 
    for i in range(0,2*(n-1)):
        for j in range(0,n):
            print(calendario.matriz[i][j].dato)
        print("\n")
        
    if validar_calendario(calendario, n, M_in, M_ax) and comprobar_calendario(calendario, n, M_in, M_ax, D):
            return calendario
    #mostrar la matriz de calendario
    raise ValueError("No se pudo generar un calendario válido")


def validar_calendario(calendario, n, M_in, M_ax):
    for j in range(n):
        gira_actual = 0
        permanencia_actual = 0

        for i in range(2 * (n - 1)):
            if calendario.matriz[i][j].siguiente is not None:
                actual = calendario.matriz[i][j].siguiente
                while actual:
                    if actual.dato is not None:
                        if actual.dato > 0:
                            gira_actual = 0
                            permanencia_actual += 1
                        else:
                            permanencia_actual = 0
                            gira_actual += 1

                        if gira_actual > M_ax or permanencia_actual > M_ax or permanencia_actual < M_in:
                            return False

                    actual = actual.siguiente

    for i in range(2 * (n - 2)):
        for j in range(n):
            if (
                calendario.matriz[i][j].siguiente is not None and
                calendario.matriz[i + 2][j].siguiente is not None and
                calendario.matriz[i][j].siguiente.dato == calendario.matriz[i + 2][j].siguiente.dato
            ):
                return False

    return True


def comprobar_calendario(calendario, n, M_in, M_ax, D):
    for i in range(n):
        actual = calendario.matriz[0][i].siguiente
        while actual:
            if actual.dato < 0:
                rival = abs(actual.dato)
                distancia = D[i][rival - 1]
                if distancia > M_ax:
                    return False

            actual = actual.siguiente

    return True

def cargar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        n, M_in, M_ax, D = cargar_entrada(file_path)
        try:
            calendario = generar_calendario(n, M_in, M_ax, D)
            # Actualiza el widget Text para mostrar el calendario en la interfaz gráfica
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Calendario generado:\n{calendario}\n")
            if validar_calendario(calendario, n, M_in, M_ax) and comprobar_calendario(calendario, n, M_in, M_ax, D):
                output_text.insert(tk.END, "El calendario cumple con todas las restricciones.\n")
            else:
                output_text.insert(tk.END, "El calendario no cumple con todas las restricciones.\n")
        except ValueError as e:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Error: {str(e)}\n")


# Crear la interfaz gráfica
root = tk.Tk()
root.title("Generador y Verificador de Calendario")

# Botón para cargar archivo
button = tk.Button(root, text="Cargar Archivo", command=cargar_archivo)
button.pack(pady=20)

# Widget Text para mostrar el calendario y resultados
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=20)

# Lanzar la interfaz gráfica
root.mainloop()
