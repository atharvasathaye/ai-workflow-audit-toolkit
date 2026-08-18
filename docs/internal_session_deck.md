# What Automated Tools are Good and Bad At In Our Sprint
*(Internal Session Deck / Talking Points)*

---

## Slide 1: The automation Reality Check
*How we actually performed with new code generation tools.*

**The Promise vs. The Reality**
- **Promise:** "Tools write your code for you."
- **Reality:** These tools act like eager junior developers who types really fast but doesn't know our business rules.

**The Numbers (From our Audit Dashboard)**
- **Where we won:** Generating test scaffolding, writing PR summaries, updating inline documentation. (Median time saved: 40%+)
- **Where we lost:** Deep refactoring, complex bug triaging without context. (Net-negative in 15% of cases).
- **The Rework Tax:** On average, 30% of generated code requires manual tweaking before it passes CI.

---

## Slide 2: The Context Problem & The MCP Solution
*Why copy-pasting is dead.*

**The Old Way:**
1. Open Jira/GitHub issue.
2. Copy the description.
3. Paste into Claude.
4. The tool asks for 3 more files.
5. You paste those files manually.

**The New Way (Model Context Protocol - MCP):**
1. We built a Python MCP Server that hooks directly into our GitHub Projects.
2. We tell the CLI tool: "Fix the bug described in Issue #45."
3. The tool *automatically* fetches the issue, reads our sprint burndown, and searches our docs.

**Takeaway for the Team:**
Don't fight the automation. Give it the tools it needs to see our world. Start using the MCP server today to stop being a "copy-paste engineer."
