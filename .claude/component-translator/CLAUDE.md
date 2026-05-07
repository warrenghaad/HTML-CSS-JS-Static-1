# Local instructions for Claude Code

When the user is working inside `.claude/component-translator/` or asks
about the component-translator pipeline:

1. **Don't write components from this directory.** This is the planning
   layer. Components land in `src/components/` of the target project,
   driven by the foreman agent.

2. **Phase order matters.** Scout → Analyzer → Sourcer → Foreman. Don't
   skip phases unless the user explicitly says to. Each agent's input
   is the previous agent's `out/*.json`.

3. **Treat `/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID` as the
   canonical source.** Notion / Drive / Figma / AEM are
   cross-references; if they conflict with the local files, the local
   files win.

4. **The four agents are subagents, not slash commands.** Invoke them
   with the Agent tool by name (`scout-euclid`, `component-analyzer`,
   `component-sourcer`, `foreman-translator`).

5. **The foreman is the only agent permitted to write code.** If a
   user asks an earlier agent to "just go ahead and build it," stop
   and explain the read/write separation — it exists to keep agents
   from importing whatever they saw first.

6. **Token-first.** Color, spacing, and typography come from Figma
   variables via `get_variable_defs`, written to
   `src/styles/tokens.css`. Components reference tokens, never literals.

7. **Stop conditions.** If the scout finds < 5 artifacts, ask the user
   to verify the path. If the analyzer infers > 80 components in one
   pass, ask the user to scope down before sourcing.
