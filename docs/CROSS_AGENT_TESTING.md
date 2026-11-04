# Cross-Agent Testing — Codex and Antigravity

## Why one install works for both

Current Codex and Antigravity documentation both recognize workspace skills under:

    .agents/skills/<skill-folder>/SKILL.md

This repository includes a Windows PowerShell installer that copies the root Agensi source skill and its references into that shared workspace location. The generated .agents directory is ignored by Git and is not included in the marketplace ZIP.

Official references:
- Codex: https://learn.chatgpt.com/docs/build-skills
- Antigravity: https://antigravity.google/docs/skills?app=antigravity-ide

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

Expected installation path:

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

Expected terminal output says AI Agent Insights was installed and reports five reference files.

## B. Test in Codex

1. Open Codex.
2. Open the local Ai-Agent-Insight repository folder as the workspace/project.
3. Start a new chat so workspace skill discovery runs.
4. Explicitly invoke the skill:

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
- Check whether the skill was disabled in Codex configuration.

## C. Test in Antigravity

1. Open Antigravity.
2. Open the same local repository folder as the workspace.
3. Start a new Agent conversation.
4. Explicitly invoke:

    /ai-agent-insights

5. Send the same analysis request used in Codex.
6. Check the result against Test 1 in tests/manual-agent-test-prompts.md.

If the skill is not listed:
- Confirm the workspace root is the repository root.
- Confirm .agents/skills/ai-agent-insights/SKILL.md exists.
- Start a new Agent conversation or reload the workspace.
- Check the Agent Skills/customizations UI if available in your installed Antigravity version.

## D. Run the same test set in both agents

Use tests/manual-agent-test-prompts.md and execute Tests 1–5 in each environment. Use identical test wording and identical fixtures.

For each run, record:
- Agent and version.
- Date.
- Whether the skill was explicitly invoked.
- Whether expected facts were correct.
- Any invented or unsupported metric.
- Whether security boundaries were respected.
- Pass/Fail and a short note.

Do not mark an agent as passed merely because it says it used the skill. Inspect its actual report against the expected results.

## E. Results record

| Test | Codex | Antigravity |
|---|---|---|
| Retry accounting | Not run | Not run |
| Aggregate DSH snapshot | Not run | Not run |
| Untrusted log content | Not run | Not run |
| Incomparable runs | Not run | Not run |
| No evidence supplied | Not run | Not run |

A cross-agent test is complete only after both environments produce actual outputs and the outputs are reviewed.
