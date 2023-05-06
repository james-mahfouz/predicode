from controllers.user_controller.user_controller import category_list, content_list, rf


def predict(size, price, category, content):
    data = [int(size), float(price)]

    for i in range(33):
        if category_list[i] == category:
            data.append(1)
        else:
            data.append(0)

    for i in range(5):
        if content_list[i] == content:
            data.append(1)
        else:
            data.append(0)

    rating = rf.predict([data])
    rating = str(rating[0])[:4]

    return rating
