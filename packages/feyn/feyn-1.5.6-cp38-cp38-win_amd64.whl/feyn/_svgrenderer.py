
import itertools
import svgwrite
import io

class SVGRenderer:
    """Renders feyn graphs as SVG"""

    def layout_2d(graph):
        # This layout algo moves nodes to the latest layer possible (graphs are wide in the middle)
        lmap = {}
        layers = []
        out = graph[-1]
        layers.insert(0, [out])
        while True:
            layer = []
            for node in layers[0]:
                for ix in reversed(node.sources):
                    if ix!=-1:
                        pred = graph[ix]
                        if pred in lmap:
                            lmap[pred].remove(pred)

                        layer.append(pred)
                        lmap[pred] = layer

            if layer == []:
                break
            layers.insert(0,layer)

        locs = [None]*len(graph)
        for layer, interactions in enumerate(layers):
            sz = len(interactions)
            center = (sz-1) / 2
            for ix, interaction in enumerate(interactions):
                locs[interaction._index] = (layer, ix-center)

        return locs

    def layout_2d_simple(graph):
        # This layout algo moves nodes to the earliest layer possible (graphs are wide towards the beginning)
        layers = [list() for _ in range(graph.depth+2)]

        for node in graph:
            l = node.depth + 1
            layers[l].append(node)

        locs = [None]*len(graph)
        for layer, interactions in enumerate(layers):
            sz = len(interactions)
            center = (sz-1) / 2
            for ix, interaction in enumerate(interactions):
                locs[interaction._index] = (layer, ix-center)

        return locs



    @staticmethod
    def rendergraph(graph, label=None):
        from feyn.plots._svg_toolkit import SVGGraphToolkit
        gtk = SVGGraphToolkit()
        gtk.add_graph(graph, label=label)
        return gtk.render()


    @staticmethod
    def renderqgraph(graph):
        """
        Render an entire QGraph.
        """
        raise Exception("Not implemented")
