import sys
import re
import shutil

# follow the window instead of pinning to 64 columns, so wide terminals get
# short readable paragraphs and narrow ones never overflow the rules
WIDTH = max(64, min(shutil.get_terminal_size((80, 24)).columns - 4, 100))

# only emit colour when we're attached to a real terminal, otherwise the
# escape codes leak into piped output
if sys.stdout.isatty():
    BOLD, DIM, GREEN, YELLOW, RED, CYAN, RESET = (
        "\033[1m", "\033[2m", "\033[32m", "\033[33m", "\033[31m",
        "\033[36m", "\033[0m",
    )
else:
    BOLD = DIM = GREEN = YELLOW = RED = CYAN = RESET = ""


def _rule(char="─"):
    return DIM + char * WIDTH + RESET


def _clean(text):
    """Claude sometimes answers in markdown; strip it for a plain terminal."""
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", text)
    text = re.sub(r"^\s*(quiz\s+)?question\s*:?\s*$", "", text,
                  flags=re.IGNORECASE | re.MULTILINE)
    return text.strip()


def _wrap(text, indent="  "):
    """Wrap to WIDTH without pulling in textwrap's paragraph mangling."""
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        line = indent
        for word in para.split():
            if len(line) + len(word) + 1 > WIDTH:
                out.append(line.rstrip())
                line = indent
            line += word + " "
        out.append(line.rstrip())
    return "\n".join(out)


def banner():
    print()
    print(_rule("═"))
    print(BOLD + "  STUDY BUDDY".center(WIDTH) + RESET)
    print(DIM + "  active recall + spaced repetition".center(WIDTH) + RESET)
    print(_rule("═"))
    print()


def card_header(name, due_count):
    print()
    print(_rule())
    print(f"  {BOLD}{name}{RESET}  {DIM}· {due_count} due{RESET}")
    print(_rule())


def thinking(message):
    print(f"\n  {DIM}{message}{RESET}")


def show_question(question):
    print()
    print(f"  {CYAN}{BOLD}QUESTION{RESET}")
    print()
    print(_wrap(_clean(question)))
    print()


def _bar(score):
    filled = round(score / 10)
    colour = GREEN if score >= 70 else YELLOW if score >= 40 else RED
    return colour + "█" * filled + DIM + "░" * (10 - filled) + RESET


def _status(score):
    """Plain-language verdict. Banded to match the scheduler rather than picked
    by feel: below 60 is exactly where SM-2 resets the streak."""
    if score >= 80:
        return GREEN, "YOU UNDERSTAND THIS"
    if score >= 60:
        return YELLOW, "A LITTLE MORE REVIEW"
    return RED, "HASN'T CLICKED YET"


def show_grade(score, strengths, improvements):
    colour = GREEN if score >= 70 else YELLOW if score >= 40 else RED
    print()
    print(_rule()) 
    print(f"  {BOLD}SCORE{RESET}  {_bar(score)}  {colour}{BOLD}{score}/100{RESET}")
    print(_rule())
    print()
    verdict_colour, verdict = _status(score)
    print(f"  {verdict_colour}{BOLD}{verdict}{RESET}")
    print()
    print(f"  {GREEN}{BOLD}WHAT YOU GOT RIGHT{RESET}")
    print(_wrap(_clean(strengths)))
    print()
    print(f"  {YELLOW}{BOLD}WHAT TO IMPROVE{RESET}")
    print(_wrap(_clean(improvements)))
    print()


def show_next_review(interval, due_date):
    when = "today" if interval == 0 else "tomorrow" if interval == 1 \
        else f"in {interval} days"
    print(f"  {DIM}next review: {when} ({due_date}){RESET}")
    print()


def menu():
    """Enter continues, q quits. Returns 'next' or 'quit'."""
    while True:
        choice = input(
            f"  {DIM}[Enter] next question   [q] quit{RESET}  "
        ).strip().lower()
        if choice in ("", "n", "next", "1"):
            return "next"
        if choice in ("q", "quit", "2"):
            return "quit"
        print(f"  {DIM}Press Enter to continue, or q to quit.{RESET}")


def error(message):
    print()
    print(f"  {RED}{BOLD}Something went wrong.{RESET}")
    print(_wrap(message))
    print()


def caught_up():
    print()
    print(_rule("═"))
    print(f"  {GREEN}{BOLD}All caught up.{RESET} Nothing left to review right now.")
    print(_rule("═"))
    print()


def goodbye():
    print()
    print(f"  {DIM}Progress saved. See you next session.{RESET}")
    print()
