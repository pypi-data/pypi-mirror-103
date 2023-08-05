from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

class BarcodePlot:
    """
    A BarcodePlot shows the persistance of features throughout a fitting process
    """
    def __init__(self):
        self.graph_features = []
    
    def add_graphs(self, graphs):
        """Add the graphs from a fitting loop to the plot state

        Arguments:
            graphs {List[feyn.Graph]} -- The graphs to add to the plot state, typically qgraph.best()
        """
        features = []
        for g in graphs:
            features.append(g.features)
        self.graph_features.append(features)
        
    def plot(self):
        """
        Plot the current state of BarcodePlot
        """
        features = self.graph_features
        feats_flat = [feature for feature_list in np.ravel(features) for feature in feature_list]
        epochs = len(features)
        unique_feats = np.unique(feats_flat)

        presence_matrix = np.zeros((len(unique_feats), epochs))
        xy = dict(zip(unique_feats, presence_matrix))
        
        for i in range(epochs):
            for key, value in dict(Counter([feat for graph in features[i] for feat in graph])).items():
                xy[key][i] = value
        
        fig, ax = plt.subplots(figsize = (20,len(xy.keys())))

        for ix, key in enumerate(xy):
            for epoch in range(epochs):
                ax.plot([epoch, epoch+1], [ix,ix], c = 'k', lw=xy[key][epoch])

        ax.set_yticks(range(len(xy)))
        ax.set_xticks(range(epochs))
        ax.set_yticklabels(xy.keys())
        plt.show()