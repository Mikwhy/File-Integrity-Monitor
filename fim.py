import os
import sys
import json
import hashlib
from datetime import datetime

BASELINE_FILE = "baseline.json"


def hash_file(path):
    """sha256 hash of file"""
    sha256 = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (IOError, PermissionError):
        return None


def get_files(path):
    """get all files from path (file or folder)"""
    files = []
    if os.path.isfile(path):
        files.append(os.path.abspath(path))
    elif os.path.isdir(path):
        for root, _, filenames in os.walk(path):
            for name in filenames:
                files.append(os.path.abspath(os.path.join(root, name)))
    return files


def load_baseline():
    """load existing baseline"""
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, 'r') as f:
            return json.load(f)
    return {"files": {}, "created": None, "updated": None}


def save_baseline(data):
    """save baseline to file"""
    with open(BASELINE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def cmd_init(paths):
    """create baseline from paths"""
    baseline = {"files": {}, "created": datetime.now().isoformat(), "updated": None}
    
    all_files = []
    for path in paths:
        all_files.extend(get_files(path))
    
    if not all_files:
        print("[!] no files found")
        return
    
    print(f"[*] hashing {len(all_files)} files...")
    
    for filepath in all_files:
        h = hash_file(filepath)
        if h:
            baseline["files"][filepath] = {
                "hash": h,
                "size": os.path.getsize(filepath),
                "added": datetime.now().isoformat()
            }
            print(f"  [+] {filepath}")
    
    save_baseline(baseline)
    print(f"\n[ok] baseline created: {len(baseline['files'])} files")


def cmd_add(paths):
    """add files to existing baseline"""
    baseline = load_baseline()
    
    if not baseline["files"]:
        print("[!] no baseline exists, run 'init' first")
        return
    
    all_files = []
    for path in paths:
        all_files.extend(get_files(path))
    
    added = 0
    for filepath in all_files:
        if filepath not in baseline["files"]:
            h = hash_file(filepath)
            if h:
                baseline["files"][filepath] = {
                    "hash": h,
                    "size": os.path.getsize(filepath),
                    "added": datetime.now().isoformat()
                }
                print(f"  [+] {filepath}")
                added += 1
    
    baseline["updated"] = datetime.now().isoformat()
    save_baseline(baseline)
    print(f"\n[ok] added {added} files")


def cmd_check():
    """check files against baseline"""
    baseline = load_baseline()
    
    if not baseline["files"]:
        print("[!] no baseline exists, run 'init' first")
        return
    
    print(f"[*] checking {len(baseline['files'])} files...\n")
    
    modified = []
    deleted = []
    ok = 0
    
    for filepath, data in baseline["files"].items():
        if not os.path.exists(filepath):
            deleted.append(filepath)
            continue
        
        current_hash = hash_file(filepath)
        if current_hash != data["hash"]:
            modified.append({
                "path": filepath,
                "old_hash": data["hash"][:16] + "...",
                "new_hash": current_hash[:16] + "..."
            })
        else:
            ok += 1
    
    # results
    if modified:
        print("[!] MODIFIED FILES:")
        for m in modified:
            print(f"  {m['path']}")
            print(f"    old: {m['old_hash']}")
            print(f"    new: {m['new_hash']}")
        print()
    
    if deleted:
        print("[!] DELETED FILES:")
        for d in deleted:
            print(f"  {d}")
        print()
    
    if not modified and not deleted:
        print("[ok] all files intact")
    
    print(f"\n--- summary ---")
    print(f"ok: {ok} | modified: {len(modified)} | deleted: {len(deleted)}")


def cmd_status():
    """show baseline status"""
    baseline = load_baseline()
    
    if not baseline["files"]:
        print("[!] no baseline exists")
        return
    
    print(f"baseline created: {baseline['created']}")
    print(f"last updated: {baseline['updated'] or 'never'}")
    print(f"files monitored: {len(baseline['files'])}")
    print()
    
    for filepath in list(baseline["files"].keys())[:10]:
        print(f"  {filepath}")
    
    if len(baseline["files"]) > 10:
        print(f"  ... and {len(baseline['files']) - 10} more")


def cmd_remove(paths):
    """remove files from baseline"""
    baseline = load_baseline()
    
    removed = 0
    for path in paths:
        abspath = os.path.abspath(path)
        if abspath in baseline["files"]:
            del baseline["files"][abspath]
            print(f"  [-] {abspath}")
            removed += 1
    
    baseline["updated"] = datetime.now().isoformat()
    save_baseline(baseline)
    print(f"\n[ok] removed {removed} files")


def cmd_update():
    """update hashes for all files (new baseline)"""
    baseline = load_baseline()
    
    if not baseline["files"]:
        print("[!] no baseline exists")
        return
    
    print(f"[*] updating {len(baseline['files'])} hashes...")
    
    updated = 0
    for filepath in list(baseline["files"].keys()):
        if os.path.exists(filepath):
            h = hash_file(filepath)
            if h and h != baseline["files"][filepath]["hash"]:
                baseline["files"][filepath]["hash"] = h
                baseline["files"][filepath]["size"] = os.path.getsize(filepath)
                updated += 1
                print(f"  [~] {filepath}")
    
    baseline["updated"] = datetime.now().isoformat()
    save_baseline(baseline)
    print(f"\n[ok] updated {updated} hashes")


def print_help():
    print("""
file integrity monitor

usage:
  fim.py init <path> [path2...]   create baseline from files/folders
  fim.py add <path> [path2...]    add files to baseline
  fim.py remove <path> [path2...] remove files from baseline
  fim.py check                    check files against baseline
  fim.py update                   update baseline with current hashes
  fim.py status                   show baseline info

examples:
  fim.py init C:\\Windows\\System32\\drivers
  fim.py init config.ini data.db
  fim.py add C:\\important\\newfile.txt
  fim.py check
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if cmd == "init" and args:
        cmd_init(args)
    elif cmd == "add" and args:
        cmd_add(args)
    elif cmd == "remove" and args:
        cmd_remove(args)
    elif cmd == "check":
        cmd_check()
    elif cmd == "update":
        cmd_update()
    elif cmd == "status":
        cmd_status()
    else:
        print_help()
