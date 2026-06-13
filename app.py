from flask import (Flask, render_template, request, send_file)
import os
from analysis.quality_analyzer import analyze_images
from visualization.visualizer import create_visualizations
from report.pdf_generator import generate_pdf

# Initialize the Flask web application
app = Flask(__name__)

# Define directory paths for storing uploads, charts, and output files
UPLOAD_FOLDER = "static/uploads"
CHART_FOLDER = "static/charts"
OUTPUT_FOLDER = "outputs"

# Ensure the required directories exist before starting the application
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define the root route to render the main landing page
@app.route("/")
def home():
    return render_template("index.html")

# Handle the image upload and analysis process via POST request
@app.route("/analyze", methods=["POST"])
def analyze():
    # Retrieve the list of uploaded files and filter out empty submissions
    files = request.files.getlist("images")
    files = [file for file in files if file.filename != ""]

    # Return an error to the user if no valid files were provided
    if not files:
        return render_template("index.html", error="Please upload at least one image.")
    
    # Process the uploaded images and return the results as a DataFrame
    df = analyze_images(files)

    # Handle edge cases where images were provided but none could be successfully processed
    if df.empty:
        return render_template("index.html", error="No valid images were processed.")

    # Generate charts and build the PDF report based on the analysis results
    create_visualizations(df)
    pdf_path = generate_pdf(df)

    # Calculate summary statistics to be displayed on the result page
    summary = {
        "total": len(df),
        "accept": (df["status"] == "Accept").sum(),
        "reject": (df["status"] == "Reject").sum(),
        "accept_rate": round(((df["status"] == "Accept").sum()/ len(df)) * 100, 2),
        "avg_brightness": round(df["brightness"].mean(), 2),
        "avg_contrast": round(df["contrast"].mean(), 2),
        "avg_sharpness": round(df["sharpness"].mean(), 2)
    }

    # Render the result template with the formatted data, statistics, and PDF availability
    return render_template(
        "result.html",
        tables=df.to_dict(orient="records"),
        summary=summary,
        pdf_ready=True
    )

# Provide an endpoint for users to download the generated PDF report
@app.route("/download")
def download():
    # Construct the path to the generated PDF file
    pdf_path = os.path.join(OUTPUT_FOLDER, "quality_report.pdf")

    # Verify the file exists before attempting to send it to the client
    if not os.path.exists(pdf_path):
        return (
            "PDF report not found. "
            "Please analyze images first."
        )
    
    # Send the PDF file to the user as a downloadable attachment
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=("quality_report.pdf")
    )

# Start the Flask development server when the script is run directly
if __name__ == "__main__":
    app.run(debug=False)
