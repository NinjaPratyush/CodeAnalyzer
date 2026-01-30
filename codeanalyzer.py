
import ast
import json
import requests

BUILTIN_NAMES = set(dir(__builtins__))

def analyze_code(code: str):
    try:
        ast.parse(code)
    except SyntaxError as e:
        return {"syntax_valid": False, "error": str(e)}

    issues = []

    for node in ast.walk(ast.parse(code)):

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in BUILTIN_NAMES:
                    issues.append(f"Shadowing built-in name '{target.id}'")

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id not in BUILTIN_NAMES:
                issues.append(f"Call to undefined function '{node.func.id}'")

        elif isinstance(node, ast.Subscript):
            if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int):
                issues.append("Direct index access without bounds check")

        elif isinstance(node, ast.For):
            if (
                isinstance(node.iter, ast.Call)
                and isinstance(node.iter.func, ast.Name)
                and node.iter.func.id == "range"
                and node.iter.args
                and isinstance(node.iter.args[0], ast.Call)
                and isinstance(node.iter.args[0].func, ast.Name)
                and node.iter.args[0].func.id == "len"
            ):
                issues.append("Looping with range(len(...)) instead of direct iteration")

    return {
        "syntax_valid": True,
        "issues": sorted(set(issues))
    }


def explain_issues_with_ai(code: str, issues: list):
    prompt = f"""
You are a senior Python engineer reviewing code.

Code:
\"\"\"{code}\"\"\"

Issues:
{issues}

Explain each issue clearly with:
- Why it is a problem
- When it breaks
- What to do instead

Return JSON:
{{
  "explanations": [
    {{
      "issue": "",
      "why": "",
      "failure_example": "",
      "suggestion": ""
    }}
  ]
}}
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=90
        )
        return json.loads(res.json()["response"])["explanations"]
    except Exception:
        return []


def generate_fixed_code(code: str, issues: list):
    prompt = f"""
You are a senior Python engineer.

Given the following Python code and its issues,
generate an improved version that:

- Fixes the issues
- Uses Pythonic style
- Preserves original intent
- Handles edge cases

Original code:
\"\"\"{code}\"\"\"

Detected issues:
{issues}

Return ONLY the corrected Python code.
Do NOT include explanations.
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=90
        )
        return res.json()["response"]
    except Exception:
        return None


if __name__ == "__main__":
    print("\n=== AI Code Reviewer & Auto-Fixer ===")
    print("Paste Python code below. End with empty line.\n")

    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)

    user_code = "\n".join(lines)

    analysis = analyze_code(user_code)

    if not analysis["syntax_valid"]:
        print("\n❌ Syntax Error:")
        print(analysis["error"])
        exit()

    if not analysis["issues"]:
        print("\n✅ No issues detected.")
        exit()

    print("\n⚠️ Issues Found:")
    for issue in analysis["issues"]:
        print(f"- {issue}")

    explanations = explain_issues_with_ai(user_code, analysis["issues"])

    if explanations:
        print("\n🤖 AI Review:\n")
        for i, e in enumerate(explanations, 1):
            print(f"{i}. {e['issue']}")
            print(f"   Why: {e['why']}")
            print(f"   Failure: {e['failure_example']}")
            print(f"   Fix: {e['suggestion']}\n")

    fixed = generate_fixed_code(user_code, analysis["issues"])

    if fixed:
        print("\n✨ Suggested Improved Code:\n")
        print(fixed)




