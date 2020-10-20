import pandas as pd

from utilities.constants import *


def save_full_experiment_data():
    if os.path.isfile(PATH):
        experiment_data = pd.read_csv(PATH)
        if os.path.isfile(FINAL_PATH):
            old_experiment_data = pd.read_csv(FINAL_PATH)
            experiment_data = experiment_data.drop(experiment_data.index[range(0,len(old_experiment_data))])
            experiment_data = old_experiment_data.append(experiment_data, ignore_index=True)
        os.remove(PATH)
        experiment_data.to_csv(FINAL_PATH, index=False)
