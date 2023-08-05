import numpy as np

from pge.model.growth.pa import PADiGrowth
from pge.model.spreading.spreader.basic import SpreadingModel


class PADirSpread(PADiGrowth, SpreadingModel):
    def __init__(self, graph, schema, deg, model_param, rs):
        super().__init__(graph, schema, deg, model_param)
        self.received = {str(node): 1 for node in graph.get_ids()}
        self.n = 0
        self.rs = rs

    def stop(self):
        return self.rs == self.n - self.gr.size()

    def new_node_add(self, graph, to, tp, attrs):
        super().new_node_add(graph, to, tp, attrs)

        self.received.update({to: int(tp == 2)})
        self.n += int(tp == 2)

    def new_edge_add(self, gr, attrs):
        node1, node2 = self.choice(gr, 1, tp="out")[0], self.choice(gr, 1, tp="in")[0]
        gr.add_edge(node1, node2, {attrs[0]: attrs[1] + 1})

        if self.received[str(node1)] == 1:
            self.n += int(self.received[str(node2)] != 1)
            self.received.update({str(node2): 1})

    def new_load(self, gr):
        self.n = self.gr.size()
        return gr

    def iteration_bunch(self, num_iter):
        times = []

        for _ in np.arange(num_iter):
            gr = self.proceed(self.rs*10000)
            times.append(gr.size_edge()-self.gr.size_edge())
        return times

