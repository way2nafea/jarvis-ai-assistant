import os
import sys
import argparse
import threading
import time
from dotenv import load_dotenv

from core.voice import speak, listen
from core.registry import SkillRegistry
from core.engine import JarvisEngine
from gui.app import run_gui as run_gui_app


# ================== ENV SETUP ==================
load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    print("Error: GROQ_API_KEY not found.")
    sys.exit(1)


# ================== EXIT HANDLER ==================
def is_exit_command(cmd: str) -> bool:
    exit_words = {
        "exit",
        "quit",
        "shutdown",
        "close",
        "stop",
        "stop listening"
    }
    return cmd.strip().lower() in exit_words


# ================== MAIN JARVIS LOOP ==================
def jarvis_loop(pause_event, registry, args):
    jarvis = JarvisEngine(registry)

    if args.text:
        print("JARVIS: Jarvis Online. Ready for command (Text Mode).")
    else:
        speak("Jarvis Online. Ready for command.")

    while True:
        # Pause handling
        if pause_event.is_set():
            time.sleep(0.5)
            continue

        # Input
        if args.text:
            try:
                user_query = input("YOU: ").strip().lower()
            except EOFError:
                break
        else:
            user_query = listen().strip().lower()

        if not user_query or user_query == "none":
            continue

        # 🔴 GLOBAL EXIT (TOP PRIORITY)
        if is_exit_command(user_query):
            print("JARVIS: Shutting down.")
            if not args.text:
                speak("Shutting down. Goodbye, sir.")
            break

        # Pause check again
        if pause_event.is_set():
            continue

        # Direct commands
        direct_commands = [
            "open", "volume", "search", "create", "write", "read", "make",
            "who", "what", "when", "where", "how", "why", "thank", "hello"
        ]

        is_direct = any(cmd in user_query for cmd in direct_commands)

        # Wake-word filter
        if "jarvis" not in user_query and not is_direct:
            print(f"Ignored: {user_query}")
            continue

        clean_query = user_query.replace("jarvis", "").strip()

        try:
            print(f"Thinking: {clean_query}")
            response = jarvis.run_conversation(clean_query)

            if pause_event.is_set():
                continue

            if response:
                if args.text:
                    print(f"JARVIS: {response}")
                else:
                    speak(response)

        except Exception as e:
            print(f"Main Loop Error: {e}")
            if args.text:
                print("JARVIS: System error.")
            else:
                speak("System error.")


# ================== ENTRY POINT ==================
def main():
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant")
    parser.add_argument("--text", action="store_true", help="Run in text mode (no voice I/O)")
    args = parser.parse_args()

    # Load skills
    registry = SkillRegistry()
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    registry.load_skills(skills_dir)

    # Pause control
    pause_event = threading.Event()

    # Background Jarvis thread
    t = threading.Thread(
        target=jarvis_loop,
        args=(pause_event, registry, args),
        daemon=True
    )
    t.start()

    # GUI must run on main thread
    run_gui_app(pause_event)


if __name__ == "__main__":
    main()