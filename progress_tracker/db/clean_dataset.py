#SCRIPT TO CLEAN BOOKS DATASET
import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('C:/progress_tracker_project/progress_tracker/db/BooksDataset.csv') 


# 1. Remove duplicate entries based on Title and Authors
df = df.drop_duplicates(subset=['Title', 'Authors'])

# 2. Keep only the required columns
df = df[['Title', 'Authors', 'Description', 'Category', 'Publish Date (Year)']]


# 3. Exclude columns like Publisher, Price Starting With ($), and Publish Date (Month)
# No need to drop them explicitly as we are selecting only the required columns in step 2

# 4. Populate missing Ratings and Pages with random values
# For Ratings: Generate random values between 1.0 and 5.0
#df['Rating'] = np.where(df['Rating'].isnull(), np.round(np.random.uniform(1.0, 5.0, size=len(df)), 1), df['Rating'])
if 'Rating' not in df.columns:
    df['Rating'] = np.round(np.random.uniform(1.0, 5.0, size=len(df)), 1)

# For Pages: Generate random values between 100 and 500
#df['Pages'] = np.where(df['Pages'].isnull(), np.random.randint(100, 501, size=len(df)), df['Pages'])
if 'Pages' not in df.columns:
    df['Pages'] = np.random.randint(50, 1000, size=len(df))

# Ensure Ratings are float and Pages are integers
df['Rating'] = df['Rating'].astype(float)
df['Pages'] = df['Pages'].astype(int)

# 5. Handle Category: Keep up to 2 unique categories per book
df['Category'] = df['Category'].apply(lambda x: ', '.join(x.split(', ')[:2]) if pd.notnull(x) else '')

# 6. Remove entries where descriptions are missing
df = df.dropna(subset=['Description'])

# 7. Additional cleaning:
# - Normalize text fields to lowercase for consistency
df['Title'] = df['Title'].str.lower()
df['Authors'] = df['Authors'].str.lower()
df['Description'] = df['Description'].str.lower()
df['Category'] = df['Category'].str.lower()

# - Strip whitespace from all text columns
df['Title'] = df['Title'].str.strip()
df['Authors'] = df['Authors'].str.strip()
df['Description'] = df['Description'].str.strip()
df['Category'] = df['Category'].str.strip()

# - Ensure 'Publish Date (Year)' is numeric and contains only valid years
# df['Publish Date (Year)'] = pd.to_numeric(df['Publish Date (Year)'], errors='coerce').fillna(0).astype(int)

# Strip spaces from column names
df.rename(columns=lambda x: x.strip(), inplace=True)

# Rename columns to match database schema
df.rename(columns={
    'Title': 'title',
    'Authors': 'authors',
    'Description': 'description',
    'Category': 'category',
    'Publish Date (Year)': 'publish_year',  # Adjusted to match your schema
    'Rating': 'rating',
    'Pages': 'pages'
}, inplace=True)

# Convert the 'publish_year' column to numeric
if 'publish_year' in df.columns:
    df['publish_year'] = pd.to_numeric(df['publish_year'], errors='coerce').fillna(0).astype(int)
else:
    print("Column 'publish_year' not found in DataFrame.")

df['title'] = df['title'].str.title()

# - Remove 'by' from the start of the 'authors' column and capitalize the first letter of each name
df['authors'] = df['authors'].str.replace(r'^by\s+', '', case=False, regex=True).str.title()

# - Capitalize only the first letter of each 'description'
df['description'] = df['description'].str.capitalize()

# Drop rows with any null values
df.dropna(inplace=True)

# Reset the index after cleaning
df.reset_index(drop=True, inplace=True)

# View the cleaned data
print(df.head())


# Save cleaned data back to a CSV file (optional)
df.to_csv('C:/progress_tracker_project/progress_tracker/db/CleanedBooksDataset.csv', index=False)

