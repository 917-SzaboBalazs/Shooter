def one_hot_encode(number, num_categories):
    """
    Transform a number into its one-hot encoded vector using Python lists.

    Parameters:
    number (int): The number to be one-hot encoded.
    num_categories (int): The total number of categories.

    Returns:
    list: The one-hot encoded vector.
    """
    # Initialize a list of zeros with length equal to the number of categories
    one_hot_vector = [0] * num_categories

    # Set the position corresponding to the number to 1
    one_hot_vector[number] = 1

    return one_hot_vector