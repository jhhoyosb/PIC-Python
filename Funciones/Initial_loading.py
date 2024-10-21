# initial_loading.py
import numpy as np

def load_initial_conditions(
    num_particles: int,
    drift_velocity: float, 
    thermal_velocity: float, 
    perturbation_amplitude: float,
    mode: int, 
    system_length: float) -> tuple:
    
    positions = np.linspace(0, system_length - system_length / num_particles, num_particles)
    velocities = thermal_velocity * np.random.randn(num_particles) + drift_velocity  # Maxwellian distribution
    
    if perturbation_amplitude != 0:
        positions += perturbation_amplitude * np.cos(2 * np.pi * mode * positions / system_length)
        
    return positions, velocities
