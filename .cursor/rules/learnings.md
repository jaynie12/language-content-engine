# Python Learning Notes After Code Changes

When implementing or modifying Python code, always end the response with a short section titled `Learning Notes`.

## Learning Notes Requirements
Include 3 bullets max:
1. **Concepts used**: Any non-obvious Python concepts used in the change (e.g., decorators, async/await, context managers, typing protocols, dependency injection patterns).
2. **Patterns worth learning**: 1-3 intermediate/advanced patterns present in this change and why they matter.
3. **Advanced alternative (optional)**: Mention a more advanced approach only if relevant, but do not default to it unless explicitly requested.

## Style Constraints
- Keep it concise (4-8 lines total).
- Focus only on concepts actually used in the produced code.
- Do not add generic theory if the code does not demonstrate it.
- Do not expand into long tutorials unless the user asks.

## Collaboration Rules
1. Do not implement large features end-to-end without first proposing an approach.
2.  For any non-trivial change, explain the reasoning briefly before coding.
3. Stop early - if requirements are vague or assumptions are being made, highlight this and state them early on
4. Default to minimal, incremental changes rather than large rewrites.
5. If there is an opportunity for a hook, rule or skill point it out and we can work on it. 


## Architecture Awareness
Before introducing new modules, patterns, or abstractions:
Propose the structure
Explain tradeoffs and alternatives
Prefer simple solutions unless complexity is justified.
Explicitly state assumptions when requirements are unclear.


🎯 Communication Style
Keep responses concise and structured
Avoid over-explaining basic concepts
Prioritize clarity over completeness