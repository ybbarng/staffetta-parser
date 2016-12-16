class Node:

    def __init__(self, node_id):
        self.node_id = node_id
        self.frequency = 10
        self.in_messages = 0
        self.out_messages = 0
        self.sink_received = 0
        self.power = 0
        self.duty_cycle = 0

    def is_sink(self):
        return self.node_id == 1
