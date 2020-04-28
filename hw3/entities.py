import datetime
from faker import Faker
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
fake = Faker('en_US')


class Customer(Base):

    __tablename__ = 'customers'
    __table_args__ = {'mysql_charset': 'utf8', }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    fullname = Column(String(40), nullable=False)
    email = Column(String(70), nullable=False)
    birthday = Column(Date, nullable=False)

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name: str = None, fullname: str = None, email: str = None, birthday: str = None):
        self.name = name if name else fake.first_name()
        self.fullname = fullname if fullname else fake.last_name()
        self.email = email if email else fake.email()
        try:
            datetime.datetime.strptime(birthday, "%Y-%m-%d")
            date = birthday
        except:
            date = fake.date()
        self.birthday = date

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f'<Customer :: {self.id}_{self.name}_{self.fullname}_{self.email}_{self.birthday})>'

