# -*- coding: utf-8 -*-
with open("dashboard/halloween_app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace if (scatterMetricSelect) { ... }
text = text.replace("if (scatterMetricSelect) {\n            scatterMetricSelect.addEventListener('change', () => renderRainRiceScatterPlot());\n        }",
                    "if (scatterMetricSelect) {{\n            scatterMetricSelect.addEventListener('change', () => renderRainRiceScatterPlot());\n        }}")

with open("dashboard/halloween_app.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed scatterMetricSelect braces")
