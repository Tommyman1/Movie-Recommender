import pandas as pd

#!!!!!!!!note this is only to remodel the data and not our main program shouldn't be used multiple times if df_3 is already created. Data from IMDb. As well as different process are commented out by !!!!! so conversion should be uncommented for first time use then comment them again and uncomment the next section!!!!!!!!

#Transforming tsv data into csv
# tsv_file='title.basics.tsv'
# tsv_file2="title.ratings.tsv"

# # reading given tsv file
# csv_table=pd.read_table(tsv_file,sep='\t')

# # converting tsv file into csv
# csv_table.to_csv('title.ratings.csv',index=False)
# csv_table.to_csv('ttitle.basics.csv',index=False)
# # output
# print("Successfully made csv file")
#!!!!!!!!!!!!!!!!!  


#!!!!!!!!!!!!!!!!!!!!!!!!!
#reconstruction of the database to obtain information we desire

df_1 = pd.read_csv("title.basics.csv", dtype = {"primaryTitle": str,"runtimeMinutes": str,"genres": str,"endYear": str,"tconst": str,"startYear": str,"tconst": str,"titleType": str,"originalTitle":str,"isAdult":str})

#filtering out everything that is not a movie
df_1 = df_1[df_1["titleType"] == "movie"]

#setting values
df_2 = pd.read_csv("title.ratings.csv",dtype ={"numVotes": str,"tconst": str, "averageRating": str})
#merging all data sets
merged = df_1.merge(df_2, on = "tconst")
#choosing specfic datasets
df_3 = merged[["primaryTitle","startYear","runtimeMinutes","genres","averageRating"]]

#we are filtering out numbers less then 30 and strings
for index in df_3.index:
    try:
        if pd.to_numeric(df_3.loc[index,"runtimeMinutes"]) < 30:
            df_3.loc[index,"runtimeMinutes"] = 30
    except:
        df_3.loc[index,"runtimeMinutes"] = 30
    
#creates the dataset
df_3.to_csv("movie.csv",index = False)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!