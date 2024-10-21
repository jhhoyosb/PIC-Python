import numpy as np

def update_position(
    position: np.ndarray, 
    velocity: np.ndarray, 
    method: str, 
    time_step: float
) -> np.ndarray:
    """
    Updates the position of particles based on the selected motion method.

    Args:
        position: Current position of particles.
        velocity: Current velocity of particles.
        method: Method for updating position ('Euler', 'Leapfrog', 'RK4').
        time_step: Time step for the update.

    Returns:
        np.ndarray: Updated position of particles.
    """
    if method == 'Euler':
        return position + velocity * time_step

    elif method == 'Leapfrog':
        return position + velocity * time_step

    elif method == 'RK4':
        k1 = velocity * time_step
        k2 = (velocity + 0.5 * k1) * time_step
        k3 = (velocity + 0.5 * k2) * time_step
        k4 = (velocity + k3) * time_step
        return position + (1/6) * (k1 + 2 * k2 + 2 * k3 + k4)
