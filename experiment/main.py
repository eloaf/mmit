import argparse
import itertools
import os

def generate():
    # function that generates cmdlines (i.e. calling "run" with the appropriate args)
    return


def run():
    # function that runs a test
    return


if __name__=="__main__":
    # parse args
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--datasets', type=str, nargs='+')

    args = parser.parse_args()

    datasets = args.datasets

    command_line = "features=%s targets=%s folds=%s max_features"

    for dataset in datasets:
        if os.path.isdir(dataset):
            print(dataset, os.listdir(dataset))
            #print("N=%s" % sum(1 for line in open(os.path.join(dataset, 'features.csv'))))
            #print("k=%s" % sum(1 for char in open(os.path.join(dataset, 'features.csv')).readline() if char==','))

            X_path = os.path.join(dataset, 'features.csv')
            y_path = os.path.join(dataset, 'targets.csv')
            fold_path = os.path.join(dataset, 'folds.csv')

            folds = set(int(x.strip()) for x in open(fold_path).readlines()[1: ])


            print(command_line % (X_path, y_path, fold_path))
