from collections import defaultdict, OrderedDict
from decimal import Decimal
from os import path, listdir, makedirs, remove

import pylab as pl

import parser as s_parser

out = '/out'
script_directory = path.dirname(path.realpath(__file__))
out_directory = script_directory + out

tableau20 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40),
             (148, 103, 189), (140, 86, 75), (227, 119, 194), (127, 127, 127),
             (188, 189, 34), (23, 190, 207)]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

def setup_out_directory():
    if not path.exists(out_directory):
        makedirs(out_directory)


def save_plot(name):
    pl.savefig(out_directory + path.sep + name + '.png')


def plot_line_graph(title, name, xname, x, yname, y, color, xlimit=None, ylimit=None):
    pl.title(title, fontsize=22)
    pl.xlabel(xname, fontsize=16)
    pl.ylabel(yname, fontsize=16)
    if ylimit is not None:
        pl.ylim(ymin=0, ymax=ylimit)
    if xlimit is not None:
        pl.xlim(xmin=0, xmax=xlimit)
    pl.grid('on')

    line, = pl.plot(x, y, linestyle=':', marker='o', label=name)
    line.set_antialiased(True)
    line.set_color(color)
    line.set_linewidth(4)

def get_data(index, data_type, is_cdf=False, postfix=''):
    xs = []
    collisions = []
    get_collisions = {
        'frequency': s_parser.get_fc,
        'time': s_parser.get_tc,
    }
    total = 0
    for x, collision in sorted(get_collisions[data_type]('data/loglistener{}{}.txt'.format(index, postfix))):
        print(x, collision)
        xs.append(x)
        total += collision
        collisions.append(total if is_cdf else collision)
    if is_cdf and False:
        collisions = [ _ / total for _ in collisions]
    print(total)
    return xs, collisions


def plot(data_type, is_cdf=False, postfix=''):
    setup_out_directory()
    indexes = [9, 16, 25, 36]
    for index in indexes:
        xs, collisions = get_data(index, data_type, is_cdf, postfix)
        xlimit = 17 if data_type == 'time' else None
        ylimit = 300 if data_type == 'time' else None
        xname = data_type
        yname = 'collision'
        title = xname.title() + ' - ' + yname.title() + (' - CDF ' if is_cdf else '') + ' Graph'
        plot_line_graph(title, str(index), xname, xs, yname, collisions, tableau20[index // 10], xlimit, ylimit)
    pl.legend(loc=2)
    pl.show()
    pl.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Staffetta Parser')
    parser.add_argument('data_type', choices=['frequency', 'time'])
    parser.add_argument('is_cdf', choices=['true', 'false'], default='false')
    parser.add_argument('postfix', type=str, default='')

    args = parser.parse_args()
    plot(args.data_type, args.is_cdf == 'true', args.postfix)
