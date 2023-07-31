

# Our environment is going to be generated in lib/__init__.py using a series of
# imports and instantiations. Here we will generate a
# sqlite3.Connection object, CONN, and a sqlite3.Cursor object, 
# CURSOR to be used throughout the lab.

import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

# The __init__ method takes name and breed as arguments and 
# saves them as instance attributes. __init__ should also create an 
# id instance attribute.
class Dog:
    def __init__ (self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None
    

    # Create a create_table() class method that will create the dogs table if it does not already exist. 
    # The table should have columns for an id, a name, and a breed.
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)
        CONN.commit()


    # This class method should drop the dogs table if it does exist- 
    # pretty much the opposite of create_table().
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)
        CONN.commit()


    # Create an instance method save() that saves a Dog object to your database.
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]



    # This is a class method that should:
    #     Create a new row in the database.
    #     Return a new instance of the Dog class.
    # Think about how you can re-use the save() method to help with this one.
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog


    # Class Dog in dog.py contains method "new_from_db()" that takes a database row and creates a Dog instance.
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog


    # This class method should return a list of Dog instances for every record in the dogs table
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    

    # Class Dog in dog.py contains method "find_by_name()" that returns a Dog instance corresponding to its database record retrieved by name.
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (name,)).fetchone()

        return cls.new_from_db(dog)
    


    # This class method takes in an ID, and should return a single Dog instance for the corresponding record in the dogs table with that same ID.
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (id,)).fetchone()

        return cls.new_from_db(dog)



    