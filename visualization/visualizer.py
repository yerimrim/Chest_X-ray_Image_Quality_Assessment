import matplotlib
matplotlib.use('Agg')

import os
import matplotlib.pyplot as plt
import seaborn as sns

CHART_FOLDER = "static/charts"

#  Generate visualizations based on the DataFrame and save them as images
def create_visualizations(df):
    # Ensure the chart folder exists
    os.makedirs(CHART_FOLDER, exist_ok=True)

    # Create and save the grade distribution chart
    plt.figure()
    sns.countplot(data=df, x="grade")
    plt.title("Grade Distribution")
    plt.savefig(f"{CHART_FOLDER}/grade.png")
    plt.close()

    # Create and save the Accept vs Reject distribution
    plt.figure()
    sns.countplot(data=df, x="status")
    plt.title("Accept vs Reject")
    plt.savefig(f"{CHART_FOLDER}/status.png")
    plt.close()

    # Create and save the brightness distribution chart
    plt.figure()
    sns.histplot(df["brightness"], kde=True)
    plt.savefig(f"{CHART_FOLDER}/brightness.png")
    plt.close()

    # Create and save the sharpness distribution chart
    plt.figure()
    sns.histplot(df["sharpness"], kde=True)
    plt.savefig(f"{CHART_FOLDER}/sharpness.png")
    plt.close()