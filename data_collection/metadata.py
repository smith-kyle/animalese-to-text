from os import listdir
from os.path import isfile
from pathlib import Path

def process_text_files(txt_files):
    result = []
    seen = set()
    for path in txt_files:
        with open(path) as f:
             f.read()

def get_text(t: str):
    return " ".join(t.splitlines()[1:])

def get_id(path):
    return path.split("/")[-1].split(".txt")[0]

def get_texts_and_ids(txt_files):
    results = []
    for txt_path in txt_files:
        with open(txt_path) as f:
            results.append((get_text(f.read()), get_id(str(txt_path))))
    return results


def normalize_text(text):
    replacements = [
        ("0", "zero"),
        ("1", "one"),
        ("1,000", "one thousand"),
        ("10", "ten"),
        ("10,000", "ten thousand"),
        ("100", "one hundred"),
        ("11", "eleven"),
        ("12", "twelve"),
        ("13", "thirteen"),
        ("140", "one hundred and fourty"),
        ("15", "fifteen"),
        ("160", "one hundred and sixty"),
        ("171", "one hundred and seventy one"),
        ("180", "one hundred and eighty"),
        ("23", "twenty three"),
        ("300", "three hundred"),
        ("33", "thirty three"),
        ("36", "thirty six"),
        ("4", "four"),
        ("40", "fourty"),
        ("42", "fourty two"),
        ("50", "fifty"),
        ("50,000", "fifty thousand"),
        ("7", "seven"),
        ("8", "eight"),
        ("800", "eight hundred"),
        ("9", "nine")
    ]
    replacements = sorted(replacements, key=lambda x: -1 * len(x[0]))
    s = text
    for match, replace in replacements:
        s = s.replace(match, replace)
    return s

def create_metadata(txt_files, path):
    texts_and_ids = get_texts_and_ids(txt_files)
    rows = []
    seen = set()
    for t, id_ in texts_and_ids:
        if t in seen:
            continue
        rows.append((id_, t, normalize_text(t)))
        seen.add(t)
    
    for row in rows:
        print(f"\"{row[0]}.wav\",")
    file = '\n'.join('|'.join(row) for row in rows)
    with open(path, 'w') as f:
        f.write(file)

if __name__ == "__main__":
    import sys
    DATA_DIR = Path(sys.argv[1])
    OUTPUT_PATH = sys.argv[2]

    txt_files = [DATA_DIR / f for f in listdir(DATA_DIR) if isfile(DATA_DIR / f) and ".txt" in f]
    create_metadata(txt_files, OUTPUT_PATH)



