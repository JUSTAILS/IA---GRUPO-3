import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Tamaño de la cuadrícula nxn
n = 2

size= (n, n)

mem = [0]*(size[0]*size[1])

# Metrica de balance energético
energia = 0

print(mem)

class VisualEnvironment:
    def __init__(self):

        # Cuadrícula: 0 = Limpio, 1 = Sucio
        self.grid = np.random.choice([0, 1], size=size)
        self.sucio = np.sum(self.grid) # conteo de celdas sucias

        # Posición inicial aleatoria (fila, columna)
        self.agent_pos = [random.randint(0, n-1), random.randint(0, n-1)]

        # Configuración del gráfico interactivo
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

    def render(self, step, action):
        self.ax.clear()
        # Dibujar la cuadrícula (colores cambian según limpieza)
        self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)
        
        # Dibujar al agente como un punto rojo grande
        self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', markersize=40)
        
        # Etiquetas de estado
        for i in range(n):
            for j in range(n):
                estado = "SUCIO" if self.grid[i, j] == 1 else "LIMPIO"
                self.ax.text(j, i, estado, ha='center', va='center', 
                             color='black', weight='bold', fontsize=12)

        self.ax.set_title(f"Paso: {step} | Acción: {action}", pad=20)
        self.ax.set_xticks(range(n))
        self.ax.set_yticks(range(n))
        self.ax.set_xticks(
            np.arange(-0.5, n, 1),
            minor=True
        )
        self.ax.set_yticks(
            np.arange(-0.5, n, 1),
            minor=True
        )

        self.ax.grid(
            which='minor',
            color='black',
            linestyle='-',
            linewidth=1
        )

        self.ax.tick_params(
            which='minor',
            bottom=False,
            left=False
        )
        plt.draw()
        plt.pause(1.5) # Pausa para visualizar la animación

    def get_percept(self):
        return self.agent_pos.copy(), self.grid[self.agent_pos[0], self.agent_pos[1]]

    def execute_action(self, action):

        global energia
        fila, columna = self.agent_pos
        indice = fila * n + columna

        if action == 'Suck':
            if self.grid[fila, columna] == 1:
                self.grid[fila, columna] = 0
                # Actualizar la memoria del agente para reflejar que la celda ha sido limpiada
                mem[indice] = 1
                energia -=1
        elif action == 'Up' and self.agent_pos[0] > 0:
            self.agent_pos[0] -= 1
            energia += 1
        elif action == 'Down' and self.agent_pos[0] < n-1:
            self.agent_pos[0] += 1
            energia += 1
        elif action == 'Left' and self.agent_pos[1] > 0:
            self.agent_pos[1] -= 1
            energia += 1
        elif action == 'Right' and self.agent_pos[1] < n-1:
            self.agent_pos[1] += 1
            energia += 1

    def is_completely_clean(self):
        return np.sum(self.grid) == 0

class RandomVacuumAgent:
    def __init__(self):
        self.mem = [0] * (n * n)

    def act(self, percept):
        pos, status = percept

        fila, columna = pos
        indice = fila * n + columna

        if status == 1:
            self.mem[indice] = 1
            return 'Suck'

        self.mem[indice] = 1

        movimientos_posibles = []

        if fila > 0 and self.mem[(fila - 1) * n + columna] == 0:
            movimientos_posibles.append('Up')

        if fila < n - 1 and self.mem[(fila + 1) * n + columna] == 0:
            movimientos_posibles.append('Down')

        if columna > 0 and self.mem[fila * n + columna - 1] == 0:
            movimientos_posibles.append('Left')

        if columna < n - 1 and self.mem[fila * n + columna + 1] == 0:
            movimientos_posibles.append('Right')

        if movimientos_posibles:
            return random.choice(movimientos_posibles)

        return 'Stop'

if __name__ == "__main__":
    env = VisualEnvironment()
    agent = RandomVacuumAgent()

    env.render(step=0, action="Inicio")

    for paso in range(1, n*n*2+1):
        percept = env.get_percept()
        action = agent.act(percept)

        if action == 'Stop':
            print("No hay celdas adyacentes pendientes.")
            break

        env.execute_action(action)
        env.render(step=paso, action=action)
        
        if env.is_completely_clean() and action != 'Suck':
            print(f"¡Entorno {n}x{n} completamente limpio!")
            break

    print("Rendimiento:", env.sucio / paso) # Métrica de rendimiento: celdas sucias / pasos
    print("Gasto energetico:", energia) # Metrica de balance energetico: energia gastada
    plt.ioff()
    plt.show()
