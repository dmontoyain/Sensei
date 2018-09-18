from dbUpdater.dbData.run import updateUsers

try:
    updateUsers('test')
except:
    print("error")
