#!/usr/bin/env python3
"""
Simple test runner for the real estate parser project.
"""
import sys
import os
import subprocess

def run_tests():
    """Run all tests using pytest."""
    try:
        # Add the project root to Python path
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        # Run pytest
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 'tests/', '-v'
        ], cwd=project_root)
        
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code) 