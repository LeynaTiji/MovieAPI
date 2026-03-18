def genre_popularity(genre_year_count):

    popular_genres = []

    for genre, year in genre_year_count.items():
        each_year = []
        # sort years in order
        for y in sorted(year.keys()):
            count = year[y]
            #find percentage that genre makes up for total year
            percentage = ((count / year[y]) * 100, 2) if year[y] else 0
            each_year.append({"year": y, "count": count, "percentage": percentage})
