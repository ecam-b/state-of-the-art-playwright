import json
from pathlib import Path
from typing import Dict, Any


class DataProvider:
    """Utility to load test data from JSON files by domain and scenario."""
    
    @staticmethod
    def get_data(domain: str, scenario: str) -> Dict[str, Any]:
        """
        Load test data from data/{domain}.json for specific scenario.
        Returns dictionary with test data for the requested scenario.
        """
        file_path = Path(__file__).parent.parent / "data" / f"{domain}.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data[scenario]