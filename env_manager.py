#!/usr/bin/env python3
"""Environment variable manager. Zero dependencies."""
import os, sys, json

def get(key, default=None, type_fn=str):
    val = os.environ.get(key, default)
    if val is None: return None
    try: return type_fn(val)
    except: return default

def require(key):
    val = os.environ.get(key)
    if val is None:
        raise EnvironmentError(f"Required env var {key} not set")
    return val

def get_bool(key, default=False):
    val = os.environ.get(key, "").lower()
    if val in ("1", "true", "yes", "on"): return True
    if val in ("0", "false", "no", "off"): return False
    return default

def get_int(key, default=0):
    return get(key, default, int)

def get_list(key, sep=",", default=None):
    val = os.environ.get(key)
    if val is None: return default or []
    return [item.strip() for item in val.split(sep) if item.strip()]

def prefix_group(prefix):
    return {k[len(prefix):]: v for k, v in os.environ.items() if k.startswith(prefix)}

def dump(pattern=None):
    items = sorted(os.environ.items())
    if pattern:
        items = [(k, v) for k, v in items if pattern.lower() in k.lower()]
    return items

def mask(value, show=4):
    if len(value) <= show: return "***"
    return value[:show] + "*" * (len(value) - show)

def to_dotenv(env_vars):
    return "\n".join(f"{k}={v}" for k, v in sorted(env_vars.items()))

def from_dotenv(text):
    env = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'").strip('"')
    return env

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Env manager")
    p.add_argument("action", choices=["get","list","search"])
    p.add_argument("key", nargs="?")
    args = p.parse_args()
    if args.action == "get":
        print(os.environ.get(args.key, "(not set)"))
    elif args.action == "list":
        for k, v in dump()[:20]:
            print(f"{k}={mask(v)}")
    elif args.action == "search":
        for k, v in dump(args.key):
            print(f"{k}={v}")
