import pandas as pd

# Load your CSV
df = pd.read_csv('vulnerabilities_updated.csv')

# Define the function to prepend "rust\n" only if the value is not empty
def prepend_rust_if_not_empty(cell_value):
    # Check if the cell is not empty (i.e., not NaN and not an empty string)
    if pd.notna(cell_value) and cell_value != '':
        return "rust\n" + str(cell_value)  # Prepend "rust\n"
    return cell_value  # Return the original value if the cell is empty

# Apply the function to the 'insecure_code' column starting from row 296
df.loc[295:, 'insecure_code'] = df.loc[295:, 'insecure_code'].apply(prepend_rust_if_not_empty)

# Apply the function to the 'secure_code' column starting from row 296
df.loc[295:, 'secure_code'] = df.loc[295:, 'secure_code'].apply(prepend_rust_if_not_empty)

# Save the modified file
df.to_csv('vulnerabilities_modified.csv', index=False)
