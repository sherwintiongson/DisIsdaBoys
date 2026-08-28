import matplotlib.pyplot as plt
import numpy as np


def moving_average_filter(data, window_size):
    """
    Applies a moving average FIR filter to the input data.

    Parameters:
    - data: Input data (1D array or list)
    - window_size: Size of the moving average window

    Returns:
    - filtered_data: Output data after applying the moving average filter
    """
    filtered_data = []

    for i in range(len(data) - window_size + 1):
        window = data[i : i + window_size]
        average = sum(window) / window_size
        filtered_data.append(average)

    return filtered_data

# Example usage and plot
if __name__ == "__main__":

    np.random.seed(42)
    original_data = np.random.random_integers(35000, 45000, 100) * 5

    # Set the window size for the moving average filter
    window_size_2 = 2
    window_size_10 = 10
    window_size_30 = 30

    # Apply the moving average filter
    filtered_data_2 = moving_average_filter(original_data, window_size_2)
    filtered_data_10 = moving_average_filter(original_data, window_size_10)
    filtered_data_30 = moving_average_filter(original_data, window_size_30)

    # Plot the original and filtered data
    plt.figure(figsize=(15, 8))
    plt.plot(original_data, label='Original Data', linestyle='-', marker='o')
    plt.plot(filtered_data_2, label=f'FIR Filter - Moving Average (Window Size = {window_size_2})', linestyle='-', marker='o')
    plt.plot(filtered_data_10, label=f'FIR Filter - Moving Average (Window Size = {window_size_10})', linestyle='-', marker='o')
    plt.plot(filtered_data_30, label=f'FIR Filter - Moving Average (Window Size = {window_size_30})', linestyle='-', marker='o')
    plt.title('Moving Average FIR Filter Example')
    plt.xlabel('Sample Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
