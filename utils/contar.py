import pandas as pd

#ME cuenta todos los atributos ( analisis)
file_path = 'accionsPreprocesadas1.csv'  # Replace with the path to your file
try:
    accions = pd.read_csv(file_path)
except FileNotFoundError:
    raise FileNotFoundError(f"The file {file_path} does not exist.")

# Initialize a dictionary to store results
attribute_analysis = {}

# Analyze each column (attribute)
for column in accions.columns:
    total_count = len(accions[column])  # Total number of values
    null_count = accions[column].isna().sum()  # Count of null values
    duplicate_count = accions[column].duplicated(keep=False).sum()  # Count of duplicates
    
    # Store results in the dictionary
    attribute_analysis[column] = {
        "Total Count": total_count,
        "Null Count": null_count,
        "Duplicate Count": duplicate_count
    }

# Convert the results to a DataFrame for better visualization
attribute_analysis_df = pd.DataFrame(attribute_analysis).transpose()

# Save results to a CSV file
output_file = 'contar.csv'
attribute_analysis_df.to_csv(output_file, index=True)

print(f"Analysis results saved to {output_file}")
