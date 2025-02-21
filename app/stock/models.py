from extensions import db

class Stock(db.Model):
    __tablename__="Stock"
    Id = db.Column(db.Integer,primary_key=True)
    ProductId = db.Column(db.Integer,db.ForeignKey("Product.ProductId"))
    InventoryId = db.Column(db.Integer,db.ForeignKey("Inventory.InventoryId"))
    Quantity = db.Column(db.Integer)

    def __str__(self):
        return f"StockId: {self.Id},ProductId : {self.ProductId},InvetoryId: {self.InventoryId},Quantity :{self.Quantity}"