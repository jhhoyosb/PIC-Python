import numpy as np

def apply_periodic_boundary_conditions(variable: np.ndarray, lower_bound: float, upper_bound: float) -> np.ndarray:
    """
    Apply periodic boundary conditions to the given variable.

    Args:
        variable: Array of values to adjust.
        lower_bound: Lower boundary value.
        upper_bound: Upper boundary value.

    Returns:
        np.ndarray: The adjusted variable with periodic boundary conditions applied.
    """
    # If values are less than the lower bound, add the upper bound.
    variable[variable < lower_bound] += (upper_bound - lower_bound)
    # If values are greater than the upper bound, subtract the upper bound.
    variable[variable > upper_bound] -= (upper_bound - lower_bound)
    
    return variable
