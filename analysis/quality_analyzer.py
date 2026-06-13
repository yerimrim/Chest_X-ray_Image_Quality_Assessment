import cv2
import numpy as np
import pandas as pd


# Image Quality Analyzer - Evaluates brightness, contrast, and sharpness of images
def calculate_grade(brightness, contrast, sharpness):
    score = 0
    # Brightness thresholds for good quality
    if 70 <= brightness <= 180:
        score += 30
    # Contrast threshold for good quality
    if contrast >= 40:
        score += 30
    # Sharpness threshold for good quality
    if sharpness >= 100:
        score += 40
    # Assign grades based on total score
    if score >= 90:
        return "A"
    
    elif score >= 70:
        return "B"
    elif score >= 50:
        return "C"
    return "D"

# Evaluates image quality based on brightness, contrast, and sharpness thresholds
def evaluate_quality(brightness, contrast, sharpness):
    reasons = []
    # Check brightness thresholds
    if brightness < 70:
        reasons.append("Too Dark")
    elif brightness > 180:
        reasons.append("Too Bright")

    # Check contrast threshold
    if contrast < 40:
        reasons.append("Low Contrast")

    # Check sharpness threshold
    if sharpness < 100:
        reasons.append("Blurry")

    # If no reasons, image is acceptable
    if len(reasons) == 0:
        return ("Accept", "Suitable for Analysis")

    # Otherwise, reject with reasons
    return ("Reject", ", ".join(reasons))


# Main function to analyze a list of image files and return a DataFrame with quality metrics and evaluations
def analyze_images(files):
    results = []
    # Process each uploaded image file
    for file in files:
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
        # If the image cannot be read, skip it
        if img is None:
            continue

        # Brightness is calculated as the mean pixel intensity
        brightness = img.mean()
        # Contrast is calculated as the standard deviation of pixel intensities
        contrast = img.std()
        # Sharpness is calculated using the variance of the Laplacian
        sharpness = cv2.Laplacian(img, cv2.CV_64F).var()

        # Calculate grade and evaluate quality based on the computed metrics
        grade = calculate_grade(brightness, contrast, sharpness)
        # Evaluate quality and get status and reason for acceptance or rejection
        status, reason = evaluate_quality(brightness,contrast,sharpness)
        
        # Append the results for each image to the list, rounding metrics to 2 decimal places
        results.append({
            "image_name": file.filename,
            "brightness": round(brightness, 2),
            "contrast": round(contrast, 2),
            "sharpness": round(sharpness, 2),
            "grade": grade,
            "status": status,
            "reason": reason
        })

    return pd.DataFrame(results)