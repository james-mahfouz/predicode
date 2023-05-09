from models.historyModel import History


def add_history(name, category, content_rating,
                price, size, rating, maintainability):
    history = History(name=name, category=category, content_rating=content_rating,
                          price=price, size=size, rating=rating,maintainability=maintainability)




    # name = StringField(max_length=100, required=True)
    # category = StringField(required=True)
    # content_rating = StringField(required=True)
    # price = FloatField(required=True)
    # size = FloatField(required=True)
    # rating = FloatField(required=True)
    # maintainability = StringField(required=True)
    # date_created = DateTimeField(required=True)
