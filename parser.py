from collections import Counter

from node import Node
from graph import plot


nodes = {}


def open_log(filename):
    with open(filename) as f:
        while True:
            data = f.readline()
            if not data:
                break
            yield data.split('\t')


def parse(filename):
    global nodes
    timestamp = 0
    node_id = 0
    message = 0
    for timestamp, node_id, message in open_log(filename):
        node_id = int(node_id[3:])
        if node_id not in nodes:
            nodes[node_id] = Node(node_id)
        nodes[node_id].on_message(timestamp, message)
    get_collisions()


def get_collisions():
    collisions = Counter()
    for node_id, node in nodes.items():
        collisions += node.get_collisions()
    plot(collisions)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Staffetta Log Parser')
    parser.add_argument('filename', help='The name of a log file to be parsed')
    args = parser.parse_args()
    parse(args.filename)
