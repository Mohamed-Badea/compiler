from documentation import Documentation


def get_operand_value(operand, symtab):
    if operand is None:
        return 0
    if operand in symtab:
        return symtab[operand]
    if operand.startswith('X\'') and operand.endswith('\''):
        return int(operand[2:-1], 16)
    if operand.startswith('C\'') and operand.endswith('\''):
        return ''.join([f"{ord(c):02X}" for c in operand[2:-1]])
    try:
        return int(operand)
    except ValueError:
        return 0


def format_object_code(opcode, operand, symtab, doc):
    ni = 3  # aftred simple addressing
    x = b = p = e = 0  # khaly el flags 0 dlw2ty
    displacement = 0

    if opcode.startswith('+'):
        e = 1
        opcode = opcode[1:] 
    op = doc.INSTRUCTIONS.get(opcode.upper())
    if not op:
        return ''

    op_dec = int(op['opcode'], 16)
    format_type = 4 if e else op['format']

    if format_type == 1:
        return f"{op_dec:02X}"
    elif format_type == 2:
        r1, r2 = (operand.split(',') + ['0'])[:2]
        r1_val = doc.REGISTERS.get(r1.upper(), 0)
        r2_val = doc.REGISTERS.get(r2.upper(), 0)
        return f"{op_dec:02X}{r1_val:01X}{r2_val:01X}"
    elif format_type == '3X':
    # operand expected: R1,R2,R3,R4
     regs = (operand.split(',') + ['0', '0', '0', '0'])[:4]
     r_vals = [doc.REGISTERS.get(r.strip().upper(), 0) for r in regs]
    # Construct 3 bytes: opcode + r1<<4|r2 + r3<<4|r4
     return f"{op_dec:02X}{(r_vals[0]<<4 | r_vals[1]):02X}{(r_vals[2]<<4 | r_vals[3]):02X}"

    elif format_type in [3, 4]:
        if operand and ',' in operand and 'X' in operand.upper():
            x = 1
            operand = operand.split(',')[0]

        address = symtab.get(operand, 0)

        # Format 3 w 4: opcode 6 bits w ni 2 bits w xbpe 4 w a5eran w lays a5eran displacement/address
        ni_bits = ni
        xbpe = (x << 3) | (b << 2) | (p << 1) | e
        op_code = (op_dec & 0xFC) | ni_bits
        if format_type == '3X':
         return f"{op_dec:02X}{(r_vals[0]<<4 | r_vals[1]):02X}{(r_vals[2]<<4 | r_vals[3]):02X}"

        if format_type == 3:
            disp = address & 0xFFF
            return f"{op_code:02X}{xbpe << 4 | ((disp >> 8) & 0xF):01X}{disp & 0xFF:02X}"
        else:
            return f"{op_code:02X}{xbpe << 4 | ((address >> 16) & 0xF):01X}{(address >> 8) & 0xFF:02X}{address & 0xFF:02X}"

    return ''


def pass2(intermediate_file="intermediate.txt", symtab_file="symtab.txt", obj_file="output.obj",
          lst_file="listing.lst"):

    doc = Documentation()
    symtab = {}
    modification_records = []

    with open(symtab_file, "r") as symfile:
        for line in symfile:
            label, addr = line.strip().split()
            symtab[label] = int(addr, 16)

    with open(intermediate_file, "r") as intfile, \
            open(obj_file, "w") as obj, \
            open(lst_file, "w") as lst:

        lines = intfile.readlines()

        # program_name = doc.get_prog_name()
        program_name = Documentation.get_prog_name()
        start_address = int(lines[0].split()[0], 16)
        program_length = int(lines[-1].split()[0], 16) - start_address
        text_records = []
        current_text = ""
        current_start = None

        obj.write(f"H^{program_name:<6}^{start_address:06X}^{program_length:06X}\n")

        current_loc = start_address
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue

            loc = int(parts[0], 16)
            label, opcode, operand = None, None, None

            if len(parts) == 4:
                _, label, opcode, operand = parts
            elif len(parts) == 3:
                _, opcode, operand = parts
            elif len(parts) == 2:
                _, opcode = parts

            if opcode == 'START':
                current_loc = loc
                continue
            if opcode == 'END':
                break

            object_code = ''
            if doc.is_instruction(opcode) or opcode.startswith('+'):
                object_code = format_object_code(opcode, operand, symtab, doc)
                # Check for format 4 instruction that needs modification record
                if opcode.startswith('+'):
                    # Format 4 instruction - need M record
                    m_record_loc = current_loc + 1  # Address starts after opcode and flags
                    m_record_length = 5  # 5 half-bytes (10 nibbles) to modify
                    modification_records.append((m_record_loc, m_record_length))
            elif opcode == 'BYTE':
                if operand.startswith('C\''):
                    object_code = ''.join([f"{ord(c):02X}" for c in operand[2:-1]])
                elif operand.startswith('X\''):
                    object_code = operand[2:-1]  # X'87'
            elif opcode == 'WORD':
                object_code = f"{int(operand):06X}"

            lst.write(f"{loc:04X}\t{label or ''}\t{opcode}\t{operand or ''}\t{object_code}\n")

            if object_code:
                if current_start is None:
                    current_start = loc
                current_text += object_code
                if len(current_text) >= 60:
                    text_records.append((current_start, current_text))
                    current_text = ""
                    current_start = None

            # Update current location counter
            if opcode in doc.INSTRUCTIONS:
                if opcode.startswith('+'):
                    current_loc += 4  # Format 4 instruction
                else:
                    if doc.get_format(opcode) == '3X':
                        current_loc += 3
                    else:
                        current_loc += doc.INSTRUCTIONS[opcode]['format']
                    
            elif opcode == 'WORD':
                current_loc += 3
            elif opcode == 'BYTE':
                if operand.startswith('C\''):
                    current_loc += len(operand) - 3  # Length of string
                elif operand.startswith('X\''):
                    current_loc += (len(operand) - 3) // 2  # Each pair of chars is one byte
            elif opcode == 'RESW':
                current_loc += 3 * int(operand)
            elif opcode == 'RESB':
                current_loc += int(operand)

        if current_text:
            text_records.append((current_start, current_text))

        for start, record in text_records:
            length = len(record) // 2
            obj.write(f"T^{start:06X}^{length:02X}^{record}\n")

        # Write modification records
        for m_loc, m_len in modification_records:
            obj.write(f"M^{m_loc:06X}^{m_len:02X}\n")

        end_address = f"{start_address:06X}"
        obj.write(f"E^{end_address}\n")

    print("[PASS 2] Object and listing files generated successfully.")


if __name__ == "__main__":
    pass2()