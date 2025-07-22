import pandas as pd
from datetime import datetime

def scale(number_scale):
    min = number_scale.min()
    max = number_scale.max()
    return ((number_scale-min)/(max-min))

if __name__ == "__main__":

    wl=pd.read_csv("watchlist.csv",dtype = {"primaryTitle":str,"startYear":int,"runtimeMinutes":int,"genres":str,"averageRating":float})
    
    while True:
        title = input("\nPlease input a movie title you last watched(q to quit): ")
        
        if title == "q":
            break
        
        year = int(input("In what year did the movie come out: "))
        
        while 1800 > year or year > datetime.now().year:
            year = int(input("\nIn what year did the movie come out: "))
            
        runtime = int(input("\nHow long was the movie in minutes: "))
        
        while runtime > 14400:
            runtime = int(input("\nHow long was the movie in minutes: "))
        
        rate = int(input("\nHow would you rate the movie in a scale from 0-10"))
        
        while 0 > rate or rate > 10:
            rate = int(input("\nHow would you rate the movie in a scale from 0-10"))
            
        topic = input("What is the genre of this movie: ")
        
        wl.loc[len(wl)] = [title,year,runtime,topic,rate]
        
        wl.to_csv('watchlist.csv',index = False) 
    
    #reads and assign data types for the following columns 
    df = pd.read_csv("movie.csv",dtype = {"primaryTitle":str,"startYear":int,"runtimeMinutes":int,"genres":str,"averageRating":float})
    
    #list of genres provided in the dataset
    rate_genres = {'Action': "",'Adult': "",
    'Adventure': "",'Animation': "",
    'Biography': "",'Comedy': "",
    'Crime': "",'Documentary': "",
    'Drama': "",'Family': "",
    'Fantasy': "",'Film-Noir': "",
    'Game-Show': "",'History': "",
    'Horror': "",'Music': "",
    'Musical': "",'Mystery': "",
    'News': "",'Reality-TV': "",
    'Romance': "",'Sci-Fi': "",
    'Sport': "",'Talk-Show': "",
    'Thriller': "",'War': "",'Western':"" ,}
    
    #iteriates through the dictionary
    for genre,value in rate_genres.items():
        rating = int(input(f"\nRate the genre {genre} in a scale from 1-10: "))
        #error handling
        while rating >10 or rating < 0:
            rating = int(input(f"\nRate the genre {genre} in a scale from 1-10: "))
        #saves the new values
        rate_genres[genre] = rating
    #when there are nulls it will be assigned to zero
    rate_genres['\\N'] = 0
    df["genres"] = df["genres"].fillna("0")
    #splits genres that have , to a list
    df["genres"]= df["genres"].apply(lambda genre: genre.split(","))
    
    #iteriates through every row
    for i in range(len(df)):
        #pulls out list at every row
        genres = df.at[i,"genres"]
        #iteriates through every index of the list
        for j in range(len(genres)):
            genre = genres[j]
            # if the genre is in the list of rating then we would save the rating values instead of the genre we have for it
            if genre in rate_genres:
                genres[j] = rate_genres[genre]
            #if it fails then it will get replaced with zero
            else:
                genres[j] = 0
        #saved
        df.at[i,"genres"] = genres
    
    #iteriate through a the dataframe            
    for i in range(len(df)):
        #at row i in the columns called genres
        genres = df.at[i,"genres"]
        #all the numbers will be sumed
        genres_sum = sum(genres)
        #saved 
        df.at[i,"genres"] = genres_sum
        
    wl["genres"] = wl["genres"].fillna("0")
    #splits genres that have , to a list
    wl["genres"]= wl["genres"].apply(lambda genre: genre.split(","))
    
    #iteriates through every row
    for i in range(len(wl)):
        #pulls out list at every row
        genres = wl.at[i,"genres"]
        #iteriates through every index of the list
        for j in range(len(genres)):
            genre = genres[j]
            # if the genre is in the list of rating then we would save the rating values instead of the genre we have for it
            if genre in rate_genres:
                genres[j] = rate_genres[genre]
            #if it fails then it will get replaced with zero
            else:
                genres[j] = 0
        #saved
        wl.at[i,"genres"] = genres
        
    #iteriate through a the dataframe            
    for i in range(len(wl)):
        #at row i in the columns called genres
        genres = wl.at[i,"genres"]
        #all the numbers will be sumed
        genres_sum = sum(genres)
        #saved 
        wl.at[i,"genres"] = genres_sum 
        
    #changes genres rating from int to float    
    wl["genres"] = wl["genres"].astype(float)
    #scales the genres
    wl["genres"] = scale(wl["genres"])
    #scales the runtime
    wl["runtimeMinutes"] = scale(wl["runtimeMinutes"])
    #scales the average rating
    wl["averageRating"] = scale(wl["averageRating"])
    #scales the start year
    wl["startYear"] = scale(wl["startYear"])    
        
        
    #changes genres rating from int to float    
    df["genres"] = df["genres"].astype(float)
    #scales the genres
    df["genres"] = scale(df["genres"])
    #scales the runtime
    df["runtimeMinutes"] = scale(df["runtimeMinutes"])
    #scales the average rating
    df["averageRating"] = scale(df["averageRating"])
    #scales the start year
    df["startYear"] = scale(df["startYear"])

    
    
    
