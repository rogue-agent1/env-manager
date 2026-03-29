import os
from env_manager import get_env, set_env, list_env, diff_env, snapshot, export_env
os.environ["TEST_ENV_MGR"] = "hello"
assert get_env("TEST_ENV_MGR") == "hello"
assert get_env("NONEXISTENT_XYZ", "def") == "def"
snap = snapshot()
set_env("TEST_ENV_MGR", "changed")
set_env("TEST_NEW_VAR", "new")
d = diff_env(snap)
assert "TEST_NEW_VAR" in d["added"]
assert "TEST_ENV_MGR" in d["changed"]
env_list = list_env("TEST_")
assert "TEST_ENV_MGR" in env_list
exp = export_env(["TEST_ENV_MGR"])
assert 'export TEST_ENV_MGR=' in exp
del os.environ["TEST_ENV_MGR"]
del os.environ["TEST_NEW_VAR"]
print("env_manager tests passed")
