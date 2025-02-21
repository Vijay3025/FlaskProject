from extensions import db

class Inventory(db.Model):
    __tablename__ = "Inventory"
    InventoryId = db.Column(db.Integer,primary_key=True)
    Country = db.Column(db.String)
    Location = db.Column(db.String)




