import glob
import os
import re, string
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from sklearn.metrics import confusion_matrix

# if 1 (stressed): '/'
# if 0 (unstressed): 'x'

y_true = ['/', 'x', '/', 'x', '/', 'x', '/', '/', 'x']
y_pred = ['x', '/', '/', 'x', '/', 'x', 'x', 'x', '/']

array = confusion_matrix(y_true, y_pred)
print(array)

