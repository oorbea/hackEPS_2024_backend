import pandas as pd

# Load the accions.csv file
file_path = 'accions.csv'
accions = pd.read_csv(file_path)

# Filter sessions with only one row
session_counts = accions['Sessio'].value_counts()

# Identify sessions with only one row
single_row_sessions = session_counts[session_counts == 1].index

# Filter rows where 'Usuari' is null and the session has only one row
to_remove = accions[(accions['Usuari'].isna()) & (accions['Sessio'].isin(single_row_sessions))]

# Remove these rows from the DataFrame
accions_filtered = accions.drop(to_remove.index)

# Save the updated DataFrame to a new CSV file
filtered_file_path = 'accionsPreprocesadas1.csv'
accions_filtered.to_csv(filtered_file_path, index=False)

print(f"Filtered data saved to {filtered_file_path}")
