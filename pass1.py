from documentation import Documentation

def clean_input_file():
    with open("in.txt", "r") as infile, open("cleaned_file.txt", "w") as outfile:
        for line in infile:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            comment_pos = stripped_line.find('.')
            if comment_pos != -1:
                stripped_line = stripped_line[:comment_pos].strip()
            parts = stripped_line.split()
            if not parts:
                continue
            if parts[0].isdigit():
                parts = parts[1:]
            cleaned = ' '.join(parts)
            outfile.write(cleaned + '\n')

def pass1(input_file="cleaned_file.txt", intermediate_file="intermediate.txt", symtab_file="symtab.txt"):
    doc = Documentation()
    symtab = {}
    locctr = 0
    start_address = 0
    clean_input_file()

    with open(input_file, "r") as infile, open(intermediate_file, "w") as intfile:
        lines = infile.readlines()

        for idx, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('.'):  # Law el line fady aw fe comment (.)
                continue

            parts = line.split()
            label, opcode, operand = None, None, None
            is_indexed = False
            if len(parts) >= 3:
             label = parts[0] if not doc.is_instruction(parts[0]) else None
             opcode = parts[1] if label else parts[0]
             operand = ' '.join(parts[2:]) if label else ' '.join(parts[1:])

            if len(parts) == 3:
                label, opcode, operand = parts # [ 'FIRST', 'Clear', 'X' ]
            elif len(parts) == 2:
                if doc.is_directive(parts[0]) or parts[0].startswith('+') or doc.is_instruction(parts[0]):
                    opcode, operand = parts
                else:
                    label, opcode = parts
            elif len(parts) == 1:
                opcode = parts[0]

            # El Directive START....
            if idx == 0 and opcode == 'START':  # El if condition dy one time use!!!
                start_address = int(operand, 16)
                locctr = start_address
                intfile.write(f"{locctr:04X}  {line}\n")  # Write el intermidiate file le awl mra hna
                if label is not None:
                    # doc.set_prog_name(label)
                    Documentation.set_prog_name(label)
                continue

            if start_address == 0:  # Not a good practice to start the program with address 0. It is mostly reserved for
                                    # the system's boot process or OS loading routines.
                print("Error: START directive not found.")
                return

            # SYMTAB file da
            if label:
                if label in symtab:
                    print(f"Error: Duplicate label '{label}' at line {idx + 1}")
                else:
                    symtab[label] = locctr  # Assign new instance fel symtab object

            # Write el intermidiate file
            intfile.write(f"{locctr:04X}  {line}\n")

            # Opcode.....
            if opcode and opcode.startswith('+'):
                locctr += 4  # Format 4
            elif doc.is_instruction(opcode):
                if doc.get_format(opcode) == '3X':
                    locctr += 3
                else:
                    locctr += doc.get_format(opcode)
            elif doc.is_directive(opcode):
                if opcode == 'WORD':
                    if not operand:
                        print(f"Error: Missing operand for directive 'WORD' at line {idx + 1}")
                        continue
                    locctr += 3
                elif opcode == 'RESW':
                    if not operand:
                        print(f"Error: Missing operand for directive 'RESW' at line {idx + 1}")
                        continue
                    locctr += 3 * int(operand)
                elif opcode == 'RESB':
                    if not operand:
                        print(f"Error: Missing operand for directive 'RESB' at line {idx + 1}")
                        continue
                    locctr += int(operand)
                elif opcode == 'BYTE':
                    if not operand:
                        print(f"Error: Missing operand for directive 'BYTE' at line {idx + 1}")
                        continue
                    if operand.startswith("C'"):
                        locctr += len(operand) - 3
                    elif operand.startswith("X'"):
                        locctr += (len(operand) - 3) // 2
            elif opcode == 'END':
                break
            else:
                print(f"Warning: Unknown opcode '{opcode}' at line {idx + 1}")
                continue  # Skip invalid opcode lines

    # Write symtab file
    with open(symtab_file, "w") as symfile:
        for label, addr in symtab.items():
            symfile.write(f"{label} {addr:04X}\n")

    print(f"[PASS 1] Done. SYMTAB and intermediate file generated.")

if __name__ == "__main__":
    pass1()
 