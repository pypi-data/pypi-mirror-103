import numpy as np
import feyn

from typing import Iterable, Optional

from feyn.plots._svg_toolkit import SVGGraphToolkit


def _get_min_max(graph, data, samples=10000):
    # Magic support for pandas DataFrame
    if type(data).__name__ == "DataFrame":
        data = {col: data[col].values for col in data.columns}

    samples = min(len(next(iter(data.values()))), samples)

    permutation = np.random.permutation(samples)
    data = {key: values[permutation] for key, values in data.items()}

    minval, maxval = 0, 0
    for i in range(samples):
        sample = {key: values[i:i+1] for key, values in data.items()}
        _ = graph.predict(sample)
        gmin, gmax = min([node.activation[0] for node in graph]), max([node.activation[0] for node in graph])
        minval = min(gmin, minval)
        maxval = max(gmax, maxval)

    return minval, maxval


def plot_activation_flow(graph:feyn.Graph, data:Iterable, sample:Iterable): # -> "SVG":
    """
    Plot a graph displaying the flow of activations.

    Arguments:
        graph {feyn.Graph}   -- A feyn.Graph we want to describe given some data.
        sample {Iterable} - The sample you want to visualize
        data {Iterable} -- A Pandas DataFrame or dict of numpy arrays to compute on.

    Returns:
        SVG -- SVG of the graph summary.
    """

    gtk = SVGGraphToolkit()

    # NOTE: Consider doing range [0,1] for classification
    # and min/max of prediction for regression to keep colors focused on output
    minmax = _get_min_max(graph, data)

    graph.predict(sample)
    activations = [np.round(node.activation[0], 2) for node in graph]

    gtk.add_graph(graph, label='Displaying activation of individual nodes')
    gtk.label_nodes(activations)
    gtk.color_nodes(by=activations, crange=minmax)
    gtk.add_colorbars(label='Activation strength')

    from IPython.display import HTML
    return HTML(gtk._repr_html_())


def plot_activation_flow_interactive(graph, data):
    """
    EXPERIMENTAL: For IPython kernels only.
    Interactively plot a graph displaying the flow of activations.

    Requires installing ipywidgets, and enabling the extension in jupyter notebook or jupyter lab.
    Jupyter notebook: jupyter nbextension enable --py widgetsnbextension
    Jupyter lab: jupyter labextension install @jupyter-widgets/jupyterlab-manager

    Arguments:
        graph {feyn.Graph} -- A feyn.Graph we want to describe given some data.
        data {Iterable} -- A Pandas DataFrame or dict of numpy arrays to compute on.

    Returns:
        SVG -- SVG of the graph summary.
    """
    import ipywidgets as widgets
    features = graph.features
    ranges = {}
    for i in graph:
        if i.name in features:
            name = i.name
            if 'cat' in i.spec:
                ranges[name] = data[name].unique()
            else:
                ranges[name] = (data[name].min(), data[name].max())

    def flow(**kwargs):
        for key in kwargs:
            kwargs[key] = np.array([kwargs[key]])
        return feyn.plots.plot_activation_flow(graph, data, kwargs)

    return widgets.interact(flow, **ranges)
