import random
import requests
import unittest
from sqlalchemy import create_engine, text
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import sessionmaker


URI = 'postgresql://cs162_user:cs162_password@localhost/cs162'
metadata = MetaData()
engine = create_engine(URI)
Expression = Table('expression', metadata, autoload=True, autoload_with=engine)
Session = sessionmaker(engine)  


class TestServer(unittest.TestCase):

    def test_connection(self):
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.status_code, 200)
    def test_post(self):
        response = requests.post('http://localhost:5000/add', data={'expression':'1+1'})
        self.assertEqual(response.status_code, 200)

    def test_err(self):
        response = requests.post('http://localhost:5000/add', data={'expressions':'1+'})
        self.assertEqual(response.status_code, 400)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.x = random.random()
        self.y = random.random()
        self.expr = str(self.x)+" + "+str(self.y)
        self.response = requests.post('http://localhost:5000/add', data={'expression':self.expr})

    def test_db(self):
        session = Session()
        row = session.query(Expression).order_by(text('Expression.now desc')).first()
        self.assertAlmostEqual(float(row.value), self.x+self.y)

if __name__ == '__main__':
    unittest.main()
