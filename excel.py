# Writing to an excel
# sheet using Python
from xlwt import Workbook

def Excel(data):
    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')

    sheet1.write(0, 0, 'URL')
    sheet1.write(0, 1, 'Text')
    sheet1.write(0, 2, 'Date')
    sheet1.write(0, 3, 'Language')
    sheet1.write(0, 4, 'Likes')
    sheet1.write(0, 5, 'Retweets')
    sheet1.write(0, 6, 'Replies')
    sheet1.write(0, 7, 'Quotes')
    sheet1.write(0, 8, 'Views')
    sheet1.write(0, 9, 'Media')
    sheet1.write(0, 10, 'Is retweeted')

    for i, row in enumerate(data):
        sheet1.write(i+1, 0, row["url"])
        sheet1.write(i+1, 1, row["text"])
        sheet1.write(i+1, 2, row["date"])
        sheet1.write(i+1, 3, row["lang"])
        sheet1.write(i+1, 4, row["num_like"])
        sheet1.write(i+1, 5, row["num_retweet"])
        sheet1.write(i+1, 6, row["num_reply"])
        sheet1.write(i+1, 7, row["num_quote"])
        # sheet1.write(i+1, 8, row["num_views"])
        sheet1.write(i+1, 8, row["media"])
        sheet1.write(i+1, 9, row["retweet"])


    wb.save('Excel.xls')
