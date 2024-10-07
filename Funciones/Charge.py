def charge(
    charge_mass_beam1: float,
    charge_mass_beam2: float,
    number_of_background_ions: int,
    number_of_particles_in_beam1: int,
    number_of_particles_in_beam2: int,
    length_of_system: float,
    plasma_frequency: float
    ):
    q_1 = (plasma_frequency**2 * length_of_system) / (number_of_particles_in_beam1 * charge_mass_beam1)
    if charge_mass_beam2 > 0:
        charge_mass_beam2 = -q_1 * (number_of_particles_in_beam1 / number_of_particles_in_beam2)
    elif charge_mass_beam2 < 0:
        q_2 = q_1 * (number_of_particles_in_beam1 / number_of_particles_in_beam2)
    else:
        q_2 = 0
    rho_back = (-q_1 / length_of_system) * (number_of_background_ions)
    return q_1, q_2, rho_back