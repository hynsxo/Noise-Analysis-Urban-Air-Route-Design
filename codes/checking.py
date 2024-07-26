import pandas as pd
import matplotlib.pyplot as plt

try:
    file_path = 'C:\\Users\\Kim Jihun\\Desktop\\data\\KOR_domestic_flight_data(2022).xlsx'
    data = pd.read_excel(file_path)

    column_index = 9
    if column_index < len(data.columns):
        aircraft_types = data.iloc[:, column_index]

        aircraft_types = aircraft_types.replace(
            {'A21N': 'A320F', 'A320': 'A320F', 'A321': 'A320F', 'B737': 'B737F', 'B738': 'B737F'})
        aircraft_distribution = aircraft_types.value_counts()

        plt.figure(figsize=(10, 8))
        plt.pie(aircraft_distribution, labels=aircraft_distribution.index, autopct='%1.1f%%', startangle=140)
        plt.title('Distribution of Aircraft Types')
        plt.axis('equal')
        plt.show()

        print("Aircraft Types Distribution:")
        print(aircraft_distribution)

        output_file_path = 'C:\\Users\\Kim Jihun\\Desktop\\data\\aircraft_distribution.xlsx'
        aircraft_distribution.to_excel(output_file_path, sheet_name='Distribution')
        print(f"Distribution saved to {output_file_path}")

    else:
        print(f"The dataset does not have a column at index {column_index + 1}")

except FileNotFoundError:
    print(f"File not found: {file_path}")
except pd.errors.ParserError:
    print("Error parsing the file")
except Exception as e:
    print(f"An error occurred: {e}")