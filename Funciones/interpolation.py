import numpy as np
from scipy.sparse import csr_matrix


def apply_periodic_boundary_condition(
    variable: np.ndarray, 
    lower_bound: int, 
    upper_bound: int
    ) -> np.ndarray:
    """
    Apply periodic boundary conditions to the variable.
    
    Args:
        variable: Array of values to apply boundary conditions on.
        lower_bound: Lower boundary value.
        upper_bound: Upper boundary value.
    
    Returns:
        np.ndarray: Updated variable with applied boundary conditions.
    """
    below_lower_bound = variable < lower_bound
    variable[below_lower_bound] += upper_bound
    
    above_upper_bound = variable > upper_bound
    variable[above_upper_bound] -= upper_bound
    
    return variable

def interpolate_particles(
    method: str,
    grid_spacing: float,
    cell_size: float,
    num_grid_points: float,
    particle_positions: np.ndarray,
    num_particles: int,
    auxiliary_vector: np.ndarray
) -> csr_matrix:
    """
    Interpolates particle positions onto a grid using the specified interpolation method.

    Args:
        method: The interpolation method to use ('Nearest Grid Point (NGP)' or 'Cloud in Cell (CIC)').
        grid_spacing: Grid spacing (cell_size).
        num_grid_points: Total number of grid points (Ng).
        particle_positions: Array of positions of the particles.
        num_particles: Total number of particles.
        auxiliary_vector: Auxiliary array for building the sparse matrix.

    Returns:
        csr_matrix: Sparse matrix representing the interpolation.
    """
    if num_particles == 0:
        return csr_matrix((1, num_grid_points))  # Return a sparse matrix with zero elements

    # Project particles to grid
    first_node_indices = np.floor(particle_positions / grid_spacing).astype(int)  # First node
    second_node_indices = first_node_indices + 1  # Second node
    projected_indices = np.vstack((first_node_indices, second_node_indices))  # Concatenate nodes

    # Apply periodic boundary conditions on the projected indices
    projected_indices = apply_periodic_boundary_condition(projected_indices, 0, num_grid_points - 1)

    # Compute the fraction of particle size that lies on the two nearest cells
    fraction_in_first_node = 1 - np.abs((particle_positions / grid_spacing) - first_node_indices)  # Fraction in node i
    fraction_in_second_node = 1 - fraction_in_first_node  # Fraction in node i+1
    fractions = np.vstack((fraction_in_first_node, fraction_in_second_node))  # Concatenate fractions

    # Create interpolation matrix: shape (num_particles, num_grid_points)
    fractions[fractions > 0.5] = 1
    fractions[fractions < 0.5] = 0

    # Create sparse matrix: shape (num_particles, num_grid_points)
    interpolation_matrix = csr_matrix((fractions.flatten(), (auxiliary_vector, projected_indices.flatten())), shape=(num_particles, num_grid_points))

    return interpolation_matrix
