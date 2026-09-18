

def read_multiline(prompt):
    while True:
        print(prompt)
        print("(Press Enter twice when done)")
        lines = []
        blank = 0
        while True:
            line = input()
            if line.strip() == "":
                blank += 1
                if blank == 2:
                    break
            else:
                blank = 0
            lines.append(line)

        text = "\n".join(lines).strip()
        if text:
            return text
        print("You didn't paste anything. Try again.\n")