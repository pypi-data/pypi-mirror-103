import numpy as np
import matplotlib.pyplot as plt

def feat_freq_matrix(graphs, minimum = 0, density = False):
    """This takes a list of graphs and returns an N x N matrix where N is the amount of different features used in the list of graphs.
    Along the diagonal is the amount of graphs the feature occurs in the list.
    At the i-th, j-th position is the amount of graphs both features occur in a graph

    Arguments:
        graphs {[type]} -- List of graphs

    Keyword Arguments:
        minimum {float} -- Do not show features that occur than minimum amount of times.
        Can be a count or a fraction of the total amount of graphs (default: {0})
        density {bool} -- Show proportion of amount of graphs instead of count (default: {False})

    Returns:
        [DataFrame] -- Returns matrix of feature frequency
    """
    import pandas as pd
    
    feats_in_graphs = [graph.features for graph in graphs]
    feats_uniq = list(np.unique([feat for features in feats_in_graphs for feat in features]))
    
    freq_mat = np.zeros((len(feats_uniq),len(feats_uniq)))

    for i,feat in enumerate(feats_uniq):
        freq = freq_mat[i]
        for idx, int_feat in enumerate(feats_uniq):
            for graph_feats in feats_in_graphs:
                if (int_feat in graph_feats) and  (feat in graph_feats):
                     freq[idx] += 1
    
    freq_mat = pd.DataFrame(freq_mat, columns=feats_uniq, index=feats_uniq)
    
    if minimum >=1:
        for column in freq_mat.columns:
            if freq_mat.loc[column, column] < minimum:
                freq_mat = freq_mat.drop([column]).drop([column], axis=1)
                
    if (minimum < 1) and (minimum > 0):
        for column in freq_mat.columns:
            if freq_mat.loc[column, column] < minimum * len(graphs):
                freq_mat = freq_mat.drop([column]).drop([column], axis=1)
            
    if density:
        freq_mat = freq_mat / len(graphs)        
                        
    return freq_mat

def feat_freq_heatmap(freq_df, figsize = (10,10), ax=None, show_text=True):
    """Shows a heat map of the feature frequence matrix

    Arguments:
        freq_df {DataFrame} -- feature frequency matrix

    Keyword Arguments:
        figsize {tuple} -- [description] (default: {(10,10)})
        ax {[type]} -- [description] (default: {None})
        show_text {bool} -- [description] (default: {True})

    Returns:
        Axes.subplot -- Heat map of feature frequence matrix
    """

    if ax is None:
        fig, ax = plt.subplots(figsize = figsize)

    im = ax.imshow(freq_df, cmap = 'feyn-primary')
    ax.figure.colorbar(im, ax=ax)

    ax.set_xticks(range(len(freq_df.columns)))
    ax.set_yticks(range(len(freq_df.columns)))

    ax.set_xticklabels(freq_df.columns)
    ax.set_yticklabels(freq_df.columns)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    if show_text:
        for i in range(len(freq_df.columns)):
            for j in range(len(freq_df.columns)):
                text = ax.text(j, i, round(freq_df.iloc[i, j],2),
                            ha="center", va="center")

    ax.set_title("Frequence of features in the same graph")

    fig.tight_layout()
    plt.show()

    return ax
