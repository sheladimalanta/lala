---
name: writing-style
description: Shela's writing rules. Use when drafting, editing or reviewing any prose for people, including blog posts, newsletters, emails, social posts, docs and website copy. Do NOT use for code, commands or quoted source text.
---

# Writing style

## Rules

1. No em dashes, including "—" or similar characters. Use a comma, colon or ellipsis, or rewrite the sentence. A comma usually works.
2. No exclamation points.
3. Avoid metaphors, analogies and purple prose that a person wouldn't naturally say.
4. Avoid these words and phrases: fluff; crickets, as in "launch to crickets"; here's the thing; here's the kicker; void, as in "shouting into the void"; authentic; vanity metrics; pitch-slapped; through the noise; puzzle; lightning; magic; superpower or superpowers; superstar or superstars; double-edged sword; fast track; strike gold; secret weapon, weapons or arsenal; harness; thrive; skyrocket; soar, as in "watch your engagement soar"; savvy; transformative; buzzword; integrity; game-changer; forget, as in "forget vanity metrics"; evolve; unlock; unleash or unleashed the power of; elevate; delve; in a world of; your truth; thank you for it, as in "your audience will thank you for it".
5. Avoid these patterns:
   - Art-versus-science comparisons, such as "Storytelling isn't just an art. It's a science."
   - "I used to... then I..." stories.
   - "It's not about X... it's about Y" contrasts.
   - Statements overly concerned with ethics.
6. If a draft starts using any of these, rewrite it without them.

## Before handing over

Run the check script on the file and fix what it finds:

    python3 /Users/lala/lala/_skills/system/writing-style/scripts/check_writing.py <file>

If the prose only exists in the chat, save it to a file in the scratchpad first. The script checks rules 1, 2 and 4. Judge rules 3 and 5 yourself.
