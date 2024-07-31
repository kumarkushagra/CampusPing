# import requests
# from bs4 import BeautifulSoup
# url = 'https://www.imsnsit.org/imsnsit/notifications.php'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')


# # print(soup.get_text())

# arr = [link.get('href') for link in soup.find_all('a')]

# print(arr[0])


import pandas as pd

# Create the corrected timetable data with room numbers, ensuring all lists have the same length
timetable_data_corrected = {
    'Time': ['08:00-09:00', '', '09:00-10:00', '', '10:00-11:00', '', '11:00-12:00', '', '12:00-01:00', '', 
             '01:00-02:00', '', '02:00-03:00', '', '03:00-04:00', '', '04:00-05:00', '', '05:00-06:00', '', 
             '06:00-07:00', '', '07:00-08:00', ''],
    'Monday': ['DSP', '4014', 'DSP', '4014', 'DSP', '4014', 'CN', '4014', 'CN', '4014', 
               '', '', '', '', 'IOTA(Tut-2)', '4014', 'DSP(Grp-1)', '4130', 'DSP(Grp-1)', '4130', 
               'DSP(Grp-1)', '4130', '', ''],
    'Tuesday': ['IOTA', '4014', 'DSP', '4014', 'DSP', '4014', 'WMC', '4014', 'DSP(Grp-2)', '4130', 
                'DSP(Grp-2)', '4130', 'DSP(Grp-2)', '4130', 'DSP(Grp-2)', '4130', 'DSP(Grp-2)', '4130', 
                'DSP(Grp-2)', '4130', '', '', '', ''],
    'Wednesday': ['IIOT', '4014', 'CN(Grp-2)', '4015', 'CN(Grp-2)', '4015', 'CN', '4014', '', '', 
                  '', '', '', '', '', '', '', '', '', '', '', '', ''],
    'Thursday': ['IOTA', '4014', 'DSP', '4014', 'DSP', '4014', 'WMC', '4014', 'WMC(Grp-1)', '4015', 
                 'WMC(Grp-1)', '4015', 'WMC(Grp-1)', '4015', '', '', '', '', '', '', '', '', '', ''],
    'Friday': ['CN', '4014', 'WMC(Tut-1)', '4014', 'WMC(Tut-1)', '4014', 'IOTA', '4014', '', '', 
               '', '', '', '', '', '', '', '', '', '', '', '', ''],
    'Saturday': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
}

# Convert the dictionary to a DataFrame
df_corrected = pd.DataFrame(timetable_data_corrected)

# Transpose the DataFrame
df_corrected_transposed = df_corrected.T

# Save the transposed DataFrame to an Excel file
file_path_corrected = "timetable_corrected_transposed.xlsx"
df_corrected_transposed.to_excel(file_path_corrected, header=False)

print(f"Excel file saved as: {file_path_corrected}")
