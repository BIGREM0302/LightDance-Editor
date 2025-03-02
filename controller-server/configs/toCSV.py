import csv
import json
import os

def csv_to_ts_json(csv_file, ts_file):
    dancers = {}
    current_dancer = None

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ',' not in line:
                current_dancer = line
                dancers[current_dancer] = {"dancer": current_dancer}
            elif line.endswith(','):
                current_dancer = line.split(',')[0].strip()
                dancers[current_dancer] = {"dancer": current_dancer}
            else:
                part_info = [x.strip() for x in line.split(',')]
                if current_dancer and len(part_info) == 3:
                    part_name, part_id, part_length = part_info
                    dancers[current_dancer][part_name] = {
                        "id": part_id,
                        "length": int(part_length)
                    }

    with open(ts_file, 'w', encoding='utf-8',newline=os.linesep) as f:
        f.write("const dancers = ")
        f.write(str(dancers).replace("'", '"'))
        f.write(";\n\nexport default dancers;")

csv_to_ts_json('test.csv', 'test.ts')
print("Convert complete")
