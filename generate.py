import os
import re
import ufoLib2
from ufo2ft import compileTTF

def clean_invalid_lookups(ufo):
    """
    Auto delete the invalid lookups in UFO features.fea file
    """
    if not ufo.features.text:
        return

    text = ufo.features.text
    lines = text.splitlines()

    # 1. find all defined lookup names
    defined = set(re.findall(r'lookup\s+(\w+)\s*\{', text))

    # 2. find all referenced lookup names
    referenced = set(re.findall(r'lookup\s+(\w+)\s*;', text))

    # 3. get invalid lookup
    invalid = referenced - defined
    if not invalid:
        print("No invalid lookup.")
        return

    print("Find invalid lookup:", invalid)

    # 4. delete invalid lookup line
    cleaned = []
    for line in lines:
        if any(name in line for name in invalid):
            continue
        cleaned.append(line)

    ufo.features.text = "\n".join(cleaned)
    print(f"Delete lookup: {', '.join(invalid)}")


def build_ttf_ufo2ft(ufo_path, output_dir):
    """
    Use ufo2ft from UFO generate TTF fonts (Auto convert qcurve, delete invalid lookup)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ufo = ufoLib2.Font.open(ufo_path)
    clean_invalid_lookups(ufo)

    ttf = compileTTF(ufo)
    ttf_path = os.path.join(output_dir, os.path.basename(ufo_path).replace(".ufo", ".ttf"))
    ttf.save(ttf_path)

    print(f"TTF generated in: {ttf_path}")


if __name__ == "__main__":
    output_folder = "./fonts/ttf"
    ufo_dir = r"./fonts/ufo"
    for ufo_name in os.listdir(ufo_dir):
        print("Building.... " + ufo_name)
        ufo_file = os.path.join(ufo_dir, ufo_name)
        build_ttf_ufo2ft(ufo_file, output_folder)