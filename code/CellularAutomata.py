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
        self.cm = plt.cm.Greys.reversed()
        # La región de juego será un cuadrado, para evitar errores se tomará
        # el menor de los tamaños horizontal y vertical.
        self.N, self.M = seed.shape

    def reset(self):
        self.grid = self.seed

    def plotSeed(self, figArgs={'dpi': 150, 'figsize': (4, 4)}):
        fig, ax = plt.subplots(**figArgs)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        plt.imshow(self.seed, cmap=self.cm, interpolation='none')

    def plotState(self, figArgs={'dpi': 150, 'figsize': (4, 4)}):
        fig, ax = plt.subplots(**figArgs)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        plt.imshow(self.grid, cmap=self.cm, interpolation='none')

    def _functionRules(self, neighbours, i, j):
        return self.grid[i, j]

    def _functionNeighbours(self, i, j):
        neighbours = 0
        # Miramos los vecinos de la célula y contamos als vivas
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not x == y == 0:
                    neighbours += self.grid[i+x, j+y]
        return neighbours

    def update(self):
        """
        Actualiza las células del juego

        """
        # Creamos una matriz y forzamos que en los bordes valga 0
        newGrid = self.grid.copy()
        newGrid[0, :] = 0
        newGrid[self.N-1, :] = 0

        newGrid[:, 0] = 0
        newGrid[:, self.M-1] = 0

        # Recorremos todas las celulas
        for i in range(1, self.N-1):
            for j in range(1, self.M-1):
                neighbours = self._functionNeighbours(i, j)
                newGrid[i, j] = self._functionRules(neighbours, i, j)

        self.grid = newGrid

    def animation(self, figArgs=None, animArgs=None, save=False, filePath='animation'):
        """
        Crea la animación del Juego de la vida

        """
        def init():
            self.reset()
            im.set_array(self.seed)
            return [im]

        def animate(k):
            self.update()
            im.set_array(self.grid)
            return [im]

        animArgs = animArgs or {'frames': 10, 'interval': 200}
        animArgs['init_func'] = animArgs.get('init_func') or init

        figArgs = figArgs or {'dpi': 150, 'figsize': (4, 4)}

        fig, ax = plt.subplots(**figArgs)
        ax.axis('equal')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        im = plt.imshow(self.seed, cmap=self.cm, interpolation='none')

        anim = FuncAnimation(
            fig, animate, **animArgs)
        if save:
            anim.save(f'{filePath}.gif')
        return anim


class GameOfLife(CellularAutomata):
    def _functionRules(self, neighbours, i, j):
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
    def _functionRules(self, neighbours, i, j):
        if neighbours >= 5:
            return 1
        elif neighbours <= 2:
            return 0
        else:
            return self.grid[i, j]
