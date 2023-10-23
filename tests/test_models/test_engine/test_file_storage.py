#!/usr/bin/python3
""" Check Filestorage class """
import unittest
from datetime import datetime
from models.engine import file_storage
from os import path
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

FileStorage = file_storage.FileStorage
clas_dict = {}

class test_storage(unittest.TestCase):
    """ check the class """

class TestFileStorage(unittest.TestCase):
    """Testing the FileStorage class"""
    def test_all_returns_dict(self):
        """check  all returns attr"""
        storage = FileStorage()
        n_dict = storage.all()
        self.assertEqual(type(n_dict), dict)
        self.assertIs(n_dict, storage._FileStorage__objects)
    def setUp(self):
        """ check empty """
        try:
            remove('file.json')
        except Exception:
            pass
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """ check remove class """
        try:
            remove('file.json')
        except Exception:
            pass

    def test_no_objs(self):
        """ check empty class  """
        self.assertEqual(storage.all(), {})

    def test_new(self):
        """check  attr"""
    def test_all(self):
        """ check  all function """
        storage = FileStorage()
        storage._FileStorage__objects = {}
        n_dict = {}
        for key, value in clas_dict.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                n_dict[instance_key] = instance
                self.assertEqual(n_dict, storage._FileStorage__objects)
        storage._FileStorage__objects = {}
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_save_create(self):
        """ Save  """
        obj = BaseModel()
        obj_key = 'BaseModel' + '.' + obj.id
        obj1 = User()
        obj1_key = 'User' + '.' + obj1.id
        obj2 = City()
        obj2_key = 'City' + '.' + obj2.id
        obj3 = Amenity()
        obj3_key = 'Amenity' + '.' + obj3.id
        obj4 = Place()
        obj4_key = 'Place' + '.' + obj4.id
        obj5 = Review()
        obj5_key = 'Review' + '.' + obj5.id
        obj6 = State()
        obj6_key = 'State' + '.' + obj6.id

        self.assertEqual(obj, storage.all()[obj_key])
        self.assertEqual(obj1, storage.all()[obj1_key])
        self.assertEqual(obj2, storage.all()[obj2_key])
        self.assertEqual(obj3, storage.all()[obj3_key])
        self.assertEqual(obj4, storage.all()[obj4_key])
        self.assertEqual(obj5, storage.all()[obj5_key])
        self.assertEqual(obj6, storage.all()[obj6_key])

    def test_new_empty(self):
        """ check new method """
        with self.assertRaises(TypeError):
            storage.new()

    def test_new_classes(self):
        """ check  new method is valid """
        obj = BaseModel(id='123')
        obj_key = 'BaseModel' + '.' + obj.id
        obj1 = User(id='01')
        obj1_key = 'User' + '.' + obj1.id
        obj2 = City(id='02')
        obj2_key = 'City' + '.' + obj2.id
        obj3 = Amenity(id='03')
        obj3_key = 'Amenity' + '.' + obj3.id
        obj4 = Place(id='04')
        obj4_key = 'Place' + '.' + obj4.id
        obj5 = Review(id='05')
        obj5_key = 'Review' + '.' + obj5.id
        obj6 = State(id='06')
        obj6_key = 'State' + '.' + obj6.id

        self.assertEqual(storage.all(), {})
        obj.id = 123
        storage.new(obj)
        storage.new(obj1)
        storage.new(obj2)
        storage.new(obj3)
        storage.new(obj4)
        storage.new(obj5)
        storage.new(obj6)
        self.assertEqual(obj, storage.all()[obj_key])
        self.assertEqual(obj1, storage.all()[obj1_key])
        self.assertEqual(obj2, storage.all()[obj2_key])
        self.assertEqual(obj3, storage.all()[obj3_key])
        self.assertEqual(obj4, storage.all()[obj4_key])
        self.assertEqual(obj5, storage.all()[obj5_key])
        self.assertEqual(obj6, storage.all()[obj6_key])

    def test_reload(self):
        """ check reload classes """
        obj = BaseModel()
        obj_key = 'BaseModel' + '.' + obj.id
        obj1 = User()
        obj1_key = 'User' + '.' + obj1.id
        obj2 = City()
        obj2_key = 'City' + '.' + obj2.id
        obj3 = Amenity()
        obj3_key = 'Amenity' + '.' + obj3.id
        obj4 = Place()
        obj4_key = 'Place' + '.' + obj4.id
        obj5 = Review()
        obj5_key = 'Review' + '.' + obj5.id
        obj6 = State()
        obj6_key = 'State' + '.' + obj6.id
        storage.save()

        self.assertTrue(path.isfile('file.json'))
        FileStorage._FileStorage__objects = {}

        storage.reload()

        self.assertTrue(obj_key in storage.all().keys())
        self.assertEqual(obj.id, storage.all()[obj_key].id)
        self.assertTrue(obj1_key in storage.all().keys())
        self.assertEqual(obj1.id, storage.all()[obj1_key].id)
        self.assertTrue(obj2_key in storage.all().keys())
        self.assertEqual(obj2.id, storage.all()[obj2_key].id)
        self.assertTrue(obj3_key in storage.all().keys())
        self.assertEqual(obj3.id, storage.all()[obj3_key].id)
        self.assertTrue(obj4_key in storage.all().keys())
        self.assertEqual(obj4.id, storage.all()[obj4_key].id)
        self.assertTrue(obj5_key in storage.all().keys())
        self.assertEqual(obj5.id, storage.all()[obj5_key].id)
        self.assertTrue(obj6_key in storage.all().keys())
        self.assertEqual(obj6.id, storage.all()[obj6_key].id)
