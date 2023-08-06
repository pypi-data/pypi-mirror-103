import fiddler as fdl

import pandas as pd

import pandas as pd
import pathlib
import shutil
import yaml
import random
import pickle
import numpy as np

import fiddler as fdl


df = pd.read_csv('./test-space/logreg-all-e2e-events.csv')
df.to_pickle("./test-space/logreg-all-e2e-events.pkl")


print(df)
