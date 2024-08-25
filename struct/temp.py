# DO NOT RUN THIS IF NOT NEEDED

import pandas as pd

# Load the existing CSV file into a DataFrame
df = pd.read_csv('user_data.csv')

# Add the new column "Phone Number" with empty values
df['Phone Number'] = ''

# Save the updated DataFrame back to the CSV file
df.to_csv('user_data.csv', index=False)

print("Added 'Phone Number' column with all values empty.")