Verify that all dependencies and environment settings are correctly configured to run the recipe site tool. Work through each check in order and report what passes, what fails, and what still needs attention.

## Steps

1. **Python version** — run `python3 --version` and confirm it's 3.9 or higher. If not, tell the user they need to upgrade Python.

2. **uv installed** — run `uv --version`. If uv is not found, tell the user to install it: `curl -LsSf https://astral.sh/uv/install.sh | sh`

3. **Install dependencies** — run `uv sync` from the repo root. Report any errors.

4. **AWS credentials** — run `aws configure list`. If the aws CLI is not installed, suggest `brew install awscli`. If credentials are missing, explain the two options:
   - Run `aws configure` to set up credentials interactively
   - Or set environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION=us-east-1`

5. **S3 access** — run `aws s3 ls s3://www.matthewekent.com`. If this fails, tell the user the bucket is not accessible with their current credentials.

6. **Smoke test** — run `uv run python tool.py generate`. Confirm it exits without errors and that `output/index.html` exists.

Summarize: list each check with a pass/fail status, and give a clear next step for anything that failed.
