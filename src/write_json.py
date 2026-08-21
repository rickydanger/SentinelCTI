import json
import os

def get_json(mca_telemetry_json, filename="output.json"):
    # Make sure the data folder exists
    os.makedirs("data", exist_ok=True)

    # Build the full path inside the data folder
    filepath = os.path.join("data", filename)

    # Convert to JSON string using json.dumps()
    json_string = json.dumps(mca_telemetry_json, indent=4, ensure_ascii=False)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json_string)