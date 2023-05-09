"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models

class User(Base):
    __tablename__ = "users"

    username = Column("username",TEXT, primary_key=True)
    password = Column("password", TEXT)
    first_name = Column("first_name", TEXT)
    last_name = Column("last_name", TEXT)
    age = Column("age", INTEGER)
    weight = Column("weight", INTEGER)
    height = Column("height", TEXT)

    def __init__(self,  username, password, first_name, last_name, age, weight, height):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.weight = weight
        self.height = height

    def __repr__(self):
        return str(self.first_name) , str(self.last_name) , str(self.age) , str(self.weight) + "lbs" , str(self.height)

class Workout(Base):
    __tablename__ = "workouts"

    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.username"))
    lift_id = Column("lift_id", ForeignKey("lifts.name"))
    num_reps = Column("num_reps", INTEGER)

    def __init__(self, user_id, lift_id, num_reps):
        self.user_id = user_id
        self.lift_id = lift_id
        self.num_reps = num_reps
    
    def __repr__(self):
        return str(self.lift_id) + ", " + str(self.num_reps)

class Lift(Base):
    __tablename__ = "lifts"

    name = Column("name", TEXT, primary_key=True)
    upper_lower = Column("upper_lower", INTEGER)
    muscle_group = Column("muscle_group", TEXT)
    discription = Column("discription", TEXT)

    def __init__(self, name, upper_lower, muscle_group, discription):
        self.name = name
        self.upper_lower = upper_lower
        self.muscle_group = muscle_group
        self.discription = discription





