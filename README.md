# FinDRL CLI Data Analysis

A CLI app to fetch financial data and analys.

## Prerequisites

- Python 3.11
- Git (optional, for cloning the repository)

## Installation

1. **Clone the repository** (if using Git):

   ```bash
   git clone https://github.com/asmdhabibullah/findrl.git
   cd findrl
   ```

2. **Download the repository** (if not using Git):

   Download the ZIP file from the repository, extract it, and navigate to the project directory.

3. **Create a `.env` file** in the root directory with your API keys:

   ```env
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   POLYGON_API_KEY=your_polygon_api_key
   ```

4. **Run the setup script**:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   This script will check your Python version, create `requirements.txt` if it does not exist, create a virtual environment, activate it, and install the required dependencies.

## Usage

1. **Activate the virtual environment**:

   - On Linux/macOS:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

2. **Run the CLI command**:

   ```bash
   fetch-data SYMBOL --start-date YYYY-MM-DD --end-date YYYY-MM-DD
   ```

   Replace `SYMBOL` with the stock symbol, and provide the appropriate start and end dates.

## License

This project is licensed under the MIT License.

````

### Steps to Run the Setup

1. **Clone the Repository** (if using Git):

   ```bash
   git clone https://github.com/yourusername/your_project.git
   cd your_project
````

2. **Download the Repository** (if not using Git):

   Download the ZIP file from the repository, extract it, and navigate to the project directory.

3. **Create the `.env` File**:

   Create a `.env` file in the root directory with your API keys:

   ```env
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   POLYGON_API_KEY=your_polygon_api_key
   ```

4. **Run the Setup Script**:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

5. **Activate the Virtual Environment**:

   - On Linux/macOS:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

6. **Run the CLI Command**:

   ```bash
   fetch-data SYMBOL --start-date YYYY-MM-DD --end-date YYYY-MM-DD
   ```

Replace `SYMBOL` with the stock symbol, and provide the appropriate start and end dates.
