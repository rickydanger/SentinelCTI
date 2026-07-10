import json

def get_json(mca_telemetry_json):

    # Convert to JSON string using json.dumps()
    json_string = json.dumps(mca_telemetry_json, indent=4, ensure_ascii=False)

    # Write to file
    with open("output.json", "w", encoding="utf-8") as f:
        f.write(json_string)