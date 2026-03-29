#!/usr/bin/env python3
"""Environment variable manager with .env file support."""
import sys, os, re

def parse_env_file(content):
    env = {}
    for line in content.split(chr(10)):
        line = line.strip()
        if not line or line.startswith("#"): continue
        if "=" not in line: continue
        key, _, value = line.partition("=")
        key = key.strip(); value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        value = re.sub(r'\$\{(\w+)\}', lambda m: env.get(m.group(1), os.environ.get(m.group(1), "")), value)
        env[key] = value
    return env

def serialize_env(env):
    lines = []
    for k, v in sorted(env.items()):
        if " " in v or "'" in v: lines.append(f'{k}="{v}"')
        else: lines.append(f"{k}={v}")
    return chr(10).join(lines)

def merge_envs(*envs):
    result = {}
    for e in envs: result.update(e)
    return result

def validate_env(env, required):
    missing = [k for k in required if k not in env or not env[k]]
    return missing

def mask_secrets(env, patterns=None):
    patterns = patterns or ["KEY", "SECRET", "PASSWORD", "TOKEN"]
    masked = {}
    for k, v in env.items():
        if any(p in k.upper() for p in patterns):
            masked[k] = v[:3] + "***" if len(v) > 3 else "***"
        else: masked[k] = v
    return masked

def main():
    if len(sys.argv) < 2: print("Usage: env_manager.py <demo|test>"); return
    if sys.argv[1] == "test":
        content = 'DB_HOST=localhost' + chr(10) + 'DB_PORT=5432' + chr(10) + '# comment' + chr(10) + 'DB_NAME="my db"' + chr(10) + 'DB_URL=${DB_HOST}:${DB_PORT}'
        env = parse_env_file(content)
        assert env["DB_HOST"] == "localhost"
        assert env["DB_PORT"] == "5432"
        assert env["DB_NAME"] == "my db"
        assert env["DB_URL"] == "localhost:5432"
        s = serialize_env({"A": "1", "B": "hello world"})
        assert "A=1" in s; assert 'B="hello world"' in s
        m = merge_envs({"A": "1"}, {"A": "2", "B": "3"})
        assert m == {"A": "2", "B": "3"}
        missing = validate_env({"A": "1"}, ["A", "B"])
        assert missing == ["B"]
        masked = mask_secrets({"API_KEY": "sk-abc123", "HOST": "localhost"})
        assert "***" in masked["API_KEY"]; assert masked["HOST"] == "localhost"
        assert parse_env_file("") == {}
        assert parse_env_file("# only comments") == {}
        print("All tests passed!")
    else:
        env = parse_env_file(sys.stdin.read() if not sys.stdin.isatty() else "KEY=value")
        print(mask_secrets(env))

if __name__ == "__main__": main()
