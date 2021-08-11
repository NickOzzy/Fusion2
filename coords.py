import numpy as np
ne_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
te_vals = [100,200,300,400]
nene, tete = np.mgrid[ne_vals, te_vals]

print(np.vstack([nene.ravel(), tete.ravel()]))


