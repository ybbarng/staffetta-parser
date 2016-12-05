class Node:

    def __init__(self, node_id):
        self.node_id = node_id
        self.messages = []

    def on_message(self, timestamp, message):
        self.messages.append((timestamp, message))

    def print_messages(self):
        print('Messages of node {}'.format(self.node_id))
        for message in self.messages:
            print(message)
