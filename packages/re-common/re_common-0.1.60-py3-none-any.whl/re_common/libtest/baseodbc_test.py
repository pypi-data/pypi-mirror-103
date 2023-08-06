from re_common.baselibrary.utils.baseodbc import BaseODBC

baseodbc = BaseODBC(r"C:\Users\xuzhu\Documents\WXWork\1688853051339318\Cache\File\2021-04\cnki期刊信息_20210406(3).mdb")
# baseodbc = BaseODBC(r"D:\download\cnki_qk\download\get_journal\mdb\cnki期刊信息_20200315.mdb")
baseodbc.get_cur()
sql = "select bid,GCH from `qklist`"
for row in baseodbc.select_all(sql):
    bid = row[0]
    gch = row[1]
    if not gch:
        gch = ""
    sql = f"update journallist set gch='{gch}' where journal_rawid='{bid}' and taskname='cnkijournal';"
    print(sql)