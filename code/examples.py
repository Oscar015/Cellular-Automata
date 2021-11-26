# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 08:57:10 2021

@author: oscar
"""
import numpy as np
import matplotlib.pyplot as plt
from CellularAutomata import GameOfLife, SmoothNoise

seed = np.random.randint(0, 2, size=(100, 100))

figArgs = {'dpi': 100, 'figsize': (5, 5)}
animArgs1 = {'frames': 100, 'interval': 200, 'init_func': None}
animArgs2 = {'frames': 10, 'interval': 200, 'repeat': True}


GOL = GameOfLife(seed)
GOL.plotSeed(figArgs)
GOL.update()
GOL.plotState(figArgs)
GOL.reset()
anim = GOL.animation(figArgs, animArgs1, save=False,
                     filePath='..\media\GameOfLife2')
plt.show()


SN = SmoothNoise(seed)
anim = SN.animation(figArgs, animArgs2, save=False,
                    filePath='..\media\smoothNoise2')
plt.show()
