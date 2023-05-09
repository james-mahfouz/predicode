from models.historyModel import History


def add_history(user, name, category, content_rating,
                price, size, rating, maintainability):
    history = History(name=name, category=category, content_rating=content_rating,
                      price=price, size=size, rating=rating, maintainability=maintainability)
    user.history.append(history)

