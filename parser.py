from collections import Counter
from datetime import datetime
from decimal import Decimal

from node import Node


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


def get_fc(filename):
    ''' frequencies and collisions '''
    parse(filename)
    collisions = Counter()
    for node_id, node in nodes.items():
        collisions += node.get_fcs()
    return collisions.most_common()


def get_tc(filename):
    ''' times and collisions '''
    parse(filename)
    collisions = Counter()
    for node_id, node in nodes.items():
        print(node.get_tcs())
        for timestamp, collision in node.get_tcs().most_common():
            print(timestamp)
            print(datetime.strptime(timestamp, '%M:%S.%f'))
            timestamp = Decimal((datetime.strptime(timestamp, '%M:%S.%f') - datetime(1900, 1, 1)).total_seconds()).quantize(Decimal('1'))
            print(timestamp)
            collisions.update({timestamp: collision})
    return collisions.most_common()
    collisions = [ _ / total for _ in collisions]
