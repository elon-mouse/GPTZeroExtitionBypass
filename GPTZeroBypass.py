import time
import random
import threading
from pathlib import Path

from pynput import keyboard
from pynput.keyboard import Controller, Key

# ========== Config ==========
PROMPT_PATH = Path(r"C:\Users\Path\to\your\prompt\prompt.txt")

# Typing behavior
WPM_MIN = 25            # lower bound of burst speed
WPM_MAX = 90            # upper bound of burst speed
BURST_SECONDS_MIN = 1.0
BURST_SECONDS_MAX = 6.0
CHAR_JITTER_MIN = 0.0   # extra random delay per char (seconds)
CHAR_JITTER_MAX = .08
PAUSE_AFTER_PUNCT = (0.08, 0.70)    # pause after , ; :
PAUSE_AFTER_SENTENCE = (0.25, 1.0)  # pause after . ! ?
RANDOM_PAUSE_CHANCE = 0.06  # chance to insert a random pause
RANDOM_PAUSE_RANGE = (0.08, 0.05)
# Rare “thinking” pause behavior
THINKING_PAUSE_CHANCE = 0.008        # ~0.8% chance per character (adjust as desired)
THINKING_PAUSE_RANGE = (4.5, 8.0)    # how long to pause, in seconds
# ===========================

kb = Controller()
stop_event = threading.Event()
type_thread = None
type_lock = threading.Lock()
current_text = ""


def read_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[Error] {PROMPT_PATH} not found.")
        return ""
    except Exception as e:
        print(f"[Error] Failed to read prompt: {e}")
        return ""


def _calc_char_delay(current_wpm: float) -> float:
    cps = (current_wpm * 5.0) / 60.0  # 1 word ~ 5 chars
    base = 1.0 / max(cps, 0.1)
    jitter = random.uniform(CHAR_JITTER_MIN, CHAR_JITTER_MAX)
    return base + jitter


def _natural_pause_for(ch: str) -> float:
    if ch in ",;:":
        return random.uniform(*PAUSE_AFTER_PUNCT)
    if ch in ".!?":
        return random.uniform(*PAUSE_AFTER_SENTENCE)
    return 0.0

def _maybe_random_pause():
    # Regular small hesitation pause
    if random.random() < RANDOM_PAUSE_CHANCE:
        time.sleep(random.uniform(*RANDOM_PAUSE_RANGE))

    # Rare long “thinking” pause
    if random.random() < THINKING_PAUSE_CHANCE:
        pause_duration = random.uniform(*THINKING_PAUSE_RANGE)
        print(f"[Pause] Thinking for {pause_duration:.1f} seconds...")
        for _ in range(int(pause_duration * 10)):
            if stop_event.is_set():
                break
            time.sleep(0.1)




def human_type(text: str):
    if not text:
        print("[Typing] No text to type.")
        return

    idx = 0
    n = len(text)

    while idx < n and not stop_event.is_set():
        burst_wpm = random.uniform(WPM_MIN, WPM_MAX)
        burst_end = time.time() + random.uniform(BURST_SECONDS_MIN, BURST_SECONDS_MAX)

        while idx < n and time.time() < burst_end and not stop_event.is_set():
            ch = text[idx]
            if ch == "\n":
                kb.press(Key.enter); kb.release(Key.enter)
            else:
                kb.type(ch)

            time.sleep(_calc_char_delay(burst_wpm))
            pause_len = _natural_pause_for(ch)
            if pause_len:
                time.sleep(pause_len)
            _maybe_random_pause()

            idx += 1

        if idx < n and not stop_event.is_set():
            time.sleep(random.uniform(0.05, 0.2))


def action_start_typing():
    global type_thread
    with type_lock:
        if type_thread and type_thread.is_alive():
            print("[Typing] Already running.")
            return
        stop_event.clear()
        text = current_text or read_prompt()
        if not text:
            return
        type_thread = threading.Thread(target=human_type, args=(text,), daemon=True)
        type_thread.start()
        print("[Typing] Started. Press Ctrl+Alt+S to stop.")


def action_stop_typing():
    stop_event.set()
    print("[Typing] Stop requested.")


def action_reload_prompt():
    global current_text
    current_text = read_prompt()
    if current_text:
        print(f"[Prompt] Reloaded from: {PROMPT_PATH}")
    else:
        print("[Prompt] Empty or missing prompt.")


def main():
    print("Human Prompt Typist")
    print(f"- Reading from: {PROMPT_PATH}")
    print("- Ctrl+Alt+R → Reload prompt from file")
    print("- Ctrl+Alt+P → Start typing")
    print("- Ctrl+Alt+S → Stop typing")

    # Initial read (non-blocking)
    action_reload_prompt()

    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+p': action_start_typing,
        '<ctrl>+<alt>+s': action_stop_typing,
        '<ctrl>+<alt>+r': action_reload_prompt
    }) as h:
        h.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
