from env_manager import get, get_bool, get_int, get_list, prefix_group, mask, from_dotenv, to_dotenv
import os
os.environ["TEST_VAR"] = "hello"
assert get("TEST_VAR") == "hello"
os.environ["TEST_BOOL"] = "true"
assert get_bool("TEST_BOOL") == True
os.environ["TEST_INT"] = "42"
assert get_int("TEST_INT") == 42
os.environ["TEST_LIST"] = "a,b,c"
assert get_list("TEST_LIST") == ["a","b","c"]
assert mask("secret123", 3) == "sec******"
env = from_dotenv("KEY=val\nOTHER=123")
assert env["KEY"] == "val"
print("Env manager tests passed")