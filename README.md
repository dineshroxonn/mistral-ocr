# Mistral OCR Image Processor

## Project Overview

This script processes one or more images from a specified folder, extracts structured data from them using the Mistral Document AI API, and saves the results into individual Excel files. It is designed to handle images that contain multiple records and will extract all of them into a single `.xlsx` file per image.

## Prerequisites

Before running the script, you need to have Python 3 installed, along with the following libraries:

-   `requests`
-   `pandas`
-   `beautifulsoup4`
-   `openpyxl` (for Excel support in pandas)

You can install these libraries using pip:

```bash
pip install requests pandas beautifulsoup4 openpyxl
```

## Configuration

The script requires an API key for the Mistral Document AI service. You need to set this key as an environment variable named `AZURE_API_KEY`.

### On macOS and Linux:

```bash
export AZURE_API_KEY="your_api_key_here"
```

### On Windows:

```bash
set AZURE_API_KEY="your_api_key_here"
```

## Usage

You can run the script from the command line, providing the path to the folder containing your images and an optional path to the folder where you want to save the output Excel files.

### Basic Usage:

```bash
python3 process_image.py /path/to/your/image/folder
```

This will process all the images in the specified folder and save the output Excel files in the same directory where you run the script.

### Specifying an Output Folder:

```bash
python3 process_image.py /path/to/your/image/folder /path/to/your/output/folder
```

This will save the output Excel files in the folder you specify.

## Output

For each image processed, the script will create a corresponding `.xlsx` file with the same name. For example, if you process an image named `Workload0001.jpg`, the script will create a file named `Workload0001.xlsx`.

Each row in the Excel file will contain a single record extracted from the image.
