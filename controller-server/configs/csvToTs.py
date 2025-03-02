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
                dancers[current_dancer] = {"fps":30,"OFPARTS":{}, "LEDPARTS":{}, "LEDPARTS_MERGE":{}}
            elif line.endswith(','):
                current_dancer = line.split(',')[0].strip()
                dancers[current_dancer] = {"fps":30,"OFPARTS":{}, "LEDPARTS":{}, "LEDPARTS_MERGE":{}}
            else:
                part_info = [x.strip() for x in line.split(',')]
                if current_dancer and len(part_info) == 3:
                    part_name, part_id, part_length = part_info
                    dancers[current_dancer]["LEDPARTS"][part_name] = {
                        "id": int(part_id),
                        "len": int(part_length)
                    }

    with open(ts_file, 'w', encoding='utf-8',newline=os.linesep) as f:
        f.write("import { ModelPinMapTable} from \"@/schema/PinMapTable\";\n")
        f.write("const PropPinMapTable: ModelPinMapTable = ")
        json.dump(dancers, f, ensure_ascii=False, indent=2)
        f.write(";\n\nexport default PropPinMapTable;")

csv_to_ts_json('props_channel_software.csv', 'propPinMapTable.ts')
print("Convert complete")