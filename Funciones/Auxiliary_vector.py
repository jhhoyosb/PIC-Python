def generate_auxiliary_vector(num_elements):
    """
    Generates a vector containing elements from 1 to the specified number of elements, duplicated.
    
    Parameters:
    num_elements (int): Number of elements to generate.
    
    Returns:
    numpy.ndarray: Duplicated vector of elements.
    
    Raises:
    ValueError: If the number of elements is less than or equal to 0.
    """
    if num_elements <= 0:
        raise ValueError("The number of elements must be greater than 0")

    elements = np.arange(num_elements)
    return np.concatenate((elements, elements))