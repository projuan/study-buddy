

def read_multiline(prompt, blanks_needed=2):
    hint = ("Press Enter twice when done" if blanks_needed == 2
            else "Press Enter on an empty line when done")
    while True:
        print(f"  {prompt}")
        print(f"  ({hint})")
        print()
        lines = []
        blank = 0
        while True:
            line = input()
            if line.strip() == "":
                blank += 1
                if blank == blanks_needed:
                    break
            else:
                blank = 0
            lines.append(line)

        text = "\n".join(lines).strip()
        if text:
            return text
        print("  You didn't type anything. Try again.\n")
