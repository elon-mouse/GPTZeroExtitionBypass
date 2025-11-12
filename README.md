# 🧠 Human Prompt Typist

A Python script that simulates **realistic human typing behavior** — complete with variable typing speed, random pauses, punctuation delays, and even rare “thinking pauses” that make it look like you’re stopping to think.

Ideal for demonstrations, AI prompt feeding, writing simulations, or creative automation projects.

---

## ✨ Features

- 🖋️ **Human-like typing**: Variable words-per-minute bursts and character jitter.
- ⏸️ **Realistic pauses**: Natural breaks after punctuation, sentences, or randomly mid-thought.
- 🧠 **Rare “thinking” pauses**: Occasionally stops for a few seconds as if the typist is thinking.
- 🔁 **Live prompt reloading**: Reload the text file without restarting the script.
- 🧩 **Global hotkeys**: Start, stop, or reload anytime using keyboard shortcuts.
- 🧵 **Thread-safe**: Safe concurrent operation with smooth interruption support.

---

## ⚙️ Configuration

At the top of the script, you’ll find all the tunable parameters:

| Variable | Description | Default |
|-----------|--------------|----------|
| `PROMPT_PATH` | Path to the `.txt` file to type from | `prompt.txt` |
| `WPM_MIN`, `WPM_MAX` | Random words-per-minute burst range | `25`, `90` |
| `BURST_SECONDS_MIN`, `BURST_SECONDS_MAX` | Duration of each typing burst | `1.0`, `6.0` |
| `CHAR_JITTER_MIN`, `CHAR_JITTER_MAX` | Extra random delay per character | `0.0`, `0.08` |
| `PAUSE_AFTER_PUNCT` | Pause range after punctuation (, ; :) | `(0.08, 0.50)` |
| `PAUSE_AFTER_SENTENCE` | Pause range after sentence end (. ! ?) | `(0.25, 0.60)` |
| `RANDOM_PAUSE_CHANCE` | Probability of inserting a small random pause | `0.06` |
| `RANDOM_PAUSE_RANGE` | Duration range of those random pauses | `(0.05, 0.08)` |
| `THINKING_PAUSE_CHANCE` | Probability of a long “thinking” pause | `0.008` *(~0.8%)* |
| `THINKING_PAUSE_RANGE` | Duration of “thinking” pause (seconds) | `(2.5, 6.0)` |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|-----------|---------|
| `Ctrl + Alt + P` | Start typing |
| `Ctrl + Alt + S` | Stop typing |
| `Ctrl + Alt + R` | Reload the prompt file |

---

## 🧩 Usage

1. **Install dependencies:**
   ```bash
   pip install pynput
Edit your text file:
Create or edit the prompt file you want to type from (default path in config).

Run the script:

```bash
python human_typist.py
Control it live:

Press Ctrl + Alt + P to start typing wherever your cursor is focused.

Press Ctrl + Alt + S to stop.

Press Ctrl + Alt + R to reload the prompt text while running.
```
🧠 Example Output
Console:
```bash
Human Prompt Typist
- Reading from: prompt.txt
- Ctrl+Alt+R → Reload prompt from file
- Ctrl+Alt+P → Start typing
- Ctrl+Alt+S → Stop typing
[Prompt] Reloaded from: prompt.txt
[Typing] Started. Press Ctrl+Alt+S to stop.
[Pause] Thinking for 4.8 seconds...
```

⚠️ Safety Notice
⚠️ This script simulates real keyboard input.

Make sure the window you want to type into is in focus before starting.

Use responsibly — this is intended for demos, writing automation, or creative use only.

🧰 Requirements
Python 3.8+

pynput library
(install with pip install pynput)
