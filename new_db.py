from datetime import datetime

from build_db import get_mca_telem_json
from config_db import save_config, make_db_name
from write_json import get_json

def get_new_db(args, mitre_data, config):
    """Extract new data from MITRE ATT&CK and save it. Returns the data or None on error."""
    if not args.entities:
        print("Error: --entities is required when not using --last or --db")
        return None

    if not args.platform:
        print("Error: --platform is required when extracting new data.")
        return None

    if args.platform.lower() != "windows":
        print("Currently only 'windows' platform is supported.")
        return None

    db_name = make_db_name(args.entities)

    print(f"Extracting data for: {args.entities}")
    mca_telem_json = get_mca_telem_json(args.entities, args.platform, mitre_data)

    get_json(mca_telem_json, db_name)
    print(f"Database saved → {db_name}")

    config_name = db_name.replace("_db.json", "")

    config["configs"][config_name] = {
        "mca_db_path": db_name,
        "entities": args.entities,
        "platform": args.platform,
        "created": datetime.now().isoformat(timespec="seconds")
    }
    config["last_run"] = config_name

    save_config(config)
    print(f"Config entry created → {config_name}")

    return mca_telem_json