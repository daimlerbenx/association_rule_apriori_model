# Define counts for the Venn diagram
num_common_rules = len(common_rules)
num_train_unique_rules = len(set(rules_labels_train)) - num_common_rules
num_test_unique_rules = len(set(rules_labels_test)) - num_common_rules
num_total_unique_rules = len(set(rules_labels_train) | set(rules_labels_test))

# Calculate Jaccard Similarity
jaccard_similarity = num_common_rules / num_total_unique_rules

# Find unique rules in training and testing sets
unique_train_rules = set(rules_labels_train) - common_rules
unique_test_rules = set(rules_labels_test) - common_rules

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Data for plotting
labels = ['Common Rules', 'Unique to Training Set', 'Unique to Testing Set']
values = [num_common_rules, num_train_unique_rules, num_test_unique_rules]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# Create bar plot
bars = ax.bar(labels, values, color=colors)

# Add annotations
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval}', ha='center', va='bottom')

# Add title and labels
ax.set_title('Comparison of Association Rules Between Training and Testing Sets')
ax.set_ylabel('Number of Rules')

# Show Jaccard Similarity Score on the plot
plt.figtext(0.5, 0.02, f'Jaccard Similarity between training and testing rules: {jaccard_similarity:.2f}', 
            ha='center', va='center', fontsize=12, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

# Show plot
plt.show()

# Print results
print(f"Number of common rules: {num_common_rules}")
print(f"Number of unique rules in training set: {num_train_unique_rules}")
print(f"Number of unique rules in testing set: {num_test_unique_rules}")
print(f"Jaccard Similarity between training and testing rules: {jaccard_similarity:.2f}")

# Print the results
print("Common Rules:")
print(common_rules)
print("Unique Rules in Training Set:")
print(unique_train_rules)
print("Unique Rules in Testing Set:")
print(unique_test_rules)
