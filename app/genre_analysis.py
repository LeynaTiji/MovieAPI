from collections import defaultdict

def genre_popularity(genre_year_count, total_movies):

    popular_genres = []

    # loop through all genres
    for genre, year in genre_year_count.items():
        each_year = []
        # sort years in order
        for y in sorted(year.keys()):
            count = year[y]

            #find percentage that genre makes up for total year
            percentage = ((count / total_movies[y]) * 100, 2) if year[y] else 0
            # how many movies made for genre per year
            each_year.append({"year": y, "count": count, "percentage": percentage})

        popular_genres.append({
            "genre": genre,
            "total_movies": sum(year.values()),
            "yearly_breakdown": each_year,
        })

        popular_genres.sort(key=lambda x: x["total_movies"], reverse=True)

    
    print(popular_genres[0])

def decade_summary(genre_year_count):
    #dictionary of dictionaries
    all_decades = defaultdict(lambda: defaultdict(int)) 

    for genre, year, in genre_year_count.items():

        for y, count in year.items():
            #work out what decade year is in
            decade = (y // 10 ) * 10

            # how many movies in the genre in specific decade
            all_decades[decade][genre] += count

    summary = []

    # #loop through all decades specified region
    # for decade in sorted(all_decades.keys()):


