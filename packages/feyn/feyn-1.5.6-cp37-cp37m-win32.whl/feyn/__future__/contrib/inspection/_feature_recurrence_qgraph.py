import typing
import os
import numpy as np
import pandas as pd
from feyn.filters import MaxEdges


def feature_recurrence_qgraph(data, target, qlattice,
                              get_qgtype='regressor', n_features=1,
                              n_splits=5, test_size=0.333, split_seeds=[],
                              n_loops=10, top_graphs=10, ql_seed=None,
                              stypes:typing.Optional[str]=None, filters=[],
                              threads=6, file_name=None, overwrite=False):
    """Uses the QLattice to extract simple models and
    check which features are the most recurring.
    Arguments:
        data {pd.DataFrame} -- dataset
        target {str} -- target name
        qlattice {feyn.QLattice} -- the QLattice
    Keyword Arguments:
        get_qgtype {str} -- type of qgraph (default: {'regressor'})
        n_features {int} -- max number of features, between 1 and 4 (default: {1})
        n_splits {int} -- number of distinct train-test splits (default: {5})
        test_size {float} -- fraction of data that becomes the test set (default: {0.333})
        split_seeds {array_like} -- list of random seeds to be given to each split (default: {[]})
        n_loops {int} -- number of updating loops (default: {10})
        top_graphs {int} -- number of inspected graphs (default: {10})
        ql_seed {int} -- seed for the QLattice (default: {None})
        filters {array_like} -- list of filters to apply (default: {[]})
        threads {int} -- number of threads (default: {6})
        file_name {str} -- name of file where results will be writen (default: {None})
        overwrite {bool} -- whether or not to overwrite the given file (default: {False})

    Returns:
        DataFrame that records in features in the top graphs from each train-test split
    """

    from sklearn.model_selection import train_test_split

    if n_features < 1 or n_features > 4:
        raise Exception("Number of features must be between 1 and 4!")
    configurations = {
        1: {'max_depth': 1, 'max_edges': 2},
        2: {'max_depth': 1, 'max_edges': 3},
        3: {'max_depth': 2, 'max_edges': 6},
        4: {'max_depth': 2, 'max_edges': 7}
    }
    max_depth = configurations[n_features]['max_depth']
    max_edges = configurations[n_features]['max_edges']

    if not np.any(split_seeds):
        split_seeds = np.random.randint(0, 1000000, size=n_splits)
    elif len(split_seeds) != n_splits:
        raise Exception("The number of random seeds given to the train-test split must\
                        be equal to n_splits!")

    if ql_seed is None:
        ql_seed = -1

    if stypes is None:
        stypes = {}

    res_dict = {'n_split': [],
                'n_graph': [],
                'n_features': [],
                'features': [],
                'graph_loss': [],
                'metric_score_train': [],
                'metric_score_test': []}

    if file_name:
        if os.path.exists(file_name) and overwrite is False:
            out_file = open(file_name, 'a')
        else:
            out_file = open(file_name, 'w')
        out_file.write('QLattice seed: %d\n' % ql_seed)
        for key in res_dict.keys():
            out_file.write('%s\t' % key)
        out_file.write('\n')
    else:
        out_file = None

    for i in range(n_splits):
        qlattice.reset(ql_seed)

        if get_qgtype == 'regressor':
            train, test = train_test_split(data,
                                           test_size=test_size,
                                           random_state=split_seeds[i])
            qgraph = qlattice.get_regressor(data.columns,
                                            target,
                                            max_depth=max_depth,
                                            stypes=stypes)
            loss_function = 'squared_error'
            if not len(filters) == 0:
                for f in filters:
                    qgraph = qgraph.filter(f)
        elif get_qgtype == 'classifier':
            train, test = train_test_split(data,
                                           test_size=test_size,
                                           stratify=data[target],
                                           random_state=split_seeds[i])
            qgraph = qlattice.get_classifier(data.columns,
                                             target,
                                             max_depth=max_depth,
                                             stypes=stypes)
            loss_function = 'binary_cross_entropy'
            if not len(filters) == 0:
                for f in filters:
                    qgraph = qgraph.filter(f)
        else:
            raise Exception("QGraph type error: please choose get_type to be \
                either regressor or classifier!")

        qgraph = qgraph.filter(MaxEdges(max_edges))
        for _ in range(n_loops):
            qgraph.fit(train, threads=threads, loss_function=loss_function)
            best_graphs = qgraph.best()
            qlattice.update(best_graphs)
        # After going through the full update loop,
        # we go through the top 10 graphs

        for ix, g in enumerate(qgraph.best()[:top_graphs]):

            if get_qgtype == 'regressor':
                metric_score_train = g.r2_score(train)
                metric_score_test = g.r2_score(test)
            elif get_qgtype == 'classifier':
                metric_score_train = g.roc_auc_score(train)
                metric_score_test = g.roc_auc_score(test)
            else:
                metric_score_train = None
                metric_score_test = None

            res_dict['n_split'].append(i)
            res_dict['n_graph'].append(ix)
            res_dict['n_features'].append(len(g.features))
            res_dict['features'].append(g.features)
            res_dict['graph_loss'].append(g.loss_value)
            res_dict['metric_score_train'].append(metric_score_train)
            res_dict['metric_score_test'].append(metric_score_test)

        if out_file:
            for i in range(top_graphs):
                for key in res_dict.keys():
                    value = res_dict[key][-top_graphs:][i]
                    if type(value) == str or hasattr(value, '__len__'):
                        out_file.write('%s\t' % value)
                    elif type(value) == int:
                        out_file.write('%d\t' % value)
                    else:
                        out_file.write('%6e\t' % value)
                out_file.write('\n')

    if out_file:
        out_file.close()

    res_df = pd.DataFrame(res_dict)

    return res_df
