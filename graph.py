from collections import defaultdict, OrderedDict
from decimal import Decimal
from os import path, listdir, makedirs, remove

import pylab as pl

import parser

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
    else:
        for _file in listdir(out_directory):
            remove(out_directory + path.sep + _file)


def save_plot(name):
    pl.savefig(out_directory + path.sep + name + '.png')


def plot_line_graph(name, x, y, color):
    pl.title('Frequency Collision Graph', fontsize=22)
    pl.xlabel('Frequency', fontsize=16)
    pl.ylabel('Collisions', fontsize=16)
    pl.grid('on')

    line, = pl.plot(x, y, '-', label=name)
    line.set_antialiased(True)
    line.set_color(color)

def get_data(index):
    frequencies = []
    collisions = []
    total = 0
    for frequency, collision in sorted(parser.get_fc('data/loglistener{}.txt'.format(index))):
        print(frequency, collision)
        frequencies.append(frequency)
        collisions.append(collision)
        total += collision
    print(total)
    return frequencies, collisions


def plot():
    setup_out_directory()
    indexes = [10, 20, 30, 40, 50]
    for index in indexes:
        frequencies, collisions = get_data(index)
        plot_line_graph(index, frequencies, collisions, tableau20[index // 10])
    pl.legend()
    pl.show()
    pl.close()


if __name__ == '__main__':
    plot()
