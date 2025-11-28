import sys
import os

# Add server directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

if __name__ == "__main__":
    sys.exit(pytest.main(["server/tests/test_main.py"]))
