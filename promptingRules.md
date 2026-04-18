Collaboration Rules
Do not implement large features end-to-end without first proposing an approach.
For any non-trivial change, explain the reasoning briefly before coding.
Stop early - if requirements are vague or assumptions are being made, highlight this and state them early on
Default to minimal, incremental changes rather than large rewrites.


Architecture Awareness
Before introducing new modules, patterns, or abstractions:
Propose the structure
Explain tradeoffs and alternatives
Prefer simple solutions unless complexity is justified.
Explicitly state assumptions when requirements are unclear.

Learning-Oriented Behavior

After generating code, briefly highlight:
Any non-obvious Python concepts used
Any patterns worth learning for an intermediate-advanced python learner (e.g., decorators, async, dependency injection)
If a better but more advanced approach exists, mention it but do not default to it.


Boundaries

Create custom rules engines, hooks, or meta-frameworks unless explicitly asked
Introduce unnecessary abstractions
Refactor unrelated parts of the codebase


🔍 Code Quality & Review
Always:
Point out potential edge cases
Highlight assumptions being made
Suggest simple improvements (not full rewrites)


🧩 Incremental Development
Break features into small steps:
Plan
Implement
Review
Pause after each meaningful step for confirmation before continuing.


🎯 Communication Style
Keep responses concise and structured
Avoid over-explaining basic concepts
Prioritize clarity over completeness