import scipp as sc
import ipympl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def plot(data: sc.Dataset) -> ipympl.backend_nbagg.Canvas:
    """
    A general plotting function for EasyReflectometry.
    
    :param data: the Dataset to be plotted.
    
    :returns: The plot canvas.
    """
    if len([i for i in list(data.keys()) if 'sld' in i]) == 0:
        fig = plt.figure(figsize=(5, 3))
        gs = GridSpec(1, 1, figure=fig)
    else:
        fig = plt.figure(figsize=(5, 6))
        gs = GridSpec(2, 1, figure=fig)
        ax2 = fig.add_subplot(gs[1, 0])
    ax1 = fig.add_subplot(gs[0, 0])
    refl_nums = [k[2:] for k, v in data.coords.items() if 'Qz' == k[:2]]
    for i in refl_nums:
        sc.plot(data[f'data_set{i}'], ax=ax1, norm='log', linestyle='', marker='o')
        try:
            sc.plot(data[f'data_set{i}_best_fit'], ax=ax1, norm='log', linestyle='-', color='orange', marker='')
        except sc.NotFoundError:
            pass
    sld_nums = [k[1:] for k, v in data.coords.items() if 'z' == k[0]]
    for i in sld_nums:
        sc.plot(data[f'data_set{i}_sld'], ax=ax2, linestyle='-', color='orange', marker='')
    return fig.canvas