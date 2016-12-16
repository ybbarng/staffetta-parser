from collections import Counter
from datetime import datetime
from decimal import Decimal

from numpy import std

from node import Node

nodes = {}


def open_log(filename):
    with open(filename) as f:
        while True:
            data = f.readline()
            if not data:
                break
            yield data.split('\t')


def get_fairness(nodes):
    hop_groups = [[2, 4], [6, 8]]
    stds = []
    for hop_group in hop_groups:
        buf = []
        for node_id in hop_group:
            in_messages = nodes[node_id].in_messages
            buf.append(in_messages)
        stds.append(std(buf))
    return stds

def save_dfrequency(filename, dfrequency):
    with open('dfrequency-' + filename, 'w') as f:
        for t, df in dfrequency:
            f.write('{},{}\n'.format(t, df))

dfrequency_sum = 0
def parse(filename):
    global nodes, dfrequency_sum
    nodes = {}
    for i in range(1, 10):
        nodes[i] = Node(i)

    dfrequency = []

    def _parse(node, timestamp, argv):
        global dfrequency_sum

        if argv[0] == 2:
            dfrequency_sum += abs(node.frequency - argv[2])
            dfrequency.append((timestamp, dfrequency_sum))
            node.frequency = argv[2]
        elif argv[0] == 5:
            sender = nodes[argv[1]]
            receiver = nodes[argv[2]]
            receiver.in_messages += 1
            sender.out_messages += 1
        elif argv[0] == 6:
            node.power = argv[1]
            node.duty_cycle = argv[2]
    collisions = 0
    timestamp = 0
    node_id = 0
    message = 0
    complete_timestamp = None
    is_over = False
    for timestamp, node_id, message in open_log(filename):
        if timestamp[0:2] == '30':
            is_over = True

        node = nodes[int(node_id[3:])]
        if node.is_sink():
            if 'complete' in message:
                complete_timestamp = timestamp
                break
            elif not is_over:
                if message[0].isdigit():
                    argv = list(map(int, message.split()))
                    print(argv)
                    nodes[1].sink_received = argv[3]
        if not is_over:
            if message[0].isdigit():
                _parse(node, timestamp, list(map(int, message.split())))
            if 'collision' in message.lower():
                collisions += 1
    total_power = sum(node.power for key, node in nodes.items())
    print('collisions : {}'.format(collisions))
    print('complete_timestamp: {}'.format(complete_timestamp))
    # print('total power: {}μJ'.format(total_power))
    fairness = get_fairness(nodes)
    print('max std of hop groups: {}'.format(max(fairness)))
    print('std of hop groups: {}'.format(fairness))
    message_sent = nodes[9].out_messages
    print('message sent: {}'.format(message_sent))
    print('message loss: {}'.format(message_sent - nodes[1].sink_received))
    print('dfrequency_sum: {}'.format(dfrequency_sum))
    save_dfrequency(filename, dfrequency)


if __name__ == '__main__':
    import sys
    parse(sys.argv[1])
