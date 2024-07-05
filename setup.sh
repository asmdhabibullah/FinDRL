# #!/bin/bash

# Find and remove all directories
find . -type d -name ".venv" -exec rm -rf {} +
find . -type d -name "*.egg-info" -exec rm -rf {} +
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "requirements.txt" -exec rm -rf {} +

echo "__pycache__, .venv directories & requirements.txt file sre removed."

# Function to check the Python version
check_python_version() {
  REQUIRED_PYTHON="3.11"
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  
  # Compare versions using grep and awk
  compare_versions() {
    local version1=$(echo "$1" | awk -F. '{ printf("%d%03d%03d\n", $1,$2,$3); }')
    local version2=$(echo "$2" | awk -F. '{ printf("%d%03d%03d\n", $1,$2,$3); }')
    if [ "$version1" -lt "$version2" ]; then
      return 1
    else
      return 0
    fi
  }

  if compare_versions "$PYTHON_VERSION" "$REQUIRED_PYTHON"; then
    echo "Python version $PYTHON_VERSION is correct."
  else
    echo "Python version $PYTHON_VERSION is not supported. Please install Python $REQUIRED_PYTHON or higher."
    exit 1
  fi
}

# Function to create and activate a virtual environment based on OS
create_and_activate_venv() {
    # echo "Before sourcing:"
    # printenv  # Print environment variables before sourcing
    

  python3 -m venv .venv
  
  case "$OSTYPE" in
    linux-gnu*)
      echo "Detected Linux OS"
      source .venv/bin/activate
      ;;
    darwin*)
      echo "Detected macOS"
      source .venv/bin/activate
      ;;
    cygwin* | msys* | win32*)
      echo "Detected Windows OS"
      source .venv/Scripts/activate
      ;;
    *)
      echo "Unsupported OS"
      exit 1
      ;;
  esac
}

# Function to create requirements.txt if it does not exist
create_requirements_file_and_dependency() {
  if [ ! -f requirements.txt ]; then
    echo "Creating requirements.txt..."
    cat <<EOL > requirements.txt
ta>=0.11.0
click>=8.1.7
numpy>=2.0.0
pandas>=2.2.2
requests>=2.32.3
reportlab>=4.2.0
yfinance>=0.2.40
matplotlib>=3.9.0
backtesting>=0.3.3
setuptools>=70.1.0
python-dotenv>=1.0.1

EOL
  else
    echo "requirements.txt already exists."
  fi
}


# Check Python version
check_python_version

# Create and activate virtual environment
create_and_activate_venv

# Create requirements.txt if it does not exist
create_requirements_file_and_dependency

# Install required dependencies
pip install --upgrade pip
cat requirements.txt
pip install -q -r requirements.txt
pip freeze > requirements.txt
cat requirements.txt

# Create list of directories if they do not exist
directories=("app" "utils" "data" "fetcher" "analysis" "backtest" "strategies" "indicators" "results")

# Function to capitalize the first letter of a string
capitalize_first_letter() {
  first_letter=$(echo "$1" | cut -c1 | tr '[:lower:]' '[:upper:]')
  rest=$(echo "$1" | cut -c2-)
  echo "$first_letter$rest"
}

# Loop through each directory
for dir in "${directories[@]}"; do
  # Check if directory does not exist
  if [ ! -d "$dir" ]; then
    # Create the directory
    mkdir "$dir"
    echo "Created directory: $dir"
  fi

  # Capitalize the first letter of the directory name
  capitalized_dir=$(capitalize_first_letter "$dir")

  # Define the main Python file name with the first letter capitalized
  main_file="$dir/${capitalized_dir}.py"

  # Check if the Python file does not exist
  if [ ! -f "$main_file" ]; then
    # Create an empty Python file
    touch "$main_file"
    echo "Created file: $main_file"
  fi

  # Check if __init__.py file does not exist
  init_file="$dir/__init__.py"
  if [ ! -f "$init_file" ]; then
    # Create an empty __init__.py file
    touch "$init_file"
    echo "Created file: $init_file"
  fi
done


pip install -e .

echo "Then folow the steps to get the desire result!"

echo "1. Use the CLI command: (fetch-yahoo-data || fetch-polygon-data) SYMBOL --start-date YYYY-MM-DD --end-date YYYY-MM-DD"
echo "2. Use the CLI command: analysis --data-directory ./data/* "
echo "3. Use the CLI command: backtest --data-directory ./data/* file-number 0"

echo "Setup complete. To use the CLI app, run:"

