# from docx import Document
# import csv

# doc = Document("data.docx")

# with open("data.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)

#     # Заголовки
#     writer.writerow(["ID", "Text"])

#     for table in doc.tables:
#         for row in table.rows:
#             # беремо тільки перші дві колонки
#             if len(row.cells) >= 2:
#                 id_val = row.cells[0].text.strip()
#                 text_val = row.cells[1].text.strip()
#                 writer.writerow([id_val, text_val])

import csv

with open("data.csv", "r", encoding="utf-8") as f_in, \
     open("numbered.csv", "w", newline="", encoding="utf-8") as f_out:

    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    for i, row in enumerate(reader, start=1):
        # row[0] може бути порожнім, тому просто ставимо i як ID
        text = row[1] if len(row) > 1 else ""
        writer.writerow([i, text])
