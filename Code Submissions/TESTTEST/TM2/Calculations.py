# from scipy import stats as st
# a = 1 - st.poisson(5, 1.8)
# print(a)

import numpy as np

X=np.array([[1,0],[0,1]])
Y=np.array([[2,1],[1,2]])
Z=np.dot(X,Y)
print(Z)