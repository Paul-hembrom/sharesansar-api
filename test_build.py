#!/usr/bin/env python3
"""
Test if the package builds correctly locally
"""
import subprocess
import sys
import os


def test_build():
    print("🧪 Testing local build...")

    # Clean previous builds
    for dir_name in ['build', 'dist', 'src/sharesansar_api.egg-info']:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)

    # Try to build
    try:
        result = subprocess.run([
            sys.executable, '-m', 'build'
        ], capture_output=True, text=True, check=True)

        print("✅ Build successful!")
        print("Output:", result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print("Error:", e.stderr)
        return False


if __name__ == "__main__":
    success = test_build()
    sys.exit(0 if success else 1)