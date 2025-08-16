# Technical Context: OCR Automation Stack

## 1. Core Technologies

- **Programming Language:** Python 3 is the exclusive language used for the scripting, chosen for its strong data manipulation libraries and ease of integration with web services.

- **AI Service:** The Mistral Document AI model, accessed via an Azure Serverless API Endpoint, is used for the core OCR and structured data extraction.

- **Data Manipulation:** The `pandas` library is used to structure the final data and export it to an Excel (`.xlsx`) file. `openpyxl` is a required dependency for this.

- **Web Scraping:** The `requests` library is used to make HTTP requests to Wikipedia, and `BeautifulSoup4` is used to parse the HTML response and extract the necessary information (e.g., county data).

- **Number Conversion:** The `word2number` library is a specialized tool used to convert numbers written as words (e.g., "seventeen") into their integer or float equivalents.

## 2. Development Setup

- **Environment Management:** The project uses a Python virtual environment (`venv`) to manage dependencies. This ensures that the project's packages are isolated from the system's global Python installation, preventing conflicts.

- **API Key Management:** The API key for the Azure service is managed via an environment variable (`AZURE_API_KEY`). This is a security best practice that avoids hardcoding sensitive credentials directly into the source code.

- **Execution:** The entire process is orchestrated by a single script, `process_image.py`, which is run from the command line.

## 3. Key Dependencies

The project relies on the following external Python packages, which must be installed in the virtual environment:

- `requests`
- `pandas`
- `openpyxl`
- `word2number`
- `beautifulsoup4`
