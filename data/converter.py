import pandas as pd

# Read the original CSV file
df = pd.read_csv('data/series_diff.csv')

# Melt the DataFrame to convert the years into a single column
melted_df = pd.melt(df, id_vars=['Division', 'Sex', 'Event'], var_name='Year', value_name='Value')

# Convert the 'Year' column to integer
melted_df['Year'] = melted_df['Year'].astype(int)

# Sort the DataFrame by 'Division', 'Sex', 'Event', and 'Year'
melted_df = melted_df.sort_values(by=['Division', 'Sex', 'Event', 'Year'])

# Save the result to a new CSV file
melted_df.to_csv('top100avg_zeroed.csv', index=False)