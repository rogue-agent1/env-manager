#!/usr/bin/env python3
"""env_manager - Environment variable manager with .env file support."""
import sys, os, re

def parse_env(text):
    result = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        result[key] = val
    return result

def to_env(env_dict):
    lines = []
    for k, v in sorted(env_dict.items()):
        if " " in str(v) or "=" in str(v) or '"' in str(v):
            v = f'"{v}"'
        lines.append(f"{k}={v}")
    return "\n".join(lines)

def interpolate(env_dict):
    result = dict(env_dict)
    for key, val in result.items():
        def replacer(m):
            ref = m.group(1)
            return result.get(ref, m.group(0))
        result[key] = re.sub(r'\$\{(\w+)\}', replacer, str(val))
    return result

def merge(*env_dicts):
    result = {}
    for d in env_dicts:
        result.update(d)
    return result

def validate(env_dict, required_keys):
    missing = [k for k in required_keys if k not in env_dict or not env_dict[k]]
    return missing

def mask_secrets(env_dict, secret_patterns=None):
    if secret_patterns is None:
        secret_patterns = ["password", "secret", "key", "token", "api"]
    result = {}
    for k, v in env_dict.items():
        if any(p in k.lower() for p in secret_patterns):
            result[k] = "***"
        else:
            result[k] = v
    return result

def test():
    env_text = """
# Database config
DB_HOST=localhost
DB_PORT=5432
DB_NAME="my database"
SECRET_KEY='abc123'
"""
    env = parse_env(env_text)
    assert env["DB_HOST"] == "localhost"
    assert env["DB_PORT"] == "5432"
    assert env["DB_NAME"] == "my database"
    assert env["SECRET_KEY"] == "abc123"
    output = to_env(env)
    reparsed = parse_env(output)
    assert reparsed["DB_HOST"] == "localhost"
    env2 = {"BASE": "/app", "LOG": "${BASE}/logs"}
    interp = interpolate(env2)
    assert interp["LOG"] == "/app/logs"
    m = merge({"A": "1"}, {"B": "2"}, {"A": "3"})
    assert m == {"A": "3", "B": "2"}
    missing = validate(env, ["DB_HOST", "MISSING_VAR"])
    assert missing == ["MISSING_VAR"]
    masked = mask_secrets(env)
    assert masked["SECRET_KEY"] == "***"
    assert masked["DB_HOST"] == "localhost"
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("env_manager: Env var manager. Use --test")
