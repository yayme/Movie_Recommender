from imdb import IMDb
import pandas as pd
top_movies=pd.read_csv("IMDB-Movie-Data.csv")
top_movies_data=[]

for index,movie in top_movies.iterrows():


    top_movies_data.append(
        {
            "title": movie['Title'],
            "genres": movie.get('Genre'),
            "director": movie['Director'],
            "cast": movie['Actors'].split(', ')[:3]
        }
    )
imdb_object=IMDb()
watched_movies=[]

print("Enter movies you've watched. Type 'Done' when you're done")

while True:
    movie_title=input("Title: ")
    print("please wait")

    if not movie_title or movie_title.lower() =='done':
        break

    search_results=imdb_object.search_movie(movie_title)
    if search_results:
        movie=search_results[0]
        imdb_object.update(movie)
        watched_movies.append({
            "title": movie['title'],
            "genres": movie.get('genres'),
            "director": movie['director'][0]['name'] if movie.get('director') else "Unknown",
            "cast": [actor['name'] for actor in movie['cast'][:3]]
        })

from sklearn.feature_extraction.text import TfidfVectorizer

features=[]
for movie in top_movies_data:
    feature_string=' '.join(movie['genres'] or [])+' '+movie['director']+' '+' '.join(movie['cast'])
    features.append(feature_string)

vectorizer=TfidfVectorizer()
feature_matrix=vectorizer.fit_transform(features)

# recommendation part

from sklearn.metrics.pairwise import cosine_similarity

similarity_matrix=cosine_similarity(feature_matrix)

def recommend_movie(watched_index,similarity_matrix,movie_titles):
    similar_score=list(enumerate(similarity_matrix[watched_index]))
    similar_score=sorted(similar_score,key=lambda x: x[1], reverse=True)
    recommend_titles=[movie_titles[i[0]] for i in similar_score[1:6]]
    return recommend_titles

for idx,movie in enumerate(watched_movies):
    print(f"Recommendations based on '{movie['title']}'")
    recommendations=recommend_movie(idx,similarity_matrix,[_['title'] for _ in top_movies_data])
    for rec in recommendations:
        print(f"-{rec}")
    print()

