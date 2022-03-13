def totalrait(reviews):
    s, c, total_rating = 0, 0, 0
    lr = []
    for i in reviews:
        s += sum(i.return_rating())
        c += 1
    if c:
        total_rating = round(s/c)

    if total_rating == 5:
        lr = [1, 1, 1, 1, 1]
    elif total_rating == 4:
        lr = [1, 1, 1, 1, 0]
    elif total_rating == 3:
        lr = [1, 1, 1, 0, 0]
    elif total_rating == 2:
        lr = [1, 1, 0, 0, 0]
    elif total_rating == 1:
        lr = [1, 0, 0, 0, 0]

    return lr, c
