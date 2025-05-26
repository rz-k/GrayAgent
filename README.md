# AI Code Agent 🤖

An intelligent AI agent that writes code for you based on a simple natural language prompt.  
It can generate full applications in multiple programming languages (HTML, CSS, JS, Python, etc.) with minimal input.

Built with **Python**. Clean, simple, and powerful.

---

## 🚀 Installation

Clone the repository:

```
git clone https://github.com/your-username/ai-code-agent.git
cd ai-code-agent
```


Install [`uv`](https://github.com/astral-sh/uv) (if you don’t have it):

```
curl -Ls https://astral.sh/uv/install.sh | sh
```

Sync dependencies:

```
uv sync
```

Copy the environment configuration:

```
cp .env.example .env
```

---

## 🗂 Project Structure

```
.
├── core                  # Core logic of the AI agent
│   ├── code_generator.py     # Handles AI-based code generation
│   ├── file_extractor.py     # Extracts code parts from the AI response
│   ├── file_writer.py        # Writes generated code to the file system
│   ├── openai_client.py      # Handles communication with OpenAI API
│   ├── planner.py            # Plans the app structure before generation
│   └── prompts.py            # Manages all prompt templates
│
├── generated             # Output directory for generated applications
│   ├── app.js
│   ├── index.html
│   └── styles.css
│
├── logs                  # Stores generation logs and plans
│   └── plan.md
│
├── main.py               # Entry point of the application
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # Project documentation
└── uv.lock               # Lock file for package versions
```

---

## 💡 How to Use

### Option 1: CLI Prompt

Run the app and type your prompt:

```
uv run main.py
```

You will be asked for an idea (e.g. "Build a blog using Django").

The generated files will appear in the `generated/` folder.

---

### Option 2: Use as a Module

You can also import the agent and use it programmatically from another script:

Create a file named `run_prompt.py`:

```python
from main import run_agent_with_prompt

run_agent_with_prompt("Build a responsive landing page using HTML, CSS, and JavaScript")
```

Then run it:

```bash
uv run run_prompt.py
```

This will generate a fully working landing page in the `generated/` directory without any manual input.

---

## 📦 Example

```bash
$ uv run main.py

🧠 Enter your prompt:
Build a calculator web app with HTML, CSS, and JavaScript.

✅ Code has been generated in the `generated/` folder!

$ tree generated/
generated/
├── app.js
├── index.html
└── styles.css
```

Open `index.html` in your browser and enjoy your AI-generated app! 🎉

---