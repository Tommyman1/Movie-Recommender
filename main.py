import pandas as pd
from datetime import datetime
from sklearn.neighbors import NearestNeighbors
import random
import time
import json
import os

def scale(number_scale, optional_param=None):
    min_val = optional_param.min() if optional_param is not None else number_scale.min()
    
    max_val = optional_param.max() if optional_param is not None else number_scale.max()
    if max_val == min_val:
        return number_scale * 0
    
    scaled = ((number_scale - min_val) / (max_val - min_val))
    return scaled

def preprocess(Dataframe, optional_param=None):
    #scales the runtime,average rating,start year,genres 
    cols =["startYear","averageRating","runtimeMinutes","genres"]
    for col in cols:
        Dataframe[col] = scale(
            Dataframe[col].astype(float),
            optional_param[col].astype(float) if optional_param is not None else None
        )
    
    return Dataframe
        
    
def adding(Dataframe):    
    Dataframe["genres"] =Dataframe["genres"].apply(sum)

def str_replacer(DataFrame,genre_list):
    #iteriates through every row
    for i in range(len(DataFrame)):
        #goes to a row in the collum genres i which can have a list in it
        genres = DataFrame.at[i,"genres"]
        #goes through the list in the specific row 
        for j in range(len(genres)):
            genre = genres[j]
            # if the genre is in the list of rating then we would save the rating values instead of the genre we have for it
            if genre in genre_list:
                #The specific genre row
                genres[j] = genre_list[genre]
            #if it fails then it will get replaced with zero
            else:
                genres[j] = 0
        #saved
        DataFrame.at[i,"genres"] = genres
        
def preparing(Dataframe, drop_columns = False):
    temp_Dataframe = Dataframe.copy()
    if drop_columns == True:
        temp_Dataframe = temp_Dataframe.drop(columns = ["primaryTitle"]).reset_index(drop = True)
        temp_Dataframe = temp_Dataframe.dropna()
        temp_Dataframe = temp_Dataframe.fillna(0)
    return temp_Dataframe
    

if __name__ == "__main__": 
    #reads and assign data types for the following columns 
    df = pd.read_csv("movie.csv", na_values="\\N", dtype = {"primaryTitle":str,"startYear":float,"runtimeMinutes":float,"genres":str,"averageRating":float})
    
    
    #list of genres provided in the dataset
    rate_genres = {
    'Action': 0,'Adult': 0,
    'Adventure': 0,'Animation': 0,
    'Biography': 0,'Comedy': 0,
    'Crime': 0,'Documentary': 0,
    'Drama': 0,'Family': 0,
    'Fantasy': 0,'Film-Noir': 0,
    'Game-Show': 0,'History': 0,
    'Horror': 0,'Music': 0,
    'Musical': 0,'Mystery': 0,
    'News': 0,'Reality-TV': 0,
    'Romance': 0 ,'Sci-Fi': 0,
    'Sport': 0,'Talk-Show': 0,
    'Thriller': 0,'War': 0,'Western':0,}
    
    #Reads a clean dataframe and inputs the variables as datatype
    wl=pd.read_csv("watchlist.csv",dtype = {"primaryTitle":str,"startYear":float,"runtimeMinutes":float,"genres":str,"averageRating":float})
    
    #Loop that will add to this empty Dataframe
    while True:
        title = input("\nPlease input a movie title you last watched(q to quit): ").strip()
        #quit
        if title.lower() == "q":
            break
        
        
        while True:
            try:
                #obtaining years
                year = float(input("\nIn what year did the movie come out: "))
                if 1800 < year and year <= datetime.now().year:
                    break
            except ValueError:
                print("\nAnswer invalid,try again")
                
        while True:     
            try:  
                #obtaining runtime    
                runtime = float(input("\nHow long was the movie in minutes: "))
                if runtime < 14400:
                    break
            except ValueError:
                print("\nAnswer invalid,try again")
        
        while True:
            try:   
            #obtaining rating    
                rate = float(input("\nHow would you rate the movie in a scale from 0-10: "))
                if 0 < rate and rate <= 10:
                    break
            except ValueError:
                print("\nAnswer invalid,try again")
            
        #obtaining genres and making sure its in our list of genres we have
        print("\nWhat genre is this movie(Please choose one or more from the following seperating it with ,):\n")
        time.sleep(2)
        print('\n'.join(rate_genres.keys()))
        
        while True:
            topic = [t.strip() for t in input("\nEnter genre(s), separated by commas: ").split(",")]
            if all(t in rate_genres for t in topic):
                break
            print("\nOne or more genres not recognized. Please choose from the following:")
            print('\n'.join(rate_genres.keys()))
            
        #making a row with all the data
        wl.loc[len(wl)] = [title,year,runtime,topic,rate]
        
        #A loop that displays watchlist if we desire
        while True:
            command =(input("\nType w if you wish to view your watchlist(q to quit): ").strip()).lower()
            if command == "w":
                print(wl["primaryTitle"])
                break
            elif command == "q":
                break
            else:
                print("\nInvalid key")
    
    if os.path.exists("personal.json"):
        
        with open("./personal.json","r") as user_answers:  
            rate_genres = json.load(user_answers)
        
    else:
        #iteriates through the dictionary of genres and assigns user inputs to them
        for genre,value in rate_genres.items():
            while True:
                try:
                    rating = float(input(f"\nRate the genre {genre} in a scale from 1-10: "))
                    if float(rating) < 11 and float(rating) > 0:
                        #saves the new values
                        rate_genres[genre] = rating
                        break
                    
                    
                    else:
                        print("\nPlease enter a number between 0 and 10")
                except ValueError:
                    print("\nAnswer invalid,try again")
                    
        with open("./personal.json","w") as output:
            json.dump(rate_genres,output, indent=4)
    
    #when there are nulls in the dataset, it will be assigned to zero as well as anything empty will also be assigned a zero 
    rate_genres['\\N'] = 0
    df["genres"] = df["genres"].fillna("0")
    
    #In the collum genre we split  multiple titles into a list by splitting anytime there is a , in the collum
    df["genres"]= df["genres"].apply(lambda genre: genre.split(",") if isinstance(genre,str) else genre)
    
    str_replacer(df,rate_genres)
    adding(df)
    df_original = df.copy()
    
    for col in ["startYear", "averageRating", "runtimeMinutes", "genres"]:
        df[col] = scale(df[col])

        
    wl["genres"] = wl["genres"].fillna("0")
    #splits genres that have , to a list
    wl["genres"]= wl["genres"].apply(lambda genre: genre.split(",") if isinstance(genre,str) else genre)
    
    #preparomg the data and removing any nulls and adding 0 to any missing values
    str_replacer(wl,rate_genres)
    adding(wl) 

    for col in ["startYear", "averageRating", "runtimeMinutes", "genres"]:
        wl[col] = scale(wl[col], optional_param= df_original[col])
    
    temp_df = preparing(df,drop_columns=True)
    temp_wl = preparing(wl,drop_columns=True)
    
    recommend = "The movies that we recommend to you based on your last movie are:\n"
        
    if 0 < len(wl) < 10:
        try:
            while True:
                knn = NearestNeighbors(n_neighbors=10)
                knn.fit(temp_df)
                distance, indices = knn.kneighbors(temp_wl.iloc[[-1]])
                for inx in indices[0]:
                    recommend += "\n " + df.loc[inx]["primaryTitle"]
                break
            
        except Exception as e:
            default_row = pd.DataFrame([{
            "startYear": 2022,
            "runtimeMinutes": 100,
            "genres": 7,
            "averageRating": 8,
                }])
            
            temp_wl = pd.concat([temp_wl, default_row], ignore_index=True)
            temp_wl = scale(temp_wl,optional_param=temp_df) 
            temp_wl = temp_wl.fillna(0)
            
            knn = NearestNeighbors(n_neighbors=10)
            knn.fit(temp_df)
            distance, indices = knn.kneighbors(temp_wl.iloc[[-1]])
            
            for inx in indices[0]:
                recommend += "\n " + df.loc[inx]["primaryTitle"]
               
    else:
        knn = NearestNeighbors(n_neighbors=10)
        knn.fit(temp_df)
        
        temp_wl = temp_wl.reset_index(drop = True)
        r = random.randrange(0,len(temp_wl))
        
        distance, indices = knn.kneighbors(temp_wl.loc[[r]])
        
        for inx in indices[0]:
            recommend += "\n " + df.loc[inx]["primaryTitle"]
            
    print(recommend)
    
    while True:
        save = input("\nDo you want to save your watch list data? (y/n): ").lower()
        if save == 'y':
            wl.to_csv("watchlist.csv", index=False)
            break
        elif save == 'n':
            break
        else:
            print("\nInvalid key")