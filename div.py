import csv
from collections import defaultdict

# словник для частин мови
data = defaultdict(list)

# читаємо існуючий файл з IDs
with open("results_with_ids.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pos = row['POS']
        word = row['Lemma']
        count = int(row['Frequency'])
        ids = row['IDs']
        data[pos].append((word, count, ids))

# функція для запису окремого файлу
def save_sorted(pos, filename):
    items = sorted(data.get(pos, []), key=lambda x: x[0].lower())  # сортування алфавітом
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([pos, "Word", "Count", "IDs"])
        for word, count, ids in items:
            writer.writerow([pos, word, count, ids])

save_sorted("NOUN", "nouns.csv")
save_sorted("VERB", "verbs.csv")
save_sorted("ADJ", "adjs.csv")
