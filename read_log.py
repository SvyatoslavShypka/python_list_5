import sys
from parsing import parsing_line


def read_log():
    result = []
    for line in sys.stdin:
        line = line.strip()
        # print("line: ", line)
        if line:  # Jeżeli linia nie jest pusta
            log_entry = parsing_line(line)
            if log_entry:
                result.append(log_entry)
    return result
