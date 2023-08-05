import numpy as np
import networkx as nx


class BasicGrowth:
    def __init__(self, graph, schema, deg, model_param):
        self.gr = graph
        self.deg = deg
        self.schema = schema
        self.param = model_param

    def choice(self, gr, sz):
        return []

    def new_edge_add(self, gr, attrs):
        return

    def new_node_add(self, graph, to, tp, attrs):
        return

    def prep(self, graph):
        return graph

    def proceed(self, n, save=None, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        nx.set_node_attributes(nw_graph.get_nx_graph(), 0, name=attr)
        nx.set_edge_attributes(nw_graph.get_nx_graph(), 0, name=attr)
        nw_graph = self.new_load(nw_graph)

        count = self.gr.size()
        for _ in np.arange(n):
            print(_)
            if self.stop():
                break

            nw_graph = self.prep(nw_graph)
            new_node = np.random.choice(len(self.schema), p=self.schema)
            if new_node == 1:
                self.new_edge_add(nw_graph, (attr, _))
            else:
                self.new_node_add(nw_graph, str(count), new_node, (attr, _))
                count += 1
        if save is None:
            return nw_graph
        else:
            self.save(nw_graph, save)

    def save(self, gr, to):
        nx.write_graphml(gr.get_nx_graph(), to + ".graphml")

    def new_load(self, gr):
        return gr

    def stop(self):
        return False


class BDiGrowth(BasicGrowth):
    def new_node_add(self, graph, to, tp, attrs):
        if tp == 0:
            if self.deg[0][0] == "const":
                nodes = self.choice(graph, self.deg[0][1], tp="in")
            else:
                nodes = self.choice(graph, self.deg[0][0](self.deg[0][1]), tp="in")

            for node in nodes:
                graph.add_edge(to, node, {attrs[0]: attrs[1] + 1})
        else:
            if self.deg[1][0] == "const":
                nodes = self.choice(graph, self.deg[1][1], tp="out")
            else:
                nodes = self.choice(graph, self.deg[1][0](self.deg[1][1]), tp="out")

            for node in nodes:
                graph.add_edge(node, to, {attrs[0]: attrs[1] + 1})
        graph.set_attr(to, attrs[0], attrs[1] + 1)

    def new_edge_add(self, gr, attrs):
        node1, node2 = self.choice(gr, 1, tp="out")[0], self.choice(gr, 1, tp="in")[0]
        gr.add_edge(node1, node2, {attrs[0]: attrs[1] + 1})

    def choice(self, gr, sz, tp="in"):
        return []


class BUnGrowth(BasicGrowth):
    def new_node_add(self, graph, to, tp, attrs):
        if self.deg[0] == "const":
            nodes = self.choice(graph, self.deg[1])
        else:
            nodes = self.choice(graph, self.deg[0](self.deg[1]))

        for node in nodes:
            graph.add_edge(to, node, {attrs[0]: attrs[1] + 1})
        graph.set_attr(to, attrs[0], attrs[1] + 1)

    def new_edge_add(self, gr, attrs):
        nodes = self.choice(gr, 2)
        gr.add_edge(nodes[0], nodes[1], {attrs[0]: attrs[1] + 1})
