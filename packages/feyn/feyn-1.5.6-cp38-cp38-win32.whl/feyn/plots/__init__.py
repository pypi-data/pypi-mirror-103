"""
This module contains functions to help plotting evaluation metrics for feyn graphs and other models
"""

from ._plots import plot_confusion_matrix, plot_regression_metrics, plot_segmented_loss, plot_roc_curve, plot_goodness_of_fit, plot_residuals
from ._partial2d import plot_partial2d
from ._partial_dependence import plot_partial
from ._graph_summary import plot_graph_summary
from ._graph_flow import plot_activation_flow, plot_activation_flow_interactive
from ._set_style import abzu_mplstyle
from ._themes import Theme
from ._probability_plot import plot_probability_scores


__all__ = [
    'plot_confusion_matrix',
    'plot_regression_metrics',
    'plot_segmented_loss',
    'plot_roc_curve',
    'plot_partial2d',
    'plot_graph_summary',
    'plot_activation_flow',
    'plot_partial',
    'plot_probability_scores',
    'plot_goodness_of_fit',
    'plot_residuals',
    'Theme'
]
