# CodeAnalyzer
An AI-assisted Python code reviewer combining AST-based static analysis with local LLM reasoning to detect and fix real-world code issues.</br>




This project is a hybrid static analysis + AI reasoning system designed to review Python code in a structured, reliable way.

Unlike generic AI code tools, this system:
<ul>
<li>First performs deterministic static analysis using Python’s AST.</li>
<li>Then uses a locally hosted language model to explain issues and suggest fixes.</li>
<li>Produces input-dependent, non-repetitive feedback.<li>
</ul>

<hr>

<h2>✨ Features</h2>

<h3>🔍 Static Code Analysis (AST-based)</h3>
<ul>
  <li>Distinguishes syntax errors from runtime and semantic issues</li>
  <li>Detects real-world problems such as:</li>
  <ul>
    <li>Shadowing Python built-ins (<code>max</code>, <code>list</code>, <code>dict</code>)</li>
    <li>Unsafe direct indexing (<code>arr[0]</code>)</li>
    <li>Inefficient loops (<code>range(len(...))</code>)</li>
    <li>Calls to undefined functions</li>
  </ul>
</ul>

<h3>🤖 AI Reasoning Layer</h3>
<ul>
  <li>Explains each detected issue in concrete technical terms</li>
  <li>Describes realistic failure scenarios</li>
  <li>Suggests Pythonic improvements</li>
  <li>Avoids generic or template-based responses</li>
</ul>

<h3>🛠️ Auto-Fix Code Generation</h3>
<ul>
  <li>Generates an improved version of the input code</li>
  <li>Preserves original intent</li>
  <li>Handles common edge cases</li>
  <li>Uses clean, idiomatic Python</li>
</ul>

<hr>

<h2>🧩 How It Works</h2>

<ol>
  <li><b>Input</b>: User pastes Python code</li>
  <li><b>AST Parsing</b>:
    <ul>
      <li>Validates syntax</li>
      <li>Extracts structure</li>
      <li>Detects concrete issues deterministically</li>
    </ul>
  </li>
  <li><b>AI Explanation</b>:
    <ul>
      <li>AI receives the code <i>and</i> detected issues</li>
      <li>Explains problems with context and reasoning</li>
    </ul>
  </li>
  <li><b>Auto-Fix</b>:
    <ul>
      <li>AI generates a corrected version of the code</li>
    </ul>
  </li>
</ol>
<hr>
<h2>🛠️ Tech Stack</h2>

<ul>
  <li><b>Language</b>: Python</li>
  <li><b>Static Analysis</b>: Python AST (<code>ast</code> module)</li>
  <li><b>AI Model</b>: Mistral (via Ollama)</li>
  <li><b>Architecture</b>: Rule-based analysis + constrained AI reasoning</li>
</ul>
