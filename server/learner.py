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

dls = CollabDataLoaders.from_df(ml_sql_dataframe,user_name= "user",item_name="animeid",rating_name="rating", bs=64)

learn = collab_learner(dls, n_factors=50, y_range=(0, 10))

learn.lr_find()

learn.fit_one_cycle(10, learn.lr_find().valley)

learn.export("anime_ml_model.pkl")
