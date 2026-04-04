Thinking tokens — Claude can use extended thinking for complex reasoning

Token limits & context windows — You're extracting YouTube transcripts. Transcripts can be long. Know your context window limits (Claude 3.5 Sonnet is 200k tokens). 
Structured outputs — The docs mention JSON mode / explicit format enforcement for when I  extract vocabulary as structured JSON. It's not enough to ask "give me JSON" — you need to be explicit about schema.

Few-shot examples — Showing Claude 2-3 examples of what you want before asking it to do the real task. 

Temperature & sampling — For deterministic outputs (vocabulary extraction), you want lower temperature. For creative tasks, higher. You'll tune this based on what breaks in production 

System vs user prompts

Use XML for specific inputs with prompt templates
