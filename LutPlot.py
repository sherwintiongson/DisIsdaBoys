import matplotlib.pyplot as plt
import re


def plot_lut_data(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Use regex to find all numeric values within the content
        # This matches integers, decimals, and negative numbers
        data_str = re.findall(r"[-+]?\d*\.\d+|\d+", content)

        # The first number in the file snippet is '4096' (array size)
        # We skip the declaration values and only take the actual array elements.
        # Based on the file structure, the array starts after the '{'

        # Extract everything between the curly braces
        array_match = re.search(r'\{(.*?)\}', content, re.DOTALL)
        if not array_match:
            print("Could not find array data within curly braces.")
            return

        array_content = array_match.group(1)
        values = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", array_content)]

        # Generate indices for the Y-axis
        indices = list(range(len(values)))

        # Plotting: X-axis = values, Y-axis = indices
        plt.figure(figsize=(10, 6))
        plt.plot(values, indices, label='LUT Data')

        plt.title('ProxLUT Data: Array Values vs. Index')
        plt.xlabel('Celcius')
        plt.ylabel('NTC Reading in digit')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()

        plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Replace with your actual file path
plot_lut_data('ProxLUT.txt')