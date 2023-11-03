import itertools
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Crear una lista para almacenar los nombres de los torneos
torneos = []

# Crear un diccionario para almacenar la información de los torneos
info_torneos = {}

def crear_torneo():
    # Obtener el nombre del torneo ingresado por el usuario
    nombre_torneo = simpledialog.askstring("Crear Torneo", "Ingrese el nombre del torneo:")

    # Verificar si el campo de nombre no está vacío
    if nombre_torneo:
        # Agregar el nombre del torneo a la lista de torneos
        torneos.append(nombre_torneo)
        messagebox.showinfo("Torneo Creado", f"Torneo '{nombre_torneo}' creado")
        info_torneos[nombre_torneo] = {'participantes': [], 'resultados': None, 'ganador': None}
    else:
        messagebox.showerror("Error", "¡Ponle nombre, cohoneee!")

    # Obtener el número de jugadores
    num_jugadores = simpledialog.askinteger("Crear Torneo", "Ingrese el número de jugadores:")

    # Verificar si el número de jugadores es válido
    if num_jugadores < 2:
        messagebox.showerror("Error", "Debe haber al menos 2 jugadores en el torneo.")
        return

    # Crear una lista para almacenar los nombres de los jugadores
    jugadores = []

    # Solicitar los nombres de los jugadores
    for i in range(num_jugadores):
        nombre_jugador = simpledialog.askstring("Crear Torneo", f"Ingrese el nombre del jugador {i + 1}: ")
        jugadores.append(nombre_jugador)
        info_torneos[nombre_torneo]['participantes'].append(nombre_jugador)

    # Distribuir a los jugadores en grupos en partes iguales
    num_grupos = simpledialog.askinteger("Crear Torneo", "Ingrese el número de grupos:")
    jugadores_por_grupo = num_jugadores // num_grupos

    grupos = [[] for _ in range(num_grupos)]

    for i, jugador in enumerate(jugadores):
        grupo_idx = i % num_grupos
        grupos[grupo_idx].append(jugador)

    # Realizar enfrentamientos en la fase de grupos
    resultados_fase_grupos = jugar_fase_grupos(grupos)

    # Continuar con la fase de eliminación
    ganador = jugar_eliminacion(resultados_fase_grupos)

    info_torneos[nombre_torneo]['resultados'] = resultados_fase_grupos
    info_torneos[nombre_torneo]['ganador'] = ganador

def jugar_fase_grupos(grupos):
    resultados = {jugador: 0 for grupo in grupos for jugador in grupo}

    for grupo in grupos:
        emparejamientos_grupo = list(itertools.combinations(grupo, 2))
        random.shuffle(emparejamientos_grupo)

        for i, enfrentamiento in enumerate(emparejamientos_grupo):
            jugador1, jugador2 = enfrentamiento
            resultado = simpledialog.askstring("Fase de Grupos", f"Enfrentamiento {i + 1}: {jugador1} vs {jugador2} (1/2 para salir): ")

            if resultado == '1':
                resultados[jugador1] += 1
            elif resultado == '2':
                resultados[jugador2] += 1

    return resultados

def jugar_eliminacion(resultados_fase_grupos):
    jugadores = list(resultados_fase_grupos.keys())
    random.shuffle(jugadores)

    while len(jugadores) > 1:
        ganadores = []
        for i in range(0, len(jugadores), 2):
            jugador1 = jugadores[i]
            jugador2 = jugadores[i + 1]

            resultado = simpledialog.askstring("Eliminación", f"Enfrentamiento: {jugador1} vs {jugador2} (1/2 para salir): ")
            if resultado == '1':
                ganadores.append(jugador1)
            else:
                ganadores.append(jugador2)

        jugadores = ganadores

    campeon = jugadores[0]
    messagebox.showinfo("Torneo Finalizado", f"¡El campeón del torneo es {campeon}!")
    return campeon

def ver_torneos():
    if torneos:
        torneo_seleccionado = simpledialog.askstring("Ver Torneos", "Escribe el nombre del torneo que deseas ver:")
        if torneo_seleccionado in info_torneos:
            info_torneo = info_torneos[torneo_seleccionado]
            participantes = ', '.join(info_torneo['participantes'])
            resultados = info_torneo['resultados']
            ganador = info_torneo['ganador']
            mensaje = f"Participantes: {participantes}\nResultados de la fase de grupos: {resultados}\nGanador: {ganador}"
            messagebox.showinfo("Información del Torneo", mensaje)
        else:
            messagebox.showerror("Error", "Torneo no encontrado.")
    else:
        messagebox.showinfo("Información", "No hay torneos registrados")

def eliminar_torneo():
    nombre_torneo_a_eliminar = simpledialog.askstring("Eliminar Torneo", "Ingrese el nombre del torneo a eliminar:")
    if nombre_torneo_a_eliminar:
        if nombre_torneo_a_eliminar in torneos:
            torneos.remove(nombre_torneo_a_eliminar)
            info_torneos.pop(nombre_torneo_a_eliminar, None)
            messagebox.showinfo("Torneo Eliminado", f"Torneo '{nombre_torneo_a_eliminar}' eliminado")
        else:
            messagebox.showerror("Error", f"Torneo '{nombre_torneo_a_eliminar}' no existe")
    else:
        messagebox.showerror("Error", "¡Falta un nombre, amigo!")

def seleccionar_opcion():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    while True:
        opcion = simpledialog.askinteger("Menú", "MENU:\n1. Crear un torneo\n2. Ver torneos\n3. Eliminar un torneo\n4. Salir del programa\nSeleccione una opción:")

        if opcion == 1:
            crear_torneo()
        elif opcion == 2:
            ver_torneos()
        elif opcion == 3:
            eliminar_torneo()
        elif opcion == 4:
            messagebox.showinfo("Hasta luego", "No vemos, que Dios te bendiga")
            break
        else:
            messagebox.showerror("Error", "¿Qué estás haciendo? ¡Ahí no, amigo!")

seleccionar_opcion()
