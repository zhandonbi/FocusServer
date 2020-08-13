import xlrd

fileName = "./Daily_Check/sheet.xlsx"

def loadData():
    data = xlrd.open_workbook(fileName)
    table = data.sheets()[0]
    tables = []
    for rown in range(table.nrows):
        array = {'userID':'','name':''}
        array['userID'] = table.cell_value(rown,0)
        array['name'] = table.cell_value(rown,1)
        tables.append(array)
    return tables

if __name__ == "__main__":
    tables = loadData()
    for i in tables:
        print(i)


