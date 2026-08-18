import subprocess
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("GitHub Sprint Context")

@mcp.tool()
def get_open_tickets(repo: str) -> str:
    """
    Fetch open issues (tickets) from the specified GitHub repository.
    Example repo format: 'owner/repo'
    """
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--repo", repo, "--state", "open", "--json", "number,title,labels,updatedAt"], 
            capture_output=True, text=True, check=True
        )
        issues = json.loads(result.stdout)
        if not issues:
            return "No open tickets found."
        
        output = "Open Tickets:\n"
        for issue in issues:
            labels = [l['name'] for l in issue.get('labels', [])]
            output += f"- #{issue['number']}: {issue['title']} (Labels: {', '.join(labels)})\n"
        return output
    except subprocess.CalledProcessError as e:
        return f"Failed to fetch open tickets: {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_sprint_burndown(repo: str) -> str:
    """
    Get a summary of the current sprint's burndown progress.
    In this mocked implementation, we calculate it based on the ratio of closed vs open issues.
    """
    try:
        open_res = subprocess.run(
            ["gh", "issue", "list", "--repo", repo, "--state", "open", "--json", "number"], 
            capture_output=True, text=True, check=True
        )
        closed_res = subprocess.run(
            ["gh", "issue", "list", "--repo", repo, "--state", "closed", "--json", "number"], 
            capture_output=True, text=True, check=True
        )
        
        open_count = len(json.loads(open_res.stdout))
        closed_count = len(json.loads(closed_res.stdout))
        total = open_count + closed_count
        
        if total == 0:
            return "No sprint data found for this repository."
            
        percentage = (closed_count / total) * 100
        return (
            f"Sprint Progress Summary:\n"
            f"- Total Issues: {total}\n"
            f"- Closed: {closed_count}\n"
            f"- Open: {open_count}\n"
            f"- Burndown Completion: {percentage:.1f}%\n"
        )
    except subprocess.CalledProcessError as e:
        return f"Failed to calculate sprint burndown: {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def search_docs(query: str, repo: str) -> str:
    """
    Search for documentation, issues, or PRs matching a specific query in the repository.
    This provides critical context for the AI without needing copy-pasting.
    """
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--repo", repo, "--search", query, "--state", "all", "--json", "number,title,body"], 
            capture_output=True, text=True, check=True
        )
        items = json.loads(result.stdout)
        if not items:
            return f"No results found for query '{query}'."
            
        output = f"Search Results for '{query}':\n"
        for item in items[:5]: # limit to top 5 to save context window
            body_snippet = item.get('body', '')[:150].replace('\n', ' ') + '...'
            output += f"- #{item['number']}: {item['title']}\n  Snippet: {body_snippet}\n"
        return output
    except subprocess.CalledProcessError as e:
        return f"Search failed: {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Start the MCP server using stdin/stdout transport
    mcp.run()
