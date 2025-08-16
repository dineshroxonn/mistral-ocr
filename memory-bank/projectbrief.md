# Project Brief: Mistral OCR Data Processor

## 1. Project Goal

The primary goal of this project is to create a robust, automated pipeline that accurately extracts, calculates, and formats data from image-based mortgage documents into a structured Excel format.

## 2. Core Requirements

- **Automated Data Extraction:** Utilize the Mistral Document AI model to extract raw text and structured data from image files (`.jpg`, `.pdf`, etc.).
- **Complex Calculations:** Implement a series of financial calculations based on the extracted data and specific business rules (e.g., purchase value reductions, loan amounts, interest).
- **Dynamic Data Investigation:** Perform web-based research, following a detailed flowchart, to determine property tax assessment rates. This includes handling aliases, unrecognized city names, and other edge cases.
- **Precise Formatting:** Apply strict formatting rules to all data points, including reference numbers, names, currency, and percentages, to match a predefined Excel template.
- **Structured Output:** Generate a final `.xlsx` file containing the fully processed and correctly formatted data.

## 3. Scope

The system should be capable of processing one image at a time via a Python script. The core logic for calculations and formatting is defined by a set of training documents and a process flowchart. The immediate focus is on accurately processing the `Workload0001.jpg` image as a proof of concept.
