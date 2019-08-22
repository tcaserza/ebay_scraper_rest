from ebay import app, db


class items(db.Model):
    """
    Table structure
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    item_id = db.Column(db.String(50))
    title = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    price = db.Column(db.String(10))


    def __repr__(self):
        return '<stats %r>' % self.id

    def to_json(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "title": self.title,
            "end_date": self.end_date,
            "price": self.price
            }

    def from_json(self, source):
        for key in ["id", "item_id", "title", "end_date", "price"]:
            if key in source:
                setattr(self, key, source[key])
            else:
                setattr(self, key, None)



