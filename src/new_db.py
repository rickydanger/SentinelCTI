from datetime import datetime

from src.build_db import get_mca_telem_json
from src.config_db import save_config, make_entity_db_name, make_run_name
from src.write_json import get_json


def get_new_db(args, mitre_data, config):
    """Extract one JSON per entity. Returns combined records or None on error."""
    if not args.entities:
        print("Error: --entities is required when not using --last or --db")
        return None

    if not args.platform:
        print("Error: --platform is required when extracting new data.")
        return None

    if args.platform.lower() != "windows":
        print("Currently only 'windows' platform is supported.")
        return None

    print(f"Extracting data for: {args.entities}")

    combined = []
    db_paths = []

    for name in args.entities:
        db_name = make_entity_db_name(name)
        print(f"→ {name} → {db_name}")

        records = get_mca_telem_json([name], args.platform, mitre_data)
        get_json(records, db_name)
        print(f"  Database saved → {db_name} ({len(records)} records)")

        db_paths.append(db_name)
        combined.extend(records)

    run_name = make_run_name(args.entities)

    config["configs"][run_name] = {
        "mca_db_paths": db_paths,
        "entities": list(args.entities),
        "platform": args.platform,
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    config["last_run"] = run_name

    save_config(config)
    print(f"Config entry created → {run_name}")
    print(f"Files: {', '.join(db_paths)}")

    return combined
