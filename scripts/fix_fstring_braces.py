# -*- coding: utf-8 -*-
import re

with open("dashboard/halloween_app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace any ${expr} where expr does not start with { with ${{expr}}
# But only inside the JS script or f-string
def repl(m):
    inner = m.group(1)
    if inner.startswith("{") and inner.endswith("}"):
        return m.group(0) # already doubled
    return "${{" + inner + "}}"

new_text = re.sub(r'\$\{([^{}\n]+)\}', repl, text)

with open("dashboard/halloween_app.py", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Replacement complete")
