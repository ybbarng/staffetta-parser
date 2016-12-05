class Node:

    def __init__(self, node_id):
        self.node_id = node_id
        self.frequency = 0

    def on_message(self, timestamp, message):
        if message[0].isdigit():
            self.parse(timestamp, list(map(int, message.split())))

    def parse(self, timestamp, argv):
        if argv[0] == 2:
            self.on_ack(timestamp, *argv[1:])

    def on_ack(self, timestamp, sender_id, frequency):
        if self.node_id == 1:
            return
        print('Node {}: {} -> {}'.format(self.node_id, self.frequency, frequency))
        self.frequency = frequency
