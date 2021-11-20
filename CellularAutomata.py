# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 17:22:40 2021

@author: oscar
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation


class CellularAutomata:

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
        # La región de juego será un cuadrado, para evitar errores se tomará
        # el menor de los tamaños horizontal y vertical.
        self.N = np.min(seed.shape)

    def reset(self):
        self.grid = self.seed

    def plotSeed(self, figArgs={'dpi': 150, 'figsize': (4, 4)}):
        rects = np.zeros((self.N, self.N), dtype=Rectangle)

        fig, ax = plt.subplots(**figArgs)
        ax.axis('equal')
        ax.set_xlim(0, self.N)
        ax.set_ylim(0, self.N)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Rellenamos el array con rectangulos del color adecuado a la célula
        for i in range(self.N):
            for j in range(self.N):
                rects[i, j] = Rectangle(
                    [i, self.N-j-1], 1, 1, color=self.setColor(j, i, self.seed))
                ax.add_artist(rects[i, j])
        plt.show()

    def plotState(self, figArgs={'dpi': 150, 'figsize': (4, 4)}):
        # Rellenamos el array con rectangulos del color adecuado a la célula
        rects = np.zeros((self.N, self.N), dtype=Rectangle)

        fig, ax = plt.subplots(**figArgs)
        ax.axis('equal')
        ax.set_xlim(0, self.N)
        ax.set_ylim(0, self.N)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Rellenamos el array con rectangulos del color adecuado a la célula
        for i in range(self.N):
            for j in range(self.N):
                rects[i, j] = Rectangle(
                    [i, self.N-j-1], 1, 1, color=self.setColor(j, i, self.grid))
                ax.add_artist(rects[i, j])
        plt.show()

    def function(self, neighbours, i, j):
        return self.grid[i, j]

    def update(self):
        """
        Actualiza las células del juego

        """
        # Creamos una matriz y forzamos que en los bordes valga 0
        newGrid = self.grid.copy()
        newGrid[0, :] = 0
        newGrid[self.N-1, :] = 0

        newGrid[:, 0] = 0
        newGrid[:, self.N-1] = 0

        # Recorremos todas las celulas
        for i in range(1, self.N-1):
            for j in range(1, self.N-1):
                neighbours = 0
                # Miramos los vecinos de la célula y contamos als vivas
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if not x == y == 0:
                            neighbours += self.grid[i+x, j+y]
                newGrid[i, j] = self.function(neighbours, i, j)

        self.grid = newGrid

    def animation(self, figArgs={'dpi': 150, 'figsize': (4, 4)}, animArgs={'frames': 1, 'interval': 200}, save=False, filePath='animation'):
        """
        Crea la animación del Juego de la vida

        """

        # Creamos un array de rectangulos vacio que representarán a las células
        rects = np.zeros((self.N, self.N), dtype=Rectangle)

        fig, ax = plt.subplots(**figArgs)
        ax.axis('equal')
        ax.set_xlim(0, self.N)
        ax.set_ylim(0, self.N)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Rellenamos el array con rectangulos del color adecuado a la célula
        for j in range(self.N):
            for i in range(self.N):
                rects[i, j] = Rectangle(
                    [i, self.N-j-1], 1, 1, color=self.setColor(j, i, self.grid))
                ax.add_artist(rects[i, j])

        def init():
            self.reset()

        def animate(k):
            # Cambiamos los colores de los cuadrados
            for i in range(self.N):
                for j in range(self.N):
                    rects[i, j].set_color(self.setColor(j, i, self.grid))
            # Y actualizamos la simulación
            self.update()
            return rects,

        anim = FuncAnimation(
            fig, animate, **animArgs)
        if save:
            anim.save(f'{filePath}.gif')
        return anim

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


class GameOfLife(CellularAutomata):
    def function(self, neighbours, i, j):
        # Una célula muerta con 3 vecinos nace
        if self.grid[i, j] == 0 and neighbours == 3:
            return 1
        # Una célula muerta con 2 o 3 vecinos sigue viva
        elif self.grid[i, j] == 1 and 2 <= neighbours <= 3:
            return 1
        # En otro caso muere
        else:
            return 0


class SmoothNoise(CellularAutomata):
    def function(self, neighbours, i, j):
        if neighbours >= 5:
            return 1
        elif neighbours < 5:
            return 0
