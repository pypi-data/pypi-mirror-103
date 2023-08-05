"""
This module contains functions to help evaluate and compare feyn graphs and other models.
"""

from ._mutual import calculate_mi
from ._linear import calculate_pc
from ._metrics import accuracy_score, accuracy_threshold, roc_auc_score, r2_score, rmse, mae, mse, confusion_matrix, segmented_loss, get_summary_metrics_classification, get_summary_metrics_regression, precision_recall, get_pearson_correlations, get_mutual_information, get_spearmans_correlations, get_summary_information
from ._pvalues import p_value, plot_p_value
from ._spearman import calculate_spear

__all__ = [
    'accuracy_score',
    'accuracy_threshold',
    'calculate_mi',
    'calculate_pc',
    'calculate_spear',
    'r2_score',
    'mae',
    'mse',
    'rmse',
    'confusion_matrix',
    'segmented_loss',
    'get_summary_metrics_classification',
    'get_summary_metrics_regression',
    'precision_recall',
    'p_value',
    'plot_p_value',
    'roc_auc_score'
]
