import numpy as np
import feyn

from typing import Iterable, Optional

from feyn.plots._svg_toolkit import SVGGraphToolkit
from feyn.metrics import get_pearson_correlations, get_mutual_information, get_spearmans_correlations, get_summary_information

def plot_graph_summary(graph:feyn.Graph, dataframe:Iterable, corr_func:Optional[str]=None, test:Optional[Iterable]=None): # -> "SVG":
    """
    Plot a graph displaying the signal path and summary metrics for the provided feyn.Graph and DataFrame.

    Arguments:
        graph {feyn.Graph}   -- A feyn.Graph we want to describe given some data.
        dataframe {Iterable} -- A Pandas DataFrame for showing metrics.

    Keyword Arguments:
        corr_func {Optional[str]} -- A name for the correlation function to use as the node signal, either 'mi', 'pearson' or 'spearmans' are available. (default: {None} defaults to 'pearson')
        test {Optional[Iterable]} -- A Pandas DataFrame for showing additional metrics. (default: {None})

    Raises:
        ValueError: Raised if the name of the correlation function is not understood.

    Returns:
        SVG -- SVG of the graph summary.
    """
    if corr_func is None:
        corr_func = 'pearson'

    gtk = SVGGraphToolkit()

    if corr_func == "mi":
        # Default to mutual information
        signal_func = get_mutual_information
        legend = "Mutual Information"
    elif corr_func == "pearson":
        signal_func = get_pearson_correlations
        legend = "Pearson correlation"
    elif corr_func == 'spearmans':
        signal_func = get_spearmans_correlations
        legend = "Spearman's correlation"
    else:
        raise ValueError("Correlation function name not understood.")

    node_signal = signal_func(graph, dataframe)

    if corr_func == 'mi':
        # TODO: What does negative MI imply, and how do we communicate it?
        node_signal = np.abs(node_signal)
        color_range = node_signal
        cmap = 'feyn-highlight'
        colorbar_labels = ['low', 'high']
    elif (corr_func == 'pearson') or (corr_func == 'spearmans'):
        color_range = [-1, 1]
        cmap = 'feyn-diverging'
        colorbar_labels = ['-1', '0', '+1']

    summary = get_summary_information(graph, dataframe)

    gtk.add_graph(graph, show_loss=False) \
        .color_nodes(by=node_signal, crange=color_range, cmap=cmap)\
        .label_nodes([np.round(sig, 2) for sig in node_signal])\
        .add_colorbars(legend, color_text=colorbar_labels, cmap=cmap)\
        .add_summary_information(summary, "Metrics")

    if test is not None:
        test_summary = get_summary_information(graph, test)
        gtk.add_summary_information(test_summary, "Test Metrics")

    from IPython.display import HTML
    return HTML(gtk._repr_html_())
