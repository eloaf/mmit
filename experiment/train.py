import argparse
import os
from mmit import RandomMaximumMarginIntervalForest, MaxMarginIntervalTree
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np


def interval_MSE(model, X, y_true):
    y_pred = model.predict(X)
    under = y_pred < y_true[:, 0]
    over = y_pred > y_true[:, 1]
    under_diff = y_pred - y_true[:, 0]
    over_diff = y_pred - y_true[:, 1]
    sqr_err = (under * under_diff + over * over_diff)**2
    sqr_err[np.isnan(sqr_err)] = 0 # inf * 0 = nan
    #return np.log10(np.mean(sqr_err))
    return -np.mean(sqr_err)


def main(features, targets, folds):

    forest_param_grid = {'n_estimators': [50],
                         'max_features': [0.01, 0.025, 0.05, 0.1, 0.25, 0.5],
                         'margin': [0, 0.01, 0.1, 1, 10],
                         'n_processes': [1],
                        }
    tree_param_grid = {'max_depth': list(range(3, 20)),
                       'margin': [0, 0.01, 0.1, 1, 10]}

    test_scores = []
    for fold_i in set(folds):
        print("Testing for fold %s" % fold_i)
        train_mask = folds != fold_i
        train_X, test_X = features[train_mask], features[~train_mask]
        train_y, test_y = targets[train_mask], targets[~train_mask]
        train_folds = folds[train_mask]

        tree_model = GridSearchCV(MaxMarginIntervalTree(),
                                  tree_param_grid,
                                  scoring=interval_MSE,
                                  cv=5,
                                  n_jobs=8)
        tree_model.fit(train_X, train_y)
        tree_test_score = interval_MSE(tree_model, test_X, test_y)
        test_scores.append(tree_test_score)
        print("Tree:   %s" % -tree_test_score)

        model = GridSearchCV(RandomMaximumMarginIntervalForest(),
                             forest_param_grid,
                             scoring=interval_MSE,
                             cv=5,
                             n_jobs=8)
        model.fit(train_X, train_y)
        test_score = interval_MSE(model, test_X, test_y)
        test_scores.append(test_score)
        print('Forest: %s' % -test_score)

if __name__=="__main__":
    # parse args
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dataset', type=str)
    args = parser.parse_args()

    features = os.path.join(args.dataset, 'features.csv')
    targets = os.path.join(args.dataset, 'targets.csv')
    folds = os.path.join(args.dataset, 'folds.csv')
    features, targets, folds = map(pd.read_csv, [features, targets, folds])

    main(features.values, targets.values, folds.values.flatten())
