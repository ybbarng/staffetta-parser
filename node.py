from collections import Counter


class Node:

    def __init__(self, node_id):
        self.node_id = node_id
        self.frequency = 10
        self.collisions = Counter()
        self.messages = []

    def on_message(self, timestamp, message):
        self.messages.append((timestamp, message))
        if message[0].isdigit():
            self.parse(timestamp, list(map(int, message.split())))
        if 'collision' in message.lower():
            self.on_collision(timestamp)

    def parse(self, timestamp, argv):
        if argv[0] == 2:
            self.on_ack(timestamp, *argv[1:])

    def on_ack(self, timestamp, sender_id, frequency):
        if self.node_id == 1:
            return
        print('Node {}: {} -> {}'.format(self.node_id, self.frequency, frequency))
        self.frequency = frequency

    def on_collision(self, timestamp):
        self.collisions[self.frequency] += 1

    def get_collisions(self):
        return self.collisions

    def print_messages(self):
        print('Messages of Node {}'.format(self.node_id))
        for message in self.messages:
            print(message)
