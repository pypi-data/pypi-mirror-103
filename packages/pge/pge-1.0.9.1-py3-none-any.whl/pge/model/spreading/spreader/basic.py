class SpreadingModel(object):
    def __init__(self, graph):
        self.graph = graph
        self.initial_status = {}

    def set_initial_status(self, configuration):
        return

    def init(self):
        return

    def iteration_bunch(self, num_iter):
        return

    def iteration_bunch_comm(self, num_iter, tick):
        return

    def iteration_bunch_complex(self, nodes):
        return

    def iteration_timer(self):
        return

    def finish(self, nodes=None):
        return True

    def iteration(self):
        return None, True
