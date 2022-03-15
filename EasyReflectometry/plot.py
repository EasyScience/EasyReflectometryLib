__author__ = 'github.com/arm61'

import numpy as np
import scipp as sc
import ipympl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']


def plot(data: sc.Dataset) -> ipympl.backend_nbagg.Canvas:
    """
    A general plotting function for EasyReflectometry.
    
    :param data: the Dataset to be plotted.
    
    :returns: The plot canvas.
    """
    if len([i for i in list(data.keys()) if 'SLD' in i]) == 0:
        fig = plt.figure(figsize=(5, 3))
        gs = GridSpec(1, 1, figure=fig)
    else:
        fig = plt.figure(figsize=(5, 6))
        gs = GridSpec(2, 1, figure=fig)
        ax2 = fig.add_subplot(gs[1, 0])
    ax1 = fig.add_subplot(gs[0, 0])
    refl_nums = [k[3:] for k, v in data.coords.items() if 'Qz' == k[:2]]
    for i, name in enumerate(refl_nums):
        copy = data[f'R_{name}'].copy()
        copy.data *= sc.scalar(10.**i, unit=copy.unit)
        sc.plot(copy,
                ax=ax1,
                norm='log',
                linestyle='',
                marker='.',
                color=color_cycle[i])
        try:
            copy = data[f'R_{name}_model'].copy()
            copy.data *= sc.scalar(10.**float(i))
            sc.plot(copy,
                    ax=ax1,
                    norm='log',
                    linestyle='--',
                    color=color_cycle[i],
                    marker='')
        except KeyError:
            pass
    ax1.autoscale(True)
    ax1.relim()
    ax1.autoscale_view()

    sld_nums = [k[2:] for k, v in data.coords.items() if 'z' == k[0]]
    for i, name in enumerate(refl_nums):
        try:
            copy = data[f'SLD_{name}'].copy()
            copy.data += sc.scalar(10. * i, unit=copy.unit)
            sc.plot(data[f'SLD_{name}'],
                    ax=ax2,
                    linestyle='-',
                    color=color_cycle[i],
                    marker='')
        except KeyError:
            pass
    try:
        ax2.autoscale(True)
        ax2.relim()
        ax2.autoscale_view()
    except UnboundLocalError:
        pass
    return fig.canvas
