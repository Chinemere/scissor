from ..utils import db
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable= False, unique=True)
    email= db.Column(db.String(), nullable= False, unique=True)
    passwordHash= db.Column(db.Text(), nullable= False)
    url= db.relationship('URL', backref='url_generator', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    @classmethod
    def get_user_id(cls, id):
        return cls.query.get_or_404(id)

