
from fastai.tabular.all import *
from fastai.collab import *
import mysql.connector
import pandas as pd
from mysqlconnect import mysqlkey

mydb = mysql.connector.connect(
  host=mysqlkey("host"),
  user=mysqlkey("user"),
  password=mysqlkey("password"),
  database=mysqlkey("database")
)
mycursor = mydb.cursor()


ml_sql_dataframe = pd.read_sql("SELECT * FROM anime_lists", mydb)

learn = load_learner("anime_ml_model.pkl",cpu=False)

def get_preds_for_user(user):
    user_submission_list = pd.read_sql(("select animeid FROM anime_lists WHERE user in (%(name)s)"), mydb, params={"name":user})
    rows = []
    animeid = list(ml_sql_dataframe.drop_duplicates(subset='animeid', keep='first').animeid)

    for i in range(len(animeid)):
        rows.append( dict({'user' : user,'animeid' : animeid[i]}))
    test_data = pd.DataFrame(rows)

    test_data = pd.DataFrame(rows)

    dl = learn.dls.test_dl(test_data, bs=64)

    preds,  y = learn.get_preds(dl=dl)

    prediction_results = []
    predictions = 0
    for idx, (rating, animeid) in enumerate(sorted(zip(preds, animeid), reverse=True)):
        if animeid not in user_submission_list.values and predictions <= 9:
            prediction_results.append([animeid, round(float(rating), 5)])
            predictions = predictions + 1
    return(prediction_results)
    

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
