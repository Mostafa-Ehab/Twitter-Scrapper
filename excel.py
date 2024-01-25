# Writing to an excel
# sheet using Python
from xlwt import Workbook

def Excel(
    data: list,
    output: list
):
    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')

    for i, row in enumerate(output):
        sheet1.write(0, i, row)

    for i, row in enumerate(data):
        for j, cell in enumerate(output):
            sheet1.write(i+1, j, row[cell])
        print(row)

    wb.save('Excel.xls')
