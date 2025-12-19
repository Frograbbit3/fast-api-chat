#!/usr/bin/env bash
set -e

echo "Detecting platform and installing Python dependencies..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt &>/dev/null; then
        echo "Detected apt (Debian/Ubuntu)"
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv python3-distutils
    elif command -v dnf &>/dev/null; then
        echo "Detected dnf (Fedora/RHEL 8+)"
        sudo dnf install -y python3 python3-pip python3-virtualenv
    elif command -v yum &>/dev/null; then
        echo "Detected yum (CentOS/RHEL 7)"
        sudo yum install -y python3 python3-pip python3-virtualenv
    elif command -v pacman &>/dev/null; then
        echo "Detected pacman (Arch/Manjaro)"
        sudo pacman -Sy --noconfirm python python-pip
    elif command -v zypper &>/dev/null; then
        echo "Detected zypper (openSUSE)"
        sudo zypper install -y python3 python3-pip python3-virtualenv
    else
        echo "❌ No supported package manager found. Install Python manually."
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    if ! command -v brew &>/dev/null; then
        echo "Homebrew not found, installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        eval "$(/opt/homebrew/bin/brew shellenv)" # For Apple Silicon, adjust path if needed
    fi
    brew update
    brew install python
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Creating virtual environment..."
rm -rf .venv
python3 -m venv --upgrade-deps .venv

# Activate the venv for this script only
source .venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running setup..."
python tools/wipe.py
python serve.py
