import numpy as np

def update_velocity(
    velocity: np.ndarray, 
    charge_mass_ratio: float, 
    interpolation_matrix: np.ndarray, 
    electric_field: np.ndarray, 
    num_particles: int, 
    method: str, 
    time_step: float
) -> np.ndarray:
    """
    Updates the velocity of particles based on the selected motion method.

    Args:
        velocity: Current velocity of particles.
        charge_mass_ratio: Charge-to-mass ratio of the particles.
        interpolation_matrix: Matrix for interpolating the electric field.
        electric_field: Electric field at grid points.
        num_particles: Number of particles.
        method: Method for updating velocity ('Euler', 'Leapfrog', 'RK4').
        time_step: Time step for the update.

    Returns:
        np.ndarray: Updated velocity of particles.
    """
    if num_particles == 0:
        return np.zeros_like(velocity)

    if method == 'Euler':
        return velocity + charge_mass_ratio * interpolation_matrix.dot(electric_field) * time_step

    elif method == 'Leapfrog':
        return velocity + 0.5 * charge_mass_ratio * interpolation_matrix.dot(electric_field) * time_step

    elif method == 'RK4':
        k1 = charge_mass_ratio * interpolation_matrix.dot(electric_field) * time_step
        k2 = charge_mass_ratio * interpolation_matrix.dot(electric_field + 0.5 * k1) * time_step
        k3 = charge_mass_ratio * interpolation_matrix.dot(electric_field + 0.5 * k2) * time_step
        k4 = charge_mass_ratio * interpolation_matrix.dot(electric_field + k3) * time_step
        return velocity + (1/6) * (k1 + 2 * k2 + 2 * k3 + k4)
