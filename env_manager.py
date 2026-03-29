#!/usr/bin/env python3
"""Environment variable manager. Zero dependencies."""
import os, sys, json

def get_env(key, default=None):
    return os.environ.get(key, default)

def set_env(key, value):
    os.environ[key] = str(value)

def list_env(prefix=None):
    result = {}
    for k, v in sorted(os.environ.items()):
        if prefix and not k.startswith(prefix): continue
        result[k] = v
    return result

def diff_env(snapshot):
    """Compare current env with a snapshot dict."""
    current = dict(os.environ)
    added = {k: v for k, v in current.items() if k not in snapshot}
    removed = {k: v for k, v in snapshot.items() if k not in current}
    changed = {k: (snapshot[k], current[k]) for k in current if k in snapshot and current[k] != snapshot[k]}
    return {"added": added, "removed": removed, "changed": changed}

def snapshot():
    return dict(os.environ)

def export_env(keys=None):
    """Generate export statements."""
    items = {k: os.environ[k] for k in (keys or os.environ)}
    return "\n".join(f'export {k}="{v}"' for k, v in sorted(items.items()))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = sys.argv[1]
        for k, v in list_env(p).items():
            print(f"{k}={v}")
    else:
        print(f"Environment has {len(os.environ)} variables")
