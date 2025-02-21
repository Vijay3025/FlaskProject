from extensions import db

class Product(db.Model):
    __tablename__ = "Product"
    ProductId = db.Column(db.Integer,primary_key=True)
    CatogoryId = db.Column(db.Integer)
    ProductName = db.Column(db.String(30),unique=True)
    ProductPrice = db.Column(db.String(30))

    def __str__(self):
        return f"ProductId : {self.ProductId},ProductName: {self.ProductName},Price :{self.ProductPrice}"
    
    def __repr__(self):
        return f"< {self.ProductId},{self.ProductName},{self.ProductPrice} >"
