import subprocess
import time
import sys

def check_gh_cli():
    try:
        subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

ISSUES = [
    {"title": "Bug: Auth middleware drops token on retry", "body": "When a 401 occurs and the interceptor retries, the new token is not attached to the headers.", "label": "bug"},
    {"title": "Feature: Add export to CSV on Dashboard", "body": "Users need to be able to export their audit results to a CSV file from the main Streamlit dashboard.", "label": "enhancement"},
    {"title": "Refactor: Convert User dict to Pydantic Model", "body": "The current user dictionary pattern in the auth service is causing type errors. Let's refactor to use Pydantic models.", "label": "refactor"},
    {"title": "Docs: Update API documentation for v2.0", "body": "The /api/v2/metrics endpoint is missing from the swagger docs. Need to add docstrings to the controller.", "label": "documentation"},
    {"title": "Tech Debt: Clean up old feature flags", "body": "Remove the `USE_LEGACY_PARSER` feature flag as it's been rolled out to 100% of users for 3 months.", "label": "tech-debt"},
    {"title": "Bug: Streamlit chart renders off-screen on mobile", "body": "The altair chart in the dashboard overflows horizontally on screens narrower than 600px.", "label": "bug"},
    {"title": "Feature: MCP Support for Jira", "body": "Extend the MCP server to support Jira as a backend in addition to GitHub Projects.", "label": "enhancement"},
    {"title": "Testing: Add unit tests for MCP tool decorators", "body": "We currently lack coverage for the `get_open_tickets` tool logic.", "label": "testing"}
]

def create_issue(title, body, label):
    print(f"Creating issue: {title}")
    try:
        # We assume we are running this script inside a github repository directory
        subprocess.run([
            "gh", "issue", "create", 
            "--title", title, 
            "--body", body, 
            "--label", label
        ], check=True)
        time.sleep(1) # Rate limiting prevention
    except subprocess.CalledProcessError as e:
        print(f"Error creating issue: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--check-only':
        print("Checking dependencies...")
        return
        
    print("Seeding GitHub repository with mock backlog...")
    if not check_gh_cli():
        print("Error: GitHub CLI (gh) is not installed or not authenticated.")
        print("Run 'gh auth login' to authenticate.")
        sys.exit(1)
        
    for issue in ISSUES:
        create_issue(issue["title"], issue["body"], issue["label"])
        
    print("Done seeding backlog!")

if __name__ == "__main__":
    main()
