import numpy as np

def charge_density(charge, interp, cell_size):
    rho = (charge / cell_size) * np.sum(interp)
    return rho
