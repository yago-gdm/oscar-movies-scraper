# Infinito API

## Running the application:

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment (PowerShell):

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

3. Install dependencies:

    ```bash
    pip install -r .\requirements
    ```

4. Run the application:

    ```bash
    .\venv\Scripts\Activate.ps1 ; python .\src\main.py
    ```

## Checking software documentation:

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your web browser.

## Pre-commit Hooks

This project uses pre-commit to ensure code quality and automate certain tasks before commits. Pre-commit helps run checks and formatting automatically, preventing unformatted or problematic code from being committed.

### Pre-commit Installation

1. **Install `pre-commit` using `pip`**:

   If you don’t have `pre-commit` installed yet, you can install it globally or within your project’s virtual environment:

   ```bash
   pip install pre-commit
   ```

2. **Install the pre-commit hooks in the repository:**:

   After installing pre-commit, you need to configure the hooks in the repository so that they are executed before commits:

   ```bash
   pre-commit install
   ```
    This command will create a Git hook that will automatically run pre-commit on all modified files whenever you make a commit.

3. **Manually run the hooks (optional)**:

   If desired, you can manually run pre-commit on all project files to check and fix issues before making a commit:

   ```bash
   pre-commit run --all-files
   ```
