import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def calculate_exposure(df, pop_col, pm_col):
    # Equation 3: Xg = Sum(Pop * PM) / Sum(Pop)
    numerator = (df[pop_col] * df[pm_col]).sum()
    denominator = df[pop_col].sum()
    return numerator / denominator if denominator != 0 else 0

def generate_heatmap(df):
    # Updated columns based on the Rubric Section VI
    cols = ['pm25_corrected', 'median_income', 'pct_minority', 'pct_bachelors', 'pct_poverty']
    # Filter only columns that exist in the dataframe to avoid errors
    existing_cols = [c for c in cols if c in df.columns]
    
    plt.figure(figsize=(10, 8))
    corr = df[existing_cols].corr()
    sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0)
    plt.title("Environmental Justice Correlation Heatmap")
    plt.tight_layout()
    plt.show()