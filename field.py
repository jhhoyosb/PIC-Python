import numpy as np
from scipy.fft import fft, ifft
from scipy.linalg import solve

def compute_electric_field(
    method: str, 
    charge_density: np.ndarray, 
    num_grid_points: int, 
    spatial_step: float, 
    domain_length: float, 
    matrix_A: np.ndarray = None, 
    wave_numbers: np.ndarray = None
) -> tuple:
    """
    Calculate the electric potential (Phi) and the electric field (Eg) 
    using different numerical methods.

    Args:
        method: The method to use ('Finite Difference Method', 'FFT', or 'Direct Integration').
        charge_density: The charge density array.
        num_grid_points: Number of grid points (Ng).
        spatial_step: Spatial step size (dx).
        domain_length: Length of the domain (L).
        matrix_A: Matrix for solving the system in Finite Difference Method.
        wave_numbers: Array for wave numbers in FFT method.

    Returns:
        tuple: Phi (electric potential) and Eg (electric field).
    """
    if method == 'Finite Difference Method':
        # Solve for electric potential using finite difference method
        electric_potential = solve(matrix_A, -charge_density[:num_grid_points - 1] * spatial_step**2)
        electric_potential = np.append(electric_potential, 0)  # Append zero at the end
        
        # Compute electric field (Eg) using central differences
        electric_field = (np.roll(electric_potential, 1) - np.roll(electric_potential, -1)) / (2 * spatial_step)
        electric_field[0] = (electric_potential[num_grid_points - 1] - electric_potential[1]) / (2 * spatial_step)
        electric_field[-1] = (electric_potential[num_grid_points - 2] - electric_potential[0]) / (2 * spatial_step)

    elif method == 'Fast Fourier Transform (FFT)':
        # Compute Fourier transform of the charge density
        charge_density_k = fft(charge_density[:num_grid_points])
        
        # Solve in Fourier space for electric potential (Phi)
        potential_k = charge_density_k / wave_numbers**2
        electric_potential = np.real(ifft(potential_k))
        electric_potential[num_grid_points - 1] = 0  # Set last element to zero
        
        # Compute electric field (Eg) in Fourier space and transform back
        electric_field_k = -1j * wave_numbers * potential_k
        electric_field = np.real(ifft(electric_field_k))

    elif method == 'Direct Integration':
        # Initialize variables for integration
        G1 = np.zeros(num_grid_points)
        initial_integral = (charge_density[0] + charge_density[num_grid_points - 1]) * spatial_step / 2
        G1[0] = initial_integral

        # Compute G1 by integrating charge density
        for k in range(1, num_grid_points):
            initial_integral += (charge_density[k] + charge_density[k - 1]) * spatial_step / 2
            G1[k] = initial_integral

        F1 = np.zeros(num_grid_points)
        initial_integral_F = (G1[0] + G1[-1]) * spatial_step / 2
        F1[0] = initial_integral_F

        # Compute F1 by integrating G1
        for k in range(1, num_grid_points):
            initial_integral_F += (G1[k] + G1[k - 1]) * spatial_step / 2
            F1[k] = initial_integral_F

        # Calculate the derivative of potential and the electric field
        potential_prime = (1 / domain_length) * F1[-1]
        electric_field = -potential_prime + G1

        # Integrate electric field to get electric potential
        electric_potential = np.zeros(num_grid_points)
        initial_integral_phi = (electric_field[0] + electric_field[-1]) * spatial_step / 2
        electric_potential[0] = -initial_integral_phi

        for k in range(1, num_grid_points):
            initial_integral_phi += (electric_field[k] + electric_field[k - 1]) * spatial_step / 2
            electric_potential[k] = -initial_integral_phi

    return electric_potential, electric_field
