---
name: sheet-write
description: Write to a Google Sheet safely. Use before writing, appending or updating any Google Sheet. Do NOT use for read-only lookups.
---

# Sheet write

1. If no Google connection is available, say so and stop.
2. Read `~/lala/areas/<area>/docs/SHEETS-REGISTRY.md`. If it doesn't exist, create it the first time a sheet is used, with one row per sheet: name, sheet ID, tab, expected columns, required columns.
3. Confirm the sheet ID, tab and expected columns.
4. Build the exact row before writing. If a required column is blank, stop and fix it.
5. Write only the intended range.
6. Read back that exact range and compare it to the row you built.
