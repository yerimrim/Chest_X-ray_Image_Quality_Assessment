# Chest X-ray Image Quality Assessment

A web-based system for chest X-ray image quality assessment. The system automatically analyzes uploaded X-ray images using brightness, contrast, and sharpness metrics, generates visual reports, and provides downloadable PDF reports for documentation and review.

---

## Project Overview

### Objectives

* Evaluate chest X-ray image quality using brightness, contrast, and sharpness metrics.
* Identify whether images are acceptable for further analysis.
* Present results through interactive visualizations and automated reports.

### Why is it Useful?

* Detects poor-quality chest X-ray images before diagnosis or AI analysis.
* Supports radiologic technologists through preliminary image quality screening without replacing professional judgment.

---

## Core Features

### 1. Chest X-ray Quality Analysis

* Automatically evaluates image quality using brightness, contrast, and sharpness.
* Classifies images into **Accept/Reject** status and assigns a quality grade (**A–D**).

#### Assessments

* **Brightness Assessment:** Mean pixel intensity
* **Contrast Assessment:** Standard deviation of pixel intensities
* **Sharpness Assessment:** Laplacian variance

#### Quality Decision Logic

Accept: All quality criteria are satisfied.

* 70 ≤ Brightness ≤ 180
* Contrast ≥ 40
* Sharpness ≥ 100

Reject: One or more quality criteria are not satisfied.

* Brightness < 70 → Too Dark
* Brightness > 180 → Too Bright
* Contrast < 40 → Low Contrast
* Sharpness < 100 → Blurry

#### Grade Assignment

Score Calculation: Brightness (30) + Contrast (30) + Sharpness (40)

Quality grades are assigned based on the total score:

* A: 90–100
* B: 70–89
* C: 50–69
* D: 0–49

---

### 2. Visualization

* Generates charts illustrating quality assessment outcomes.
* Displays grade distribution, acceptance status, brightness distribution, and sharpness distribution.
* Presents analysis results through an intuitive web interface.

---

### 3. PDF Report Generation

* Generates comprehensive medical image quality reports including summary statistics, visualizations, and detailed image assessment results.
* Allows users to download reports in PDF format for documentation and review.

---

## Libraries and Technologies

| Library / Tool          | Purpose                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| OpenCV (cv2)            | Extract image features such as brightness, contrast, and sharpness |
| NumPy                   | Handle numerical operations for image processing                   |
| Pandas                  | Structure and manage analysis results in tabular form              |
| Matplotlib              | Generate statistical charts                                        |
| Seaborn                 | Create visualization plots                                         |
| ReportLab               | Generate PDF reports with tables and images                        |
| Flask                   | Backend framework for image upload and processing                  |
| HTML / CSS / JavaScript | Build the web interface and user interactions                      |

---

## Project Structure

```text
app.py
analysis/
├── quality_analyzer.py
└── __init__.py

visualization/
├── visualizer.py
└── __init__.py

report/
├── pdf_generator.py
└── __init__.py

templates/
├── index.html
└── result.html

outputs/
└── quality_report.pdf

static/
├── charts/
│   ├── brightness.png
│   ├── grade.png
│   ├── sharpness.png
│   └── status.png
├── css/
│   └── style.css
└── js/
    └── preview.js

requirements.txt
README.md
LICENSE
short_report.pdf
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yerimrim/Chest_X-ray_Image_Quality_Assessment.git
cd Chest_X-ray_Image_Quality_Assessment
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Requirements

* Python 3.10.19

Required packages:

```text
Flask
opencv-python
numpy
pandas
matplotlib
seaborn
reportlab
```

---

## How to Run

Start the Flask application:

```bash
python app.py
```

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

---

## Sample Inputs

Example chest X-ray images:

#### blurry
![Sample Image blurry1](sample/sample1_input/blurry1.jpg)

#### bright
![Sample Image bright1](sample/sample1_input/bright1.jpg)

#### dark
![Sample Image dark1](sample/sample1_input/dark1.jpg)

#### clear
![Sample Image clear1](sample/sample1_input/clear1.jpeg)

---

## Sample Outputs

Generated visualizations:

* brightness.png
* grade.png
* sharpness.png
* status.png

Generated report:

* ![quality_report.pdf](sample/sample1_output/quality_report.pdf)

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---

## Contributing

Contributions are welcome.

If you would like to improve this project:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes with clear commit messages.
4. Submit a pull request describing your modifications.

Please ensure that your code is well-documented and tested before submission.

---

## Acknowledgements

This project was developed as part of the **Introduction to Open Source Software** course final assignment.
