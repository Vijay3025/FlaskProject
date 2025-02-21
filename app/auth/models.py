from extensions import db


class User(db.Model):
    __tablename__ = "User"
    UserId = db.Column(db.String(30),primary_key=True)
    UserName = db.Column(db.String(30))
    UserRole = db.Column(db.String(30))
    Password = db.Column(db.String(100))


    def __str__(self):
        return f"UserId: {self.UserId}, UserName: {self.UserName},UserRole :{self.UserRole}"
    
    def __repr__(self):
        return f"User<  {self.UserId},{self.UserName},{self.UserRole},{self.Password} >"