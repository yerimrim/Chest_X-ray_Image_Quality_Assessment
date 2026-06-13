from flask import (Flask, render_template, request, send_file)
import os
from analysis.quality_analyzer import analyze_images
from visualization.visualizer import create_visualizations
from report.pdf_generator import generate_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
CHART_FOLDER = "static/charts"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    files = request.files.getlist("images")
    files = [file for file in files if file.filename != ""]

    if not files:
        return render_template("index.html", error="Please upload at least one image.")

    df = analyze_images(files)

    if df.empty:
        return render_template("index.html", error="No valid images were processed.")

    create_visualizations(df)

    pdf_path = generate_pdf(df)

    summary = {
        "total": len(df),
        "accept": (df["status"] == "Accept").sum(),
        "reject": (df["status"] == "Reject").sum(),
        "accept_rate": round(((df["status"] == "Accept").sum()/ len(df)) * 100, 2),
        "avg_brightness": round(df["brightness"].mean(), 2),
        "avg_contrast": round(df["contrast"].mean(), 2),
        "avg_sharpness": round(df["sharpness"].mean(), 2)
    }

    return render_template(
        "result.html",
        tables=df.to_dict(orient="records"),
        summary=summary,
        pdf_ready=True
    )


@app.route("/download")
def download():
    pdf_path = os.path.join(OUTPUT_FOLDER, "quality_report.pdf")

    if not os.path.exists(pdf_path):
        return (
            "PDF report not found. "
            "Please analyze images first."
        )

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=("quality_report.pdf")
    )


if __name__ == "__main__":
    app.run(debug=False)