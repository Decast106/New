from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    href = db.Column(db.String, unique=True, nullable=False)
    company = db.Column(db.String, nullable=True)
    price = db.Column(db.String, nullable=True)
    data = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Vacancy {} {} {} {} {} {} {}>'.format(self.id, self.title, self.href, self.company, self.price, self.data, self.content)


