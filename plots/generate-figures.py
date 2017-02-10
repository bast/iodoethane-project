import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
from glob import glob
import sys
import os


def read_data(path):
    data = {}
    for f in glob('{0}/*'.format(path)):
        file_name = os.path.basename(f)
        file_name_no_suffix = os.path.splitext(file_name)[0]
        with open(f, 'r') as _handle:
            _list = [float(line) for line in _handle]
            data[file_name_no_suffix] = np.array(_list)
    return data


def plot(ax, plt, x, x_spline, y, color, markers, xlabel, ylabel, plot_legend, ax_legend, file_name, dpi, linewidth):
    ax.plot(x, y, '{0}{1}'.format(color, markers[0]), linewidth=linewidth)
    if plot_legend is not None:
        ax.plot(x_spline, spline(x, y, x_spline), '{0}{1}'.format(color, markers[1]), linewidth=linewidth, label=plot_legend)
    else:
        ax.plot(x_spline, spline(x, y, x_spline), '{0}{1}'.format(color, markers[1]), linewidth=linewidth)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel, color=color)
    for tl in ax.get_yticklabels():
        tl.set_color(color)
    if plot_legend is not None:
        plt.legend()
    if ax_legend:
        ax.legend(loc=2)
    plt.savefig(file_name, dpi=dpi)


def main(dpi):
    data = read_data('data')
    data['coupling_fc_sd'] = data['coupling_sf'] - data['coupling_sf_nospin']
    data['shielding_diff'] = data['shielding_sf'] - data['shielding']

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    def _plot(ax, y, color, markers, ylabel, plot_legend, ax_legend, file_name):
        x = np.array(range(0, 190, 10))
        x_spline = np.linspace(x.min(), x.max(), 300)
        xlabel = 'I-C-C-H dihedral angle'
        linewidth = 2.0
        return plot(ax, plt, x, x_spline, y, color, markers, xlabel, ylabel, plot_legend, ax_legend, file_name, dpi, linewidth)

    _plot(ax1, data['energy'], 'b', ('x', '-'), 'Energy (hartree)', None, False, 'plot1.png')
    _plot(ax2, data['coupling'], 'r', ('x', '-'), 'K(H,I) in SI units', 'PSO + FC + SD + DSO (HuzIII dyall.v3z)', False, 'plot2.png')
    _plot(ax2, data['coupling_su3'], 'r', ('x', '--'), 'K(H,I) in SI units', 'PSO + FC + SD + DSO (HuzIIIsu3 dyall.v3z)', False, 'plot3.png')
    _plot(ax2, data['coupling_sf'], 'r', ('o', '-'), 'K(H,I) in SI units', 'PSO + FC + SD + DSO (HuzIII dyall.v3z; SOC-free)', False, 'plot4.png')
    _plot(ax2, data['coupling_fc_sd'], 'r', ('^', '-'), 'K(H,I) in SI units', 'FC + SD (HuzIII dyall.v3z)', False, 'plot5.png')

    plt.close('all')
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    _plot(ax2, data['coupling_fc_sd'], 'r', ('^', '-'), 'K(H,I) in SI units', 'FC + SD', False, 'plot6.png')
    _plot(ax1, data['shielding'], 'g', ('x', '-'), 'sigma(H) in ppm', 'with SOC', True, 'plot7.png')
    _plot(ax1, data['shielding_sf'], 'g', ('x', '--'), 'sigma(H) in ppm', 'no SOC', True, 'plot8.png')

    plt.close('all')
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    _plot(ax2, data['coupling_fc_sd'], 'r', ('^', '-'), 'K(H,I) in SI units', 'FC + SD', False, 'plot9.png')
    _plot(ax1, data['shielding_diff'], 'g', ('o', '-'), 'sigma(H) in ppm', 'only SOC', True, 'plot9.png')


if __name__ == '__main__':
    dpi = int(sys.argv[-1])
    main(dpi)
