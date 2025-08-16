# Product Context: Mortgage Data Automation

## 1. The Problem

The current workflow for processing mortgage application data from scanned documents is manual, time-consuming, and highly prone to error. Key challenges include:

- **Data Discrepancies:** Manually transcribing data from images leads to typos and inaccuracies, especially with long numbers and complex names.
- **Complex Business Logic:** The process requires a series of multi-step calculations and adherence to strict, non-intuitive formatting rules that are difficult for humans to apply consistently.
- **Time-Consuming Research:** A significant portion of the workflow involves manual web research to determine property tax assessment rates, which is a major bottleneck.
- **Inefficiency:** The manual process is slow, preventing the team from handling a high volume of documents efficiently.

## 2. How It Should Work

The ideal solution is a "one-click" script that automates the entire process. The user should be able to:

1.  Place an image file (like `Workload0001.jpg`) in a designated folder.
2.  Run a single Python script.
3.  Receive a perfectly formatted and calculated Excel file (`output.xlsx`) in seconds.

The system should handle all the complexity in the background, from AI-based text extraction to the final formatting, without requiring any manual intervention from the user.

## 3. User Experience (UX) Goals

- **Simplicity:** The user interaction should be minimal and straightforward. The complexity of the underlying process should be completely hidden.
- **Accuracy:** The primary goal is to eliminate manual errors. The final output must be 100% accurate according to the defined business rules.
- **Speed:** The automated process should reduce the time to process a single document from minutes or hours to just a few seconds.
- **Reliability:** The script should be robust enough to handle variations in AI model responses and potential web search failures, providing consistent results every time.
