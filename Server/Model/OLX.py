from Server import db


class Ads(db.Document):
    link = db.StringField()
    title = db.StringField()
    price = db.IntField()
    condition = db.StringField()
    description = db.StringField()
    advertiser_name = db.StringField()
    location = db.StringField()
    mobile = db.IntField()

    def to_json(self):
        return {
            "link": self.link,
            "title": self.title,
            "price": self.price,
            "condition": self.condition,
            "description": self.description,
            "advertiser_name": self.advertiser_name,
            "location": self.location,
            "mobile": self.mobile
        }
