# ...existing code...
#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from market_research_crew.crew import MarketResearchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew and save the results into the repository knowledge/ folder.
    """
    inputs = {
        'product_idea': 'A mobile app that helps users track their improvement in hair count over time using AI-powered image analysis. Which implies that your medication works properly.',
    }

    try:
        # run the crew and capture the result
        crew = MarketResearchCrew().crew()
        result = crew.kickoff(inputs=inputs)

        # persist the result into knowledge/report.md
        from pathlib import Path
        import json
        out_dir = Path(__file__).resolve().parents[2] / "knowledge"
        out_dir.mkdir(parents=True, exist_ok=True)
        report_path = out_dir / "report.md"

        if isinstance(result, str):
            report_text = result
        elif isinstance(result, (dict, list)):
            report_text = json.dumps(result, indent=2)
        else:
            report_text = str(result)

        report_path.write_text(report_text, encoding="utf-8")
        print(f"Saved crew output to {report_path}")

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
# ...existing code...