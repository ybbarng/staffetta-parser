def open_log(filename):
    with open(filename) as f:
        while True:
            data = f.readline()
            if not data:
                break
            yield data.split('\t')


def parse(filename):
    timestamp = 0
    node_id = 0
    message = 0
    for timestamp, node_id, message in open_log(filename):
        print(node_id)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Staffetta Log Parser')
    parser.add_argument('filename', help='The name of a log file to be parsed')
    args = parser.parse_args()
    parse(args.filename)
