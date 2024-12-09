import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append('funzioni.py')
import funzioni as fu

X_st = pd.read_csv('/202302/observed_starX.csv')
print(X_st.columns)
