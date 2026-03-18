def genre_popularity(genre_year_count, total_movies):

    popular_genres = []

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
