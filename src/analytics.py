import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_heatmap(df):
    # Variables for the heatmap as per Section 5 requirements
    #sub-group variables for the heatmap as per Section 5 requirements
    print("Generating heatmap...")
    heatmap_vars = [
        'pm25_corrected', 
        'Median_Household_Income', 
        'Pct_Minority', 
        'Pct_Poverty',
        'Pct_White',
        'Pct_Black',
        'Pct_Hispanic',
        'Pct_Bachelors_Plus'
    ]

    # 2. Defining "Clean Names" for the display
    clean_labels = [
        'PM2.5 Intensity', 
        'Median Income', 
        'Minority %', 
        'Education %', 
        'Poverty %',
        'White %',
        'Black %',
        'Hispanic %',
        'Bachelor+ %'
    ]

    # 3. Calculate the correlation matrix
    corr_matrix = df[heatmap_vars].corr()
    # 4. Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap='RdYlGn_r', 
        center=0, 
        fmt=".2f",
        xticklabels=clean_labels, # Renames the bottom axis
        yticklabels=clean_labels  # Renames the side axis
    )

    plt.title('Relationship between Population intensity and demographic variables', fontsize=14, pad=20)
    plt.xticks(rotation=45) # Rotates labels for better readability
    plt.tight_layout()
    #show the plot
    plt.show()