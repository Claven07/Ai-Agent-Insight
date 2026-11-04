# Cross-Agent Testing — Codex and Antigravity

## Why one install works for both

OpenAI Codex and Google Antigravity both document workspace skills under:

    .agents/skills/<skill-folder>/SKILL.md

Official references:
- Codex skills: https://learn.chatgpt.com/docs/build-skills
- Antigravity Agent Skills: https://antigravity.google/docs/skills?app=antigravity-ide

The PowerShell installer copies the repository's root Agensi source skill and its supporting references into that shared workspace path. The generated .agents directory is ignored by Git and is not included in the marketplace ZIP.

## A. Prepare the local repository

Open Windows PowerShell 5.1 or newer.

If the repository is not already on your PC:

    cd $HOME\Projects
    git clone https://github.com/Claven07/Ai-Agent-Insight.git
    cd Ai-Agent-Insight

If it is already cloned, open PowerShell in its local folder and update it:

    git pull origin main

Run the installer:

    .\scripts\install-workspace-skill.ps1

Expected installed path:

    .agents/
    └── skills/
        └── ai-agent-insights/
            ├── SKILL.md
            └── references/
                ├── metrics-analysis.md
                ├── bottleneck-detection.md
                ├── llm-failure-analysis.md
                ├── report-standards.md
                └── input-normalization.md

Expected terminal output:
- "AI Agent Insights installed for this workspace."
- Location ending in .agents\skills\ai-agent-insights.
- Reference files: 5.

## B. Test in OpenAI Codex

1. Open Codex.
2. Open the local Ai-Agent-Insight repository folder as the workspace/project.
3. Start a new chat so workspace skill discovery runs.
4. Explicitly invoke the skill by typing:

    $ai-agent-insights

5. Then send this request:

    Use AI Agent Insights to analyze examples/sample-session-failure.json.
    Do not modify any files. Produce the standard Run Performance Report.
    Show tool attempts separately from logical tool operations, explain the
    search_code timeout and correlated retry, and state all data limitations.

6. Check the result against Test 1 in tests/manual-agent-test-prompts.md.

If the skill is not listed:
- Confirm the opened workspace is the repository root.
- Confirm .agents/skills/ai-agent-insights/SKILL.md exists.
- Start a fresh Codex chat or restart Codex.
- Confirm the installed skill has not been disabled in Codex configuration.

Codex documents explicit invocation using $skill-name. Its skill discovery can also choose a skill implicitly when its description matches.

## C. Test in Google Antigravity IDE

1. Open Antigravity.
2. Open the same local repository folder as the workspace.
3. Start a new Agent conversation.
4. Ask:

    What skills are available in this workspace?

5. Confirm that ai-agent-insights appears in the available skills.
6. Then send:

    Use the AI Agent Insights skill to analyze
    examples/sample-session-failure.json. Do not modify any files.
    Produce the standard Run Performance Report. Show tool attempts
    separately from logical tool operations, explain the search_code
    timeout and correlated retry, and state all data limitations.

7. Check the result against Test 1 in tests/manual-agent-test-prompts.md.

Antigravity IDE's documented interface uses skill discovery and semantic selection; mention the skill by name in your request. Do not assume slash-command invocation in the IDE. (The Antigravity CLI has a /skills listing command, which is distinct from the IDE.)

If the skill is not listed:
- Confirm the workspace root is the repository root.
- Confirm .agents/skills/ai-agent-insights/SKILL.md exists.
- Start a new Agent conversation or reload the workspace.
- Check the Agent Skills/customizations UI if available in your installed Antigravity version.

## D. Run the same test set in both agents

Use tests/manual-agent-test-prompts.md and execute Tests 1–6 in each environment. Use identical test wording and identical fixtures. Invoke explicitly as described above.

For each run, record:
- Agent and version.
- Date.
- Whether the skill was discovered and explicitly invoked.
- Whether expected facts were correct.
- Any invented or unsupported metric.
- Whether security boundaries were respected.
- Pass/Fail and a short note.

Do not mark an agent as passed merely because it says it used the skill. Inspect its actual report against the test's expected results.

## E. Results record

| Test | Codex | Antigravity |
|---|---|---|
| Retry accounting | Not run | Not run |
| Concurrency / missing correlation | Not run | Not run |
| Aggregate DSH snapshot | Not run | Not run |
| Untrusted log content | Not run | Not run |
| Incomparable runs | Not run | Not run |
| No evidence supplied | Not run | Not run |

A cross-agent test is complete only after both environments produce actual outputs and the outputs are reviewed.
