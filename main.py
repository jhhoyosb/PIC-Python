import numpy as np
import matplotlib.pyplot as plt

# Parameters
length_of_system = 64
dt = 0.1
plasma_frequency = 1
iterations_number = 10
final_time = iterations_number * dt
grid_points = 256
number_of_beams = 2

# Beam 1
number_of_particles_in_beam1 = 10000
drift_velocity_beam1 = 5
thermal_velocity_beam1 = 1
charge_mass_relation_beam1 = -1
perturbation_amplitude_beam_1 = 0
mode_beam1 = 0

# Beam 2
number_of_particles_in_beam2 = 10000
drift_velocity_beam2 = -5
thermal_velocity_beam2 = 1
charge_mass_relation_beam2 = -1
perturbation_amplitude_beam_2 = 0
mode_beam2 = 0

# Ions in the background
number_of_background_ions = 20000

# Size of the cell
dx = length_of_system / grid_points
time = np.arange(0, final_time + dt, dt)

# Charge
def Charge(QM1, QM2, IB, N1, N2, L, WP):
    Q1 = QM1 * N1
    Q2 = QM2 * N2
    rho_back = IB / L
    return Q1, Q2, rho_back

Q1, Q2, rho_back = Charge(charge_mass_relation_beam1, charge_mass_relation_beam2, number_of_background_ions, number_of_particles_in_beam1, number_of_particles_in_beam2, length_of_system, 1)

# Initial loading
def InitialLoading(N, V0, Vth, XP, Mode, L):
    xp = np.random.uniform(0, L, N)
    vp = np.random.normal(V0, Vth, N)
    return xp, vp

xp1, vp1 = InitialLoading(number_of_particles_in_beam1, drift_velocity_beam1, thermal_velocity_beam1, perturbation_amplitude_beam_1, mode_beam1, length_of_system)
xp2, vp2 = InitialLoading(number_of_particles_in_beam2, drift_velocity_beam2, thermal_velocity_beam2, perturbation_amplitude_beam_2, mode_beam2, length_of_system)

# Auxiliarity vectors
def AuxVector(N):
    return np.arange(N)

p1 = AuxVector(number_of_particles_in_beam1)
p2 = AuxVector(number_of_particles_in_beam2)
