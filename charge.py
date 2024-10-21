def charge(
    charge_mass_beam1: float,
    charge_mass_beam2: float,
    number_of_background_ions: int,
    number_of_particles_in_beam1: int,
    number_of_particles_in_beam2: int,
    length_of_system: float,
    plasma_frequency: float
    ):
    charge_mass_beam1 = (plasma_frequency**2 * length_of_system) / (number_of_particles_in_beam1 * charge_mass_beam1)
    if charge_mass_beam2 > 0:
        charge_mass_beam2 = -charge_mass_beam1 * (number_of_particles_in_beam1 / number_of_particles_in_beam2)
    elif charge_mass_beam2 < 0:
        charge_mass_beam2 = charge_mass_beam1 * (number_of_particles_in_beam1 / number_of_particles_in_beam2)
    else:
        charge_mass_beam2 = 0
    rho_back = (-charge_mass_beam1 / length_of_system) * (number_of_background_ions) #Background density
    return charge_mass_beam1, charge_mass_beam2, rho_back