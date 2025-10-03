import pandas as pd
import spacy
from collections import defaultdict

# Завантажуємо модель spaCy
nlp = spacy.load("en_core_web_sm")

# Читаємо CSV файл
df = pd.read_csv('numbered.csv', header=None, names=['id', 'text'])
df['text'] = df['text'].fillna('').astype(str)

# Ввід діапазону речень (від 1 до N)
user_input = input("Введіть діапазон речень (наприклад, 1 2995): ")
start, end = map(int, user_input.split())

subset_df = df[(df['id'] >= start) & (df['id'] <= end)]

# Словники для лем, частоти та номерів рядків
nouns = defaultdict(lambda: {'count':0, 'ids':set()})
verbs = defaultdict(lambda: {'count':0, 'ids':set()})
adjs  = defaultdict(lambda: {'count':0, 'ids':set()})

# Обробка тексту по рядках
for _, row in subset_df.iterrows():
    sentence_id = row['id']
    doc = nlp(row['text'])
    for token in doc:
        lemma = token.lemma_.lower().strip()
        if not lemma or lemma in spacy.lang.en.stop_words.STOP_WORDS or not token.is_alpha:
            continue
        pos = token.pos_
        if pos == 'NOUN':
            nouns[lemma]['count'] += 1
            nouns[lemma]['ids'].add(sentence_id)
        elif pos == 'VERB':
            verbs[lemma]['count'] += 1
            verbs[lemma]['ids'].add(sentence_id)
        elif pos == 'ADJ':
            adjs[lemma]['count'] += 1
            adjs[lemma]['ids'].add(sentence_id)

# Формуємо список рядків для CSV
rows = []
for lemma, data in nouns.items():
    rows.append({'POS':'NOUN', 'Lemma':lemma, 'Frequency':data['count'], 'IDs':','.join(map(str, sorted(data['ids'])))})
for lemma, data in verbs.items():
    rows.append({'POS':'VERB', 'Lemma':lemma, 'Frequency':data['count'], 'IDs':','.join(map(str, sorted(data['ids'])))})
for lemma, data in adjs.items():
    rows.append({'POS':'ADJ', 'Lemma':lemma, 'Frequency':data['count'], 'IDs':','.join(map(str, sorted(data['ids'])))})

# Створюємо DataFrame та сортуємо за частотою
result_df = pd.DataFrame(rows)
result_df = result_df.sort_values(by='Frequency', ascending=False)

# Зберігаємо у CSV
result_df.to_csv('results_with_ids.csv', index=False)

print("Результати збережено у файл results_with_ids.csv")
print(result_df.head(10))
