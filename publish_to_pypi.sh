#!/bin/bash

echo "🚀 Publishing ShareSansar API to PyPI..."
echo "======================================"

echo
echo "📦 Step 1: Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

echo
echo "🔍 Step 2: Checking required files..."
if [ ! -f "requirements.txt" ]; then
    echo "⚠️  requirements.txt not found, creating one..."
    echo "requests>=2.25.0" > requirements.txt
    echo "pandas>=1.3.0" >> requirements.txt
    echo "beautifulsoup4>=4.9.0" >> requirements.txt
    echo "lxml>=4.6.0" >> requirements.txt
fi

echo
echo "🔧 Step 3: Installing build tools..."
pip install --upgrade build twine

echo
echo "🏗️ Step 4: Building package..."
python -m build

echo
echo "✅ Step 5: Checking build..."
twine check dist/*

echo
echo "📤 Step 6: Uploading to PyPI..."
twine upload dist/*

echo
echo "🎉 Done! Your package is now live on PyPI!"
echo "💻 Install with: pip install sharesansar-api"