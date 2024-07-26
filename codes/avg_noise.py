import pandas as pd

try:
    # Load the Excel file
    file_path = 'C:\\Users\\Kim Jihun\\Desktop\\data\\jet_nois_data.xlsx'
    data = pd.read_excel(file_path)
    print("File loaded successfully")

    print(data.head())

    filtered_data_b737 = data[data.iloc[:, 0].str.contains('737', na=False)]
    num_ac_b737=len(filtered_data_b737)
    filtered_data_a320 = data[data.iloc[:, 0].str.contains('A320', na=False)]
    num_ac_a320=len(filtered_data_a320)

    print(f"Filtered data for A320:\n{filtered_data_a320}")
    print(f"Filtered data for B737:\n{filtered_data_b737}")

    approach_noise_mean_b737 = filtered_data_b737.iloc[:, 2].mean()
    approach_noise_mean_a320 = filtered_data_a320.iloc[:, 2].mean()

    print("The mean approach noise level for A320 is: {0}EPNdB, Measurment num: {1}".format(approach_noise_mean_a320,num_ac_a320))
    print("The mean approach noise level for B737 is: {0}EPNdB, Measurment num: {1}".format(approach_noise_mean_b737,num_ac_b737))
except Exception as e:
    print(f"An error occurred: {e}")