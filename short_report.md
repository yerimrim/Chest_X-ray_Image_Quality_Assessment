# Chest X-ray Image Quality Assessment

## Short Report

### 1. Project Overview

Chest X-ray Image Quality Assessment is a web-based system designed to evaluate the quality of chest X-ray images automatically. The system analyzes uploaded images using three image quality metrics: brightness, contrast, and sharpness. Based on predefined thresholds, it determines whether an image is suitable for further analysis and generates visual reports and downloadable PDF reports.

The main objective of this project is to support radiologic technologists by providing preliminary image quality screening before diagnosis or AI analysis. This system does not replace professional judgment but serves as an assistive tool to improve efficiency and consistency in quality assessment.

---

### 2. Project Objectives

The objectives of this project are:

* To evaluate chest X-ray image quality using brightness, contrast, and sharpness metrics.
* To identify whether chest X-ray images are acceptable for further analysis.
* To provide interpretable quality assessment results through rule-based decision making.
* To generate visualizations and PDF reports for documentation and review.

---

### 3. Tools and Libraries Used

| Library / Tool      | Purpose                                                            |
| ------------------- | ------------------------------------------------------------------ |
| OpenCV              | Extract image features such as brightness, contrast, and sharpness |
| NumPy               | Perform numerical computations for image processing                |
| Pandas              | Organize analysis results into tabular form                        |
| Matplotlib          | Generate statistical charts                                        |
| Seaborn             | Create visualization plots                                         |
| ReportLab           | Generate structured PDF reports                                    |
| Flask               | Develop the web application backend                                |
| HTML/CSS/JavaScript | Build the user interface                                           |

---

### 4. Workflow

The system follows the workflow below:

1. Users upload chest X-ray images through the web interface.
2. The system extracts brightness, contrast, and sharpness features from each image.
3. Images are classified as Accept or Reject based on predefined thresholds.
4. Quality grades (A–D) are assigned according to the calculated quality score.
5. Statistical visualizations are generated.
6. A comprehensive PDF report is created for documentation and review.

The workflow diagram is provided in the README and presentation materials.

---

### 5. Code Implementation

#### Feature Extraction

The system evaluates image quality using three image characteristics:

* **Brightness:** Mean pixel intensity
* **Contrast:** Standard deviation of pixel intensities
* **Sharpness:** Laplacian variance

#### Quality Decision Logic

An image is classified as **Accept** only if all quality criteria are satisfied:

* 70 ≤ Brightness ≤ 180
* Contrast ≥ 40
* Sharpness ≥ 100

Otherwise, the image is classified as **Reject**, and reasons such as Too Dark, Too Bright, Low Contrast, or Blurry are provided.

#### Grade Assignment

Quality scores are calculated using weighted contributions:

* Brightness: 30 points
* Contrast: 30 points
* Sharpness: 40 points

Based on the total score, quality grades are assigned:

* A: 90–100
* B: 70–89
* C: 50–69
* D: 0–49

---

### 6. Test Cases and Results

The project was tested using multiple chest X-ray images with different quality characteristics.

#### Sample Inputs

* blurry1.jpg
* bright1.jpg
* dark1.jpg
* clear1.jpeg

#### Sample Outputs

The system successfully generated:

* Accept/Reject decisions
* Quality grades (A–D)
* Brightness distribution charts
* Sharpness distribution charts
* Grade distribution charts
* Status distribution charts
* Downloadable PDF quality reports

The results demonstrated that the system could effectively identify poor-quality images and provide interpretable explanations for rejection decisions.

---

### 7. Importance of README.md and requirements.txt

#### README.md

README.md is essential in open source projects because it provides users and contributors with important information about the project. It describes the project objectives, features, installation process, execution instructions, and usage examples. A well-written README improves usability, reproducibility, and collaboration.

#### requirements.txt

requirements.txt specifies the external libraries and package versions required to run the project correctly. It ensures that other users can reproduce the same development environment easily by installing dependencies with a single command.

---

### 8. Conclusion

This project developed a rule-based chest X-ray image quality assessment system that automatically evaluates image quality using brightness, contrast, and sharpness metrics. The system provides interpretable quality assessments, visualizations, and downloadable PDF reports to support radiologic technologists during preliminary image screening. The project demonstrates how open source tools and libraries can be integrated to create practical healthcare applications efficiently.
