# Engineering Tooling Measurement Protocol

**Objective:** Establish a statistically significant, unbiased baseline of engineering task velocity and quality before and after introducing new automated coding tools.

## 1. Task Selection (The "Instrumented 15")
We selected 15 recurring engineering and project management tasks that occur in every sprint. These tasks avoid rare "hero" debugging sessions and focus on the day-to-day grind.

**Categories:**
1. **Scaffolding:** Generating boilerplate, unit test scaffolding, database migration shells.
2. **Documentation:** Writing PR descriptions, inline docstrings, release notes.
3. **Refactoring:** Converting classes to dataclasses, abstracting repeated logic, renaming variables across files.
4. **Project Management:** Triaging bug reports, writing acceptance criteria, mapping dependencies.
5. **Context Gathering:** Finding the right file for a feature, understanding a legacy function, summarizing sprint burndown.

## 2. Methodology
To control for the "learning effect" (where doing a task a second time is naturally faster):
1. **Control Group (Manual):** Tasks are performed manually during Sprint 1. Time is tracked using a stopwatch.
2. **Experimental Group (Assisted):** Similar (but distinct) tasks from the same categories are performed in Sprint 2 using new code generation tools.
3. **The MCP Intervention:** In Sprint 3, the CLI tool is equipped with a custom Model Context Protocol (MCP) server that connects directly to our GitHub Projects/Jira backlog.

## 3. Metrics Tracked
- **Median Time per Task (Minutes):** Time from starting the task to opening the PR or updating the ticket.
- **Rework Rate (%):** The percentage of tasks requiring manual correction after the the tool generated the output.
- **Net-Negative Flag (Boolean):** Did the tool generate invalid code or break something so badly that it took *longer* to fix than doing it manually?
- **Quality Score (1-5):** Subjective score (1 = Unusable, 5 = Ready for production without edits).

## 4. Execution Steps
1. **Record Baseline:** Engineers log time in the `audit_results.csv` sheet for 5 days.
2. **Introduce Assistants:** Teams get licenses.
3. **Record Tool-Assisted Passes:** Repeat logging for 5 days.
4. **Deploy MCP:** Hook the CLI tool into our internal context.
5. **Final Evaluation:** Run the Streamlit dashboard to generate the scorecard.
