import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from scipy.spatial.distance import jaccard
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_excel("numerical_dataset.xlsx")

# Set seed for reproducibility
np.random.seed(123)

# Determine the number of rows for training (70%)
n_rows = len(df)
train_size = int(0.7 * n_rows)

# Create indices for the training set
train_indices = np.random.choice(n_rows, size=train_size, replace=False)

# Save the indices
np.save('train_indices.npy', train_indices)

# Create the training set
train_data = df.iloc[train_indices].copy()

# Rename the first column to 'content_id'
train_data.columns = ['content_id'] + list(train_data.columns[1:])

# Create a new value in the 'content_id' column for a unique identifier
train_data['content_id'] = ['content_' + str(i) for i in range(len(train_data))]

# Replace all '0' values with NaN
train_data.replace(0, np.nan, inplace=True)

# Melt the dataframe
melted_train_data = train_data.melt(id_vars='content_id', var_name='ugc', value_name='frequency')
melted_train_data.dropna(subset=['frequency'], inplace=True)
melted_train_data.sort_values(by=['content_id', 'ugc'], inplace=True)

# Create a logical boolean matrix
train_logical_matrix = melted_train_data.pivot_table(index='content_id', columns='ugc', fill_value=0, aggfunc='size') > 0

# Ensure boolean types for better performance
train_logical_matrix = train_logical_matrix.astype(bool)

# Apply the Apriori algorithm
frequent_itemsets_train = apriori(train_logical_matrix, min_support=0.01, use_colnames=True)
frequent_itemsets_train['support'] = frequent_itemsets_train['support'].round(2)
rules_train = association_rules(frequent_itemsets_train, metric='confidence', min_threshold=1)

# Round off the support, confidence, and lift values to 2 decimal places
rules_train[['support', 'confidence', 'lift']] = rules_train[['support', 'confidence', 'lift']].round(2)

# Display the results for Train set
print("Frequent Itemsets for Train Set:")
print(frequent_itemsets_train)

# Save the frequent itemsets to an Excel file
frequent_itemsets_train.to_excel('frequent_itemsets_train.xlsx', sheet_name='Frequent Itemsets', index=False)
print("Frequent itemsets for Train Set have been saved to 'frequent_itemsets_train.xlsx'")

# Load the indices used for testing
train_indices_ts = np.load('train_indices.npy')

# Use the remaining 30% for testing
test_indices_ts = np.setdiff1d(np.arange(n_rows), train_indices_ts)
test_data = df.iloc[test_indices_ts].copy()

# Rename first column to 'content_id'
test_data.columns = ['content_id'] + list(test_data.columns[1:])

# Create new value in the 'content_id' column for a unique identifier
test_data['content_id'] = ['content_' + str(i) for i in range(len(test_data))]

# Replace all '0' values with NaN
test_data.replace(0, np.nan, inplace=True)

# Melt dataframe
melted_test_data = test_data.melt(id_vars='content_id', var_name='ugc', value_name='frequency')
melted_test_data.dropna(subset=['frequency'], inplace=True)
melted_test_data.sort_values(by=['content_id', 'ugc'], inplace=True)

# Create logical boolean matrix
test_logical_matrix = melted_test_data.pivot_table(index='content_id', columns='ugc', fill_value=0, aggfunc='size') > 0

# Ensure boolean types for better performance
test_logical_matrix = test_logical_matrix.astype(bool)

# Apply Apriori algorithm
frequent_itemsets_test = apriori(test_logical_matrix, min_support=0.01, use_colnames=True)
frequent_itemsets_test['support'] = frequent_itemsets_test['support'].round(2)
rules_test = association_rules(frequent_itemsets_test, metric='confidence', min_threshold=1)

# Round off the support, confidence, and lift values to 2 decimal places
rules_test[['support', 'confidence', 'lift']] = rules_test[['support', 'confidence', 'lift']].round(2)

# Display the results for Test set
print("Frequent Itemsets for Test Set:")
print(frequent_itemsets_test)

# Extract rule labels from the results
rules_labels_train = rules_train[['antecedents', 'consequents']].apply(lambda row: tuple(sorted(row['antecedents'] | row['consequents'])), axis=1)
rules_labels_test = rules_test[['antecedents', 'consequents']].apply(lambda row: tuple(sorted(row['antecedents'] | row['consequents'])), axis=1)

# Identify common rules
common_rules = set(rules_labels_train) & set(rules_labels_test)

# Print or inspect the common rules
print(f"Number of common rules between training and testing data: {len(common_rules)}")

# Extract performance metrics for training and testing rules
print("Training metrics:")
print(rules_train[['support', 'confidence', 'lift']])

rules_train.to_excel('rules_train.xlsx', sheet_name='rules_train', index=False)
print("Frequent itemsets and rules for Train Set have been saved to 'rules_train.xlsx'")

print("Testing metrics:")
print(rules_test[['support', 'confidence', 'lift']])

rules_test.to_excel('rules_test.xlsx', sheet_name='rules_test', index=False)
print("Frequent itemsets and rules for Test Set have been saved to 'rules_test.xlsx'")

# Jaccard similarity
union_rules = set(rules_labels_train) | set(rules_labels_test)
jaccard_similarity = len(common_rules) / len(union_rules)
print(f"Jaccard Similarity between training and testing rules: {jaccard_similarity:.2f}")
