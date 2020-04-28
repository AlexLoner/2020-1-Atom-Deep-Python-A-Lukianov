from entities import Base, Customer
from orm_base import MyBase


class Tables:

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, base: MyBase):
        self.base = base
        self.engine = base.connection.engine
        self.create_table('customers')

    # ------------------------------------------------------------------------------------------------------------------
    def create_table(self, name):
        '''Create a table called name in db if its not exists'''
        if not self.engine.dialect.has_table(self.engine, name):
            Base.metadata.tables[name].create(self.engine)

    # ------------------------------------------------------------------------------------------------------------------
    def create(self, entity: Customer):
        self.base.session.add(entity)
        self.base.session.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def all(self):
        '''Return all items for table'''
        return self.base.session.query(Customer).all()

    # ------------------------------------------------------------------------------------------------------------------
    def get(self, id):
        '''Returm item by primary_key'''
        return self.base.session.query(Customer).get(id)

    # ------------------------------------------------------------------------------------------------------------------
    def update(self, condition: tuple, key_to_update, new_value):
        '''Update all items from table that satisfies condition'''
        self.base.session.query(Customer).filter(*condition).update({key_to_update: new_value})
        self.base.session.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def delete(self, condition: tuple):
        ''' Delete all items from table that satisfies condition '''
        self.base.session.query(Customer).filter(*condition).delete()
        self.base.session.commit()
