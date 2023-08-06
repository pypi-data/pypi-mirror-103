"""Various helper functions to compute and plot metrics."""
import itertools

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import typing
import feyn.losses
import feyn.metrics

from ._themes import Theme

# Sets the default theme and triggers matplotlib stylings
Theme.set_theme()


def plot_confusion_matrix(y_true: typing.Iterable,
                          y_pred: typing.Iterable,
                          labels: typing.Iterable=None,
                          title:str='Confusion matrix',
                          color_map="feyn-primary",
                          ax=None) -> None:
    """
    Compute and plot a Confusion Matrix.

    Arguments:
        y_true -- Expected values (Truth)
        y_pred -- Predicted values
        labels -- List of labels to index the matrix
        title -- Title of the plot.
        color_map -- Color map from matplotlib to use for the matrix
        ax -- matplotlib axes object to draw to, default None
    Returns:
        [plot] -- matplotlib confusion matrix
    """
    if ax is None:
        ax = plt.gca()

    if labels is None:
        labels = np.union1d(y_pred,y_true)

    cm = feyn.metrics.confusion_matrix(y_true, y_pred)

    ax.set_title(title)
    tick_marks = range(len(labels))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(labels, rotation=45)

    ax.set_yticks(tick_marks)
    ax.set_yticklabels(labels)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color=Theme.color('light') if cm[i, j] > thresh else Theme.color('dark'))

    ax.set_ylabel('Expected')
    ax.set_xlabel('Predicted')

    img = ax.imshow(cm, interpolation='nearest', cmap=color_map)
    plt.colorbar(img, ax=ax)

    return ax


def plot_regression_metrics(y_true: typing.Iterable, y_pred: typing.Iterable, title:str="Regression metrics", ax=None ) -> None:
    """
    Plot metrics for a regression problem.

    The y-axis is the range of values in y_true and y_pred.

    The x-axis is all the samples, sorted in the order of the y_true.

    With this, you are able to see how much your prediction deviates from expected in the different prediction ranges.

    So, a good metric plot, would have the predicted line close and smooth around the predicted line.

    Normally you will see areas, where the predicted line jitter a lot scores worse against the test data there.


    Arguments:
        y_true -- Expected values (Truth).
        y_pred -- Predicted values.
        title -- Title of the plot.
        ax -- matplotlib axes object to draw to, default None

    Raises:
        ValueError: When y_true and y_pred do not have same shape
    """
    if ax is None:
        ax = plt.gca()

    if type(y_true).__name__ == "Series":
        y_true = y_true.values

    if type(y_pred).__name__ == "Series":
        y_pred = y_pred.values

    if (len(y_true) != len(y_pred)):
        raise ValueError('Size of expected and predicted are different!')

    sort_index = np.argsort(y_true)
    expected = y_true[sort_index]
    predicted = y_pred[sort_index]

    ax.set_title(title)
    ax.plot(expected, label='Expected')
    ax.plot(predicted, label='Predicted')
    ax.set_xticks([])
    ax.legend()

    return ax


def plot_segmented_loss(graph: feyn.Graph, data:typing.Iterable, by:typing.Optional[str] = None, loss_function="squared_error", title="Segmented Loss", ax=None) -> None:
    """
    Plot the loss by segment of a dataset.

    This plot is useful to evaluate how a model performs on different subsets of the data.

    Example:
    > qg = qlattice.get_regressor(["age","smoker","heartrate"], output="heartrate")
    > qg.fit(data)
    > best = qg[0]
    > feyn.plots.plot_segmented_loss(best, data, by="smoker")

    This will plot a histogram of the model loss for smokers and non-smokers separately, which can help evaluate wheter the model has better performance for euther of the smoker sub-populations.

    You can use any column in the dataset as the `by` parameter. If you use a numerical column, the data will be binned automatically.

    Arguments:
        graph -- The graph to plot.
        data -- The dataset to measure the loss on.
        by -- The column in the dataset to segment by.
        loss_function -- The loss function to compute for each segmnent,
        title -- Title of the plot.
        ax -- matplotlib axes object to draw to
    """

    if by is None:
        by=graph[-1].name

    bins, cnts, statistic = feyn.metrics.segmented_loss(graph, data, by, loss_function)

    if ax is None:
        ax = plt.gca()

    ax.set_title(title)

    ax.set_xlabel("Segmented by "+by)
    ax.set_ylabel("Number of samples")

    if type(bins[0]) == tuple:
        bins = [(e[0]+e[1])/2 for e in bins]
        w = .8 * (bins[1]-bins[0])
        ax.bar(bins, height=cnts, width=w)
    else:
        ax.bar(bins, height=cnts)

    ax2 = ax.twinx()
    ax2.set_ylabel("Loss")
    ax2.plot(bins, statistic, c=Theme.color('accent'), marker="o")
    ax2.set_ylim(bottom=0)

    return ax


def plot_roc_curve(y_true: typing.Iterable, y_pred: typing.Iterable,  show_thresholds=1, title:str="ROC curve", ax=None,**kwargs):
    """
    Plot a ROC curve for a classification graph.

    A receiver operating characteristic curve, or ROC curve, is an illustration of the diagnostic ability of a binary classifier. The method was developed for operators of military radar receivers, which is why it is so named.

    Arguments:
        y_true -- Expected values (Truth).
        y_pred -- Predicted values.
        show_thresholds -- The amount of intervals to color the ROC curve with regards to the threshold. Default is 1
        title -- Title of the plot.
        ax -- matplotlib axes object to draw to, default None

    Raises:
        ValueError: When y_true and y_pred do not have same shape
        Exception: When show_thresholds is not an integer
    """
    if type(show_thresholds) != int:
        raise Exception(f"show_thresholds must be a positive integer but {type(show_thresholds).__name__} was passed instead")
    if show_thresholds < 1:
        raise Exception(f"show_thresholds must be a positive integer but {show_thresholds} was passed instead")

    if ax is None:
        ax = plt.gca()

    import sklearn.metrics
    fpr, tpr, threshold = sklearn.metrics.roc_curve(y_true, y_pred)
    roc_auc = sklearn.metrics.auc(fpr, tpr)

    ax.set_title(title)

    if "label" in kwargs:
        kwargs["label"] += ' AUC = %0.2f' % roc_auc
    else:
        kwargs["label"] = 'AUC = %0.2f' % roc_auc

    if show_thresholds > 1:
        amounts, bins = np.histogram(threshold, range = (0,1), bins = show_thresholds)
        # Reverse bins to display solid lines and then dashed from left to right on plot
        amount_rev = amounts[::-1]
        bins_rev = bins[::-1]
        len_theme_cycle = len(Theme._get_current().cycle)

        for idx, up_thres in enumerate(bins_rev[:-1]):
            amount = amount_rev[idx]
            low_thres = bins_rev[idx+1]
            if amount == 0:
                continue
            else:
                values_in_bin = (threshold >= low_thres) & (threshold <= up_thres)
                # Include index from previous interval so lines join smoothly
                first_true_idx = np.where(values_in_bin == True)[0][0]
                if first_true_idx != 0:
                    values_in_bin[first_true_idx - 1] = True

                line_style = '-'
                # Switches to dots after running through cycle
                if idx >= len_theme_cycle:
                    line_style = ':'

                ax.plot(fpr[values_in_bin],
                        tpr[values_in_bin],
                        ls = line_style,
                        label = f'{low_thres: .2f} <= thres <= {up_thres: .2f}')
    else:
        ax.plot(fpr,tpr, **kwargs)

    ax.legend(loc = 'lower right')

    ax.plot([0, 1], [0, 1],'--', c=Theme.color('accent'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_ylabel('True Positive Rate')
    ax.set_xlabel('False Positive Rate')

    return ax

def plot_goodness_of_fit(y_true: typing.Iterable, y_pred: typing.Iterable, title:str="Actuals vs Predictions", ax=None):
    """ This plots this true values on the x-axis and the predicted values on the y-axis.
    On top of the plot is the line of equality y=x.
    The closer the scattered values are to the line the better the predictions.
    The line of best fit between y_true and y_pred is also calculated and plotted. This line should be close to the line y=x 

    Arguments:
        y_true {typing.Iterable} -- True values
        y_pred {typing.Iterable} -- Predicted values

    Keyword Arguments:
        title {str} -- (default: {"Actuals vs Predictions"})
        ax {AxesSubplot} -- (default: {None})

    Returns:
        AxesSubplot -- Scatter plot of y_pred and y_true with line of best fit and line of equality
    """
    from sklearn.linear_model import LinearRegression

    # We change to numpy array because sklearn linear regression isn't compatible with pandas Series
    if type(y_true).__name__ == 'Series':
        y_true = y_true.values

    if ax is None:
        fig, ax = plt.subplots()
    
    ax.scatter(y_true, y_pred)

    lin_reg = LinearRegression()
    lin_reg.fit(X=y_true.reshape(-1,1), y=y_pred)
    coef = lin_reg.coef_[0]
    bias = lin_reg.intercept_

    mini = np.min([np.min(y_true), np.min(y_pred)])
    maxi = np.max([np.max(y_true), np.max(y_pred)])

    min_max_pred = lin_reg.predict(X = np.array([mini,maxi]).reshape(-1,1))
    
    # Line of equality
    ax.plot([mini, maxi], [mini, maxi], ls='--', lw=1, label='line of equality')

    # Line of best fit of y_pred vs y_true
    ax.plot([mini, maxi], min_max_pred, ls='--', lw=1, label=f'best fit: {coef:.2f}X + {bias:.2f}')

    ax.set_title(title)
    ax.set_xlabel('Actuals')
    ax.set_ylabel('Predictions')
    ax.legend()

    return ax

def plot_residuals(y_true: typing.Iterable, y_pred: typing.Iterable, title:str="Residual plot", ax=None):
    """This plots the predicted values against the residuals (y_true - y_pred). 

    Arguments:
        y_true {typing.Iterable} -- True values
        y_pred {typing.Iterable} -- Predicted values

    Keyword Arguments:
        title {str} -- (default: {"Residual plot"})
        ax {[type]} -- (default: {None})

    Returns:
        AxesSubplot -- Scatter plot of residuals against predicted values
    """

    if ax is None:
        fig, ax = plt.subplots()

    residuals = y_true - y_pred

    ax.scatter(y_pred, residuals)
    ax.axhline(lw = 1, ls = '--')
    ax.set_title(title)
    ax.set_xlabel('Predictions')
    ax.set_ylabel('Residuals')

    return  ax