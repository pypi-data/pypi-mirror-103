

class QueueLib(object):
    def __init__(self):
        pass

    def add_message_to_queue(self, queue, msg):
        queue.append(msg)

    def delete_message_from_queue(self, queue, msg):
        queue.remove(msg)

    def clear_message_queue(self, queue):
        queue.clear()
