import pandas as pd

def scale(number_scale):
    min = number_scale.min()
    max = number_scale.max()
    return ((number_scale-min)/(max-min))

if __name__ == "__main__":
    
    df = pd.read_csv("movie.csv",dtype = {"primaryTitle":str,"startYear":str,"runtimeMinutes":str,"genres":str,"averageRating":float})
    
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
    
    for genre,value in rate_genres.items():
        rating = int(input(f"\nRate the genre {genre} in a scale from 1-10: "))
        while rating >10 or rating < 0:
            rating = int(input(f"\nRate the genre {genre} in a scale from 1-10: "))
            
        rate_genres[genre] = rating
        
    rate_genres['\\N'] = 0
    df["genres"] = df["genres"].fillna("0")
    
    df["genres"]= df["genres"].apply(lambda genre: genre.split(","))
    
    #iteriates through every row
    for i in range(len(df)):
        #pulls out list at every row
        genres = df.at[i,"genres"]
        #iteriates through every index of the list
        for j in range(len(genres)):
            genre = genres[j]
            if genre in rate_genres:
                genres[j] = rate_genres[genre]
            else:
                genres[j] = 0
        df.at[i,"genres"] = genres
                
    for i in range(len(df)):
        genres = df.at[i,"genres"]
        genres_sum = sum(genres)
        df.at[i,"genres"] = genres_sum
        
    df["genres"] = df["genres"].astype(float)
    
    df["genres"] = scale(df["genres"])