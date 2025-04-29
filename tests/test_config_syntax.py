import os
import pytest

CONFIG_PATH = "scripts/examples/running.txt"

def test_config_file_exists():
    assert os.path.exists(CONFIG_PATH), f"Missing config file: {CONFIG_PATH}"

def test_no_unexpected_characters():
    with open(CONFIG_PATH) as f:
        for line in f:
            assert '\x00' not in line, "Null byte found in config"

def test_lines_not_too_long():
    with open(CONFIG_PATH) as f:
        for lineno, line in enumerate(f, 1):
            assert len(line) < 500, f"Line {lineno} too long ({len(line)} chars)"
