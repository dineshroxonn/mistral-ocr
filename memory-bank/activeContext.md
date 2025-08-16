# Active Context: Finalizing Calculation Logic

## 1. Current Work Focus

The primary focus is to resolve the minor discrepancies between the script's output and the "actual" correct values provided by the user. The script is functional and produces a close result, but it is not yet perfect. The immediate task is to identify the root cause of these value differences without making major changes to the code, if possible.

## 2. Recent Changes

- **Memory Bank Initiated:** The entire Memory Bank structure has been created to document the project's context, goals, and technical implementation.
- **Flowchart Logic Implemented:** The `get_property_tax_info` function was added to the `process_image.py` script. This function now performs a web search to investigate the city and state, following the logic from the user-provided flowchart.
- **Robust Parsing:** The script was updated to handle web search failures (e.g., "404 Not Found" for "DeFoor, AL") and to follow a fallback procedure, making the process more resilient.

## 3. Next Steps

1.  **Analyze Value Discrepancies:** The immediate next step is to investigate the user's question: "without changing codes what could be the reason for the minor change in values?". This involves a careful review of the AI's raw output and the calculation logic.
2.  **Identify the Source of Truth:** Determine if the "actual" values are derived from a different set of reduction percentages or a different initial value that the AI may have misinterpreted.
3.  **Propose a Solution:** Based on the analysis, propose a final adjustment to the script or an explanation for the discrepancy.

## 4. Key Learnings & Patterns

- **AI Inconsistency:** The AI model's output can be inconsistent. It is crucial to design the data extraction schema to be as specific as possible to minimize ambiguity.
- **Importance of Fallbacks:** External dependencies like web searches can fail. The system must have robust fallback logic (as defined in the flowchart) to handle these cases gracefully.
- **Iterative Refinement:** The process of achieving a perfect output is iterative. It requires running the script, comparing the output to the desired result, and making precise adjustments to the logic.
