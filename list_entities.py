from mitre_tech_patterns import list_all_malware, list_all_groups

def get_entities_list(args, mitre_data):
    """Handle -e malware / -e groups. Returns True if list mode was used."""
    if args.entities == ["malware"]:
        print("Listing all malware...\n")
        for name, mid in list_all_malware(mitre_data):
            print(f"{name:<45} | {mid}")
        return True

    if args.entities == ["groups"]:
        print("Listing all groups / MCA/APTs...\n")
        for name, gid in list_all_groups(mitre_data):
            print(f"{name:<45} | {gid}")
        return True

    return False