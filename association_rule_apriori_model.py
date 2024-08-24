import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Path to Excel file
excel_file_path = 'numerical_dataset.xlsx'
df = pd.read_excel(excel_file_path)
df

# Melt the DataFrame
melted_df = pd.melt(df, id_vars=['content_id'], var_name='ugc', value_name='frequency')

# Drop rows with NaN values in the 'frequency' column
melted_df = melted_df.dropna(subset=['frequency'])

# Sort the DataFrame by 'content_id' and 'ugc'
melted_df = melted_df.sort_values(by=['content_id', 'ugc'])

# Display the result
#print(melted_df)

# Extract the numeric part from 'content_id' and convert to integers
melted_df['content_number'] = melted_df['content_id'].str.extract('(\d+)').astype(int)

# Sort the DataFrame by 'content_number' and 'ugc' in ascending order
melted_df = melted_df.sort_values(by=['content_number', 'ugc'])

# Drop the 'content_number' column if it's no longer needed
melted_df = melted_df.drop(columns=['content_number'])

# Display the result
print(melted_df)

# Save the result to a new Excel file
output_excel_path = 'ugc_data_melted.xlsx'
melted_df.to_excel(output_excel_path, index=False)

print(f"Data has been saved to {output_excel_path}")

# Load the data for further processing
df = pd.read_excel('ugc_data_melted.xlsx')
df

# Create a binary matrix (transaction encoding)
binary_matrix = pd.crosstab(df['content_id'], df['ugc']).astype(bool).astype(int)

# Apply Apriori algorithm
frequent_itemsets = apriori(binary_matrix, min_support=0.01, use_colnames=True)
sorted_frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)

# Round the support column to 2 decimal places
sorted_frequent_itemsets['support'] = sorted_frequent_itemsets['support'].round(2)

# Generate association rules and sort the rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=1)
sorted_rules = rules.sort_values(by=['lift', 'support'], ascending=[False, False])

# Round the support, confidence, and lift columns to 2 decimal places
sorted_rules['support'] = sorted_rules['support'].round(2)
sorted_rules['confidence'] = sorted_rules['confidence'].round(2)
sorted_rules['lift'] = sorted_rules['lift'].round(2)

# Display the results
print("Frequent Itemsets:")
print(sorted_frequent_itemsets)

# Display the sorted results with selected columns
selected_columns = ['antecedents', 'consequents', 'support', 'confidence', 'lift']
print("Association Rules:")
print(sorted_rules[selected_columns])

# Save the frequent itemsets and association rules to an Excel file
try:
    with pd.ExcelWriter('frequent_itemsets_and_association_rules.xlsx') as writer:
        sorted_frequent_itemsets.to_excel(writer, sheet_name='Frequent Itemsets', index=False)
        sorted_rules[selected_columns].to_excel(writer, sheet_name='Association Rules', index=False)
    print("Results saved to 'frequent_itemsets_and_association_rules.xlsx'")
except PermissionError as e:
    print(f"Permission error: {e}. Ensure the file is not open and you have write permissions.")

# Filter rules with lift greater than 1
filtered_rules = sorted_rules[sorted_rules['lift'] > 1]

# Create a directed graph from the filtered association rules
for _, row in filtered_rules.iterrows():
    antecedent = ', '.join(row['antecedents']) if isinstance(row['antecedents'], tuple) else row['antecedents']
    consequent = ', '.join(row['consequents']) if isinstance(row['consequents'], tuple) else row['consequents']
    lift = row['lift']
    G.add_node(antecedent, type='antecedent')
    G.add_node(consequent, type='consequent')
    G.add_edge(antecedent, consequent, lift=lift)

# Define edge colors based on lift values
edge_colors = ['green' if G[u][v]['lift'] > 4 else 'orange' for u, v in G.edges()]

# Define edge widths based on lift values
edge_widths = [G[u][v]['lift'] for u, v in G.edges()]

# Adjust the position of nodes
pos = nx.spring_layout(G, seed=8, k=2.8)  # Increase k value to spread out nodes more

# Plot the graph
plt.figure(figsize=(31, 13))  # Increase the figure size for better readability
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', edge_color=edge_colors, width=edge_widths, font_color='blue', font_size=28, font_weight='bold', arrowsize=38)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{G[u][v]['lift']:.2f}" for u, v in G.edges()}, font_color='black', font_size=24, font_weight='medium')
plt.title('User Engagement Model Based on Association Rules with Lift > 3.0000')

# Save the plot to a PDF file
plt.savefig("C:/Users/daiml/Downloads/user_engagement_model.pdf", format="pdf")

# Show the plot
print("The Model:")
plt.show()
