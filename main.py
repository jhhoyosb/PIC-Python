import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

from interpolation import interpolate_particles
from motion_velocity import update_velocity
from motion_position import update_position
from periodic_boundary_conditions import apply_periodic_boundary_conditions

# Main simulation parameters
system_length: float = 64.0  
time_step: float = 0.1       
num_time_steps: int = 1000   
num_grid_points: int = 256   
num_beams: int = 2        

# Beam 1 parameters
num_particles_beam1: int = 10000
drift_velocity_beam1: float = 5.0
thermal_velocity_beam1: float = 1.0
charge_mass_ratio_beam1: float = -1.0

# Beam 2 parameters
num_particles_beam2: int = 10000
drift_velocity_beam2: float = -5.0
thermal_velocity_beam2: float = 1.0
charge_mass_ratio_beam2: float = -1.0

# Background ion parameters
num_background_ions: int = 20000

# Methods
motion_method: str = 'Leapfrog'
field_method: str = 'Finite Difference Method'
interpolation_method: str = 'Cloud in Cell'

# Grid and time setup
cell_size: float = system_length / num_grid_points  # Size of each cell
time_array: np.ndarray = np.arange(0, num_time_steps * time_step, time_step)  # Time array for the simulation

# Initialize particle positions and velocities for both beams
def initialize_particles(num_particles: int, drift_velocity: float, thermal_velocity: float):
    particle_positions = np.random.rand(num_particles) * system_length
    particle_velocities = np.random.normal(drift_velocity, thermal_velocity, num_particles)
    return particle_positions, particle_velocities

# Initialize particles for both beams
particle_positions_beam1, particle_velocities_beam1 = initialize_particles(num_particles_beam1, drift_velocity_beam1, thermal_velocity_beam1)
particle_positions_beam2, particle_velocities_beam2 = initialize_particles(num_particles_beam2, drift_velocity_beam2, thermal_velocity_beam2)

# Combine particles of both beams
all_particle_positions = np.concatenate((particle_positions_beam1, particle_positions_beam2))
all_particle_velocities = np.concatenate((particle_velocities_beam1, particle_velocities_beam2))

# Initialize the electric field and charge densities on the grid
electric_field: np.ndarray = np.zeros(num_grid_points)
charge_density: np.ndarray = np.zeros(num_grid_points)

# Auxiliary vector for sparse matrix creation
aux_vector: np.ndarray = np.arange(len(all_particle_positions))

# Main computational loop
for time_step_idx in range(num_time_steps):
    print(f"Time step: {time_step_idx + 1}/{num_time_steps}")

    # Debugging: Print the shapes and types of inputs for the interpolation
    print("Particle Positions Shape:", all_particle_positions.shape)
    print("Number of Particles:", len(all_particle_positions))
    print("Aux Vector Shape:", aux_vector.shape)

    # Interpolate particle positions to the grid
    try:
        interpolation_matrix = interpolate_particles(
            method=interpolation_method,
            num_grid_points=num_grid_points,
            cell_size=cell_size,
            particle_positions=all_particle_positions,
            num_particles=len(all_particle_positions),
            aux_vector=aux_vector
        )
        
        def interpolate_particles(
    method: str,
    grid_spacing: float,
    cell_size: float,
    num_grid_points: float,
    particle_positions: np.ndarray,
    num_particles: int,
    auxiliary_vector: np.ndarray
) -> csr_
        
    except Exception as e:
        print("Error during interpolation:", str(e))
        break

    # Update particle velocities for both beams
    try:
        all_particle_velocities = update_velocity(
            velocity=all_particle_velocities,
            charge_mass_ratio=charge_mass_ratio_beam1,  # Using beam 1's charge mass ratio for simplicity
            interpolation_matrix=interpolation_matrix,
            electric_field=electric_field,
            num_particles=len(all_particle_positions),
            method=motion_method,
            time_step=time_step
        )
        
        all_particle_velocities = update_velocity(
            velocity=all_particle_velocities,
            charge_mass_ratio=charge_mass_ratio_beam2,  # Using beam 2's charge mass ratio for simplicity
            interpolation_matrix=interpolation_matrix,
            electric_field=electric_field,
            num_particles=len(all_particle_positions),
            method=motion_method,
            time_step=time_step
        )
    except Exception as e:
        print("Error during velocity update:", str(e))
        break

    # Update particle positions
    try:
        all_particle_positions = update_position(
            position=all_particle_positions,
            velocity=all_particle_velocities,
            method=motion_method,
            time_step=time_step
        )
    except Exception as e:
        print("Error during position update:", str(e))
        break

    # Apply periodic boundary conditions to positions
    all_particle_positions = apply_periodic_boundary_conditions(
        variable=all_particle_positions,
        lower_bound=0,
        upper_bound=system_length
    )

    # Calculate charge density and electric field at grid points
    try:
        charge_density = np.histogram(all_particle_positions, bins=num_grid_points, range=(0, system_length))[0]
        electric_field = np.gradient(charge_density, cell_size)  # Ensure correct gradient calculation
    except Exception as e:
        print("Error during charge density or electric field calculation:", str(e))
        break

# Visualization of final particle positions
plt.figure(figsize=(10, 6))
plt.hist(all_particle_positions, bins=num_grid_points, range=(0, system_length), alpha=0.6, label='Particle Distribution')
plt.title('Final Particle Distribution')
plt.xlabel('Position')
plt.ylabel('Number of Particles')
plt.legend()
plt.grid()
plt.show()

# Visualization of charge density and electric field
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(charge_density, label='Charge Density')
plt.title('Charge Density on Grid')
plt.xlabel('Grid Points')
plt.ylabel('Charge Density')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(electric_field, label='Electric Field', color='orange')
plt.title('Electric Field from Charge Density')
plt.xlabel('Grid Points')
plt.ylabel('Electric Field')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

print("Simulation complete.")
