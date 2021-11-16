# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 17:22:40 2021

@author: oscar
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation


class GameOfLife:

    def __init__(self, seed):
        """
        Inicializamos el juego

        Parameters
        ----------
        seed : 2D-narray
            Matriz NxM con las condiciones iniciales
            para el juego.
            1 para las células vivas
            0 para las muertas
        """
        self.seed = seed
        self.grid = seed

    def plotSeed(self, figArgs={'dpi': 150, 'figsize': (4, 4)}):
        rects = np.zeros((N, N), dtype=Rectangle)

        fig, ax = plt.subplots(**figArgs)
        ax.axis('equal')
        ax.set_xlim(0, N)
        ax.set_ylim(0, N)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Rellenamos el array con rectangulos del color adecuado a la célula
        for i in range(N):
            for j in range(N):
                rects[i, j] = Rectangle(
                    [i, N-j-1], 1, 1, color=self.setColor(j, i, self.seed))
                ax.add_artist(rects[i, j])
        plt.show()

    def update(self):
        """
        Actualiza las células del juego

        """
        # Creamos una matriz y forzamos que en los bordes valga 0
        N, M = self.grid.shape
        newGrid = self.grid.copy()
        newGrid[0, :] = 0
        newGrid[N-1, :] = 0

        newGrid[:, 0] = 0
        newGrid[:, M-1] = 0

        # Recorremos todas las celulas
        for i in range(1, N-1):
            for j in range(1, M-1):
                neighbours = 0
                # Miramos los vecinos de la célula y contamos als vivas
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if not x == y == 0:
                            neighbours += self.grid[i+x, j+y]
                # Una célula muerta con 3 vecinos nace
                if self.grid[i, j] == 0 and neighbours == 3:
                    newGrid[i, j] = 1
                # Una célula muerta con 2 o 3 vecinos sigue viva
                elif self.grid[i, j] == 1 and 2 <= neighbours <= 3:
                    newGrid[i, j] = 1
                # En otro caso muere
                else:
                    newGrid[i, j] = 0
        self.grid = newGrid

    def animation(self, figArgs={'dpi': 150, 'figsize': (4, 4)}):
        """
        Crea la animación del Juego de la vida

        """
        # Creamos un array de rectangulos vacio que representarán a las células
        self.rects = np.zeros((N, N), dtype=Rectangle)

        self.fig, self.ax = plt.subplots(**figArgs)
        self.ax.axis('equal')
        self.ax.set_xlim(0, N)
        self.ax.set_ylim(0, N)
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)

        # Rellenamos el array con rectangulos del color adecuado a la célula
        for j in range(N):
            for i in range(N):
                self.rects[i, j] = Rectangle(
                    [i, N-j-1], 1, 1, color=self.setColor(j, i, self.grid))
                self.ax.add_artist(self.rects[i, j])

        def animate(k):
            # Cambiamos los colores de los cuadrados
            for j in range(N):
                for i in range(N):
                    self.rects[i, j].set_color(self.setColor(j, i, self.grid))
            # Y actualizamos la simulación
            self.update()
            return self.rects,

        self.anim = FuncAnimation(
            self.fig, animate, frames=30, interval=200)
        return self.anim

    def setColor(self, i, j, grid):
        """
        Dado una célula viva (Blanco) o muerta (negro) asigna un color al
        cuadrado que la representa
        Parameters
        ----------
        i : int
        j : int
        Indices de la matriz de rectángulos
        grid : 2D narray
            matriz con los datos de la simulación

        Returns
        -------
        str
            color de la célula

        """
        if grid[i, j] == 1:
            return 'white'
        else:
            return 'black'

##########################################################################


if __name__ == '__main__':
    N = 20

    # seed = np.zeros((N, N), dtype=int)
    # init = [N//3, N//3], [N//3, N//3+1], [N//3-1, N//3+2],\
    #     [N//3+1, N // 3+2], [2*N//3, 2*N//3],\
    #     [2*N//3, 2*N//3+1], [2*N//3, 2*N//3+2], [2*N//3+2, 2*N//3],\
    #     [2*N//3-1, 2*N//3]

    # for index in init:
    #     seed[index[1], index[0]] = 1

    seed = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    GOL = GameOfLife(seed)
    GOL.plotSeed(figArgs={'dpi': 150, 'figsize': (5, 5)})
    anim = GOL.animation(figArgs={'dpi': 150, 'figsize': (5, 5)})
    plt.show()
