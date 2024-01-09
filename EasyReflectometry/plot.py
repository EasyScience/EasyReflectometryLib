__author__ = 'github.com/arm61'

import scipp as sc
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']


def plot(data: sc.DataGroup) -> None:
    """
    A general plotting function for EasyReflectometry.

    :param data: the DataGroup to be plotted.

    :returns: The plot canvas.
    """
    if len([i for i in list(data.keys()) if 'SLD' in i]) == 0:
        plot_sld = False
        fig = plt.figure(figsize=(5, 3))
        gs = GridSpec(1, 1, figure=fig)
    else:
        plot_sld = True
        fig = plt.figure(figsize=(5, 6))
        gs = GridSpec(2, 1, figure=fig)
        ax2 = fig.add_subplot(gs[1, 0])
    ax1 = fig.add_subplot(gs[0, 0])
    refl_nums = [k[3:] for k in data['coords'].keys() if 'Qz' == k[:2]]
    for i, refl_num in enumerate(refl_nums):
        copy = sc.DataArray(
            data=data['data'][f'R_{refl_num}'],
            coords={f'Qz_{refl_num}': data['coords'][f'Qz_{refl_num}']}
        )
        copy.data *= sc.scalar(10.**i, unit=copy.unit)
        copy.coords[f'Qz_{refl_num}'].variances = None
        sc.plot(
            copy,
            ax=ax1,
            norm='log',
            linestyle='',
            marker='.',
            color=color_cycle[i]
        )
        try:
            copy = sc.DataArray(
                data=data['data'][f'R_{refl_num}_model'],
                coords={f'Qz_{refl_num}': data['coords'][f'Qz_{refl_num}']}
            )
            copy.data *= sc.scalar(10.**float(i))
            copy.coords[f'Qz_{refl_num}'].variances = None
            sc.plot(
                copy,
                ax=ax1,
                norm='log',
                linestyle='--',
                color=color_cycle[i],
                marker=''
            )
        except KeyError:
            pass
    ax1.autoscale(True)
    ax1.relim()
    ax1.autoscale_view()

    if plot_sld:
        for i, refl_num in enumerate(refl_nums):
            copy = sc.DataArray(
                data=data[f'SLD_{refl_num}'],
                coords={f'z_{refl_num}': data['coords'][f'z_{refl_num}']}
            )
            copy.data += sc.scalar(10. * i, unit=copy.unit)
            sc.plot(
                data[f'SLD_{refl_num}'],
                ax=ax2,
                linestyle='-',
                color=color_cycle[i],
                marker=''
            )
        ax2.autoscale(True)
        ax2.relim()
        ax2.autoscale_view()
