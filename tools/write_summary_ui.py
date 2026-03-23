#!/usr/bin/env python3
import os
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    score_path = Path("tools/output/ui_score.txt")
    score = int(score_path.read_text().strip() or "0") if score_path.exists() else 0
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 🎨 Тесты UI (бонус)\n\n")
        s.write(f"**Баллы:** `{score} / 10`" + "\n\n")

if __name__ == "__main__":
    main()