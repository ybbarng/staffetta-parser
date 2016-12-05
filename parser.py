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


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Staffetta Log Parser')
    parser.add_argument('filename', help='The name of a log file to be parsed')
    args = parser.parse_args()
    parse(args.filename)
