User Engagement Pattern Discovery and Visualization
This script aims to discover patterns of user engagement from a dataset and visualize these patterns using a network graph. The process involves the following key steps:

Overview
Data Preparation:

Load Data: Reads a dataset from an Excel file containing numerical data related to user engagement.
Melt Data: Converts the data into a format suitable for pattern analysis by melting it into a long format.
Process Data: Cleans and sorts the data, then saves the processed data to a new Excel file.
Pattern Analysis:

Binary Matrix Creation: Transforms the data into a binary matrix where each entry indicates whether a specific user engagement component is present.
Frequent Itemsets: Uses the Apriori algorithm to identify frequent itemsets in the binary matrix.
Association Rules: Generates association rules based on the frequent itemsets, with a focus on rules having a confidence of 1 or higher.
Visualization:

Network Graph Construction: Creates a directed graph to represent the association rules where nodes are engagement components, and edges represent the relationships between them with lift values.
Graph Customization: Edges are colored and sized based on the lift value to visually distinguish stronger associations.
Plot and Save: Displays and saves the network graph as a PDF file for detailed analysis.
Key Outputs
Processed Data:

ugc_data_melted.xlsx: Contains the melted and cleaned user engagement data.
Frequent Itemsets and Association Rules:

frequent_itemsets_and_association_rules.xlsx: Includes frequent itemsets and association rules, with support, confidence, and lift values rounded for clarity.
Network Graph:

user_engagement_model.pdf: A visual representation of the user engagement model based on association rules, showing nodes for engagement components and edges for relationships with varying lift values.
How to Use
Ensure you have the necessary Python libraries installed: pandas, mlxtend, networkx, and matplotlib.
Place your numerical dataset in the same directory as the script and name it numerical_dataset.xlsx.
Run the script. It will process the data, perform pattern analysis, and generate a PDF file with the network graph visualization.
Check the output files (ugc_data_melted.xlsx and frequent_itemsets_and_association_rules.xlsx) for detailed results and the user_engagement_model.pdf for the visual representation.
