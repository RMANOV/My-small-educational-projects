
from csv import excel, excel_tab


excel = excel.reader('data.csv')
excel = list(excel)
excel = excel[1:]
excel_tab = excel_tab.reader('data.csv')
excel_tab = list(excel_tab)
excel_tab = excel_tab[1:]
excel_tab = excel_tab[0]
