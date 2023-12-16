import random

def generar_calendario(n_equipos, min_partidos, max_partidos, distancias):
    if n_equipos % 2 != 0:
        n_equipos += 1  # Asegurarse de que el número de equipos sea par

    calendario = [[0] * n_equipos for _ in range(2 * (n_equipos - 1))]
    partidos_jugados = [[False] * n_equipos for _ in range(n_equipos)]

    # Partidos positivos
    for fecha in range(n_equipos - 1):
        equipos_restantes = list(range(1, n_equipos + 1))

        for equipo_local in range(1, n_equipos + 1):
            if calendario[fecha][equipo_local - 1] == 0:
                #partidos_positivos = random.randint(min_partidos, min(max_partidos, n_equipos - 1))
                partidos_positivos = 1
                for _ in range(partidos_positivos):
                    equipos_contrincantes = [equipo for equipo in equipos_restantes if equipo != equipo_local and not partidos_jugados[equipo_local - 1][equipo - 1]]

                    if equipos_contrincantes:
                        # Elegir el contrincante con la menor distancia
                        equipo_contrincante = min(equipos_contrincantes, key=lambda e: distancias[equipo_local - 1][e - 1])
                        
                        calendario[fecha][equipo_local - 1] = equipo_contrincante
                        calendario[fecha][equipo_contrincante - 1] = -equipo_local

                        partidos_jugados[equipo_local - 1][equipo_contrincante - 1] = True
                        partidos_jugados[equipo_contrincante - 1][equipo_local - 1] = True

                        if equipo_local in equipos_restantes:
                            equipos_restantes.remove(equipo_local)
                            equipos_restantes.remove(equipo_contrincante)
                    else:
                        break  # No hay equipos contrincantes disponibles, salir del bucle

    # Partidos negativos (invertir partidos positivos para la segunda mitad del calendario)
    for fecha in range(n_equipos - 1, 2 * (n_equipos - 1)):
        for equipo in range(n_equipos):
            calendario[fecha][equipo] = -calendario[fecha - (n_equipos - 1)][equipo]

    return calendario

def imprimir_calendario(calendario):
    for fecha, partidos in enumerate(calendario, start=1):
        print(f"Fecha {fecha}:", ' '.join(map(str, partidos)))

if __name__ == "__main__":
    # Matriz de distancias de ejemplo (asegurando simetría y ceros en la diagonal)
    distancias = [
        [0, 745, 665, 929],
        [745, 0, 80, 337],
        [665, 80, 0, 380],
        [929, 337, 380, 0]
    ]

    for i in range(0, 10):
        calendario = generar_calendario(4, 1, 3, distancias)
        print("\n")
        imprimir_calendario(calendario)
