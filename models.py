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

    id = Column("id", INTEGER, primary_key=True)
    username = Column("username", TEXT)
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

class Workout(Base):
    __tablename__ = "workouts"

    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    lift_id = Column("lift_id", ForeignKey("lifts.id"))
    num_reps = Column("num_reps", INTEGER)

    def __init__(self, user_id, lift_id, num_reps):
        self.user_id = user_id
        self.lift_id = lift_id
        self.num_reps = num_reps

class Lift(Base):
    __tablename__ = "lifts"

    id = Column("id", INTEGER, primary_key=True)
    muscle_group = Column("muscle_group", TEXT)
    discription = Column("discription", TEXT)

    def __init__(self, muscle_group, discription):
        self.muscle_group = muscle_group
        self.discription = discription





