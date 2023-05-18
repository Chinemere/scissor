from ..utils import db

class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer(), primary_key=True)
    url_source= db.Column(db.String(1200), nullable=False)
    scissored_url = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer(), nullable=False, default= 0)
    user = db.Column(db.Integer(), db.ForeignKey('users.id') )

    
    def __repr__(self):
        return f'<Url {self.scissored_url}  {self.clicks}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    @classmethod
    def get_url_id(cls, id):
        return cls.query.get_or_404(id)


    
    




    