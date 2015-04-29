from openpyxl import load_workbook
wb = load_workbook(filename='Lesson-1 Metadata.xlsx', read_only=True)
ws = wb['Sheet1'] # ws is now an IterableWorksheet

for row in ws.rows:
    for cell in row:
        print(cell.value)
