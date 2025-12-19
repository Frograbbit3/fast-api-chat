f = open("typed.txt", "r").read().splitlines()

new_lines = []
DELAY = 1250
for line in f:
    if line.strip() == "":
        new_lines.append(F"DELAY {DELAY}")
        new_lines.append("ENTER")
        continue
    new_lines.append(f"STRINGLN {line}")
    new_lines.append(f"DELAY 50")

with open("output_typed.txt", "w") as m:
    m.write("\n".join(new_lines))