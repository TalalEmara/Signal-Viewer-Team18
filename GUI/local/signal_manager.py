import pandas as pd

def load_signal(file_path):
    try:
        # Load the data, assuming two columns separated by whitespace
        data = pd.read_csv(file_path, header=None, sep='\s+')
        data = data.apply(pd.to_numeric, errors='coerce')  # Ensure numeric values
        print(f"Loaded data from {file_path}:\n{data.head()}\n")  # Debugging output
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Example usage
if __name__ == '__main__':
    signal1_path = 'emg.csv'  # Replace with your actual file path
    data1 = load_signal(signal1_path)

    if data1 is not None:
        print("Data loaded successfully:")
        print(data1)
    else:
        print("Failed to load data.")
