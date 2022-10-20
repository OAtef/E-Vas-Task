from Server import db


class MetaInfo(db.Document):
    meta_info_name = db.StringField()
    meta_info_value = db.StringField()

    def to_json(self):
        return {
            "meta_info_name": self.meta_info_name,
            "meta_info_value": self.meta_info_value
        }
