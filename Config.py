from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

Base = declarative_base()

# Conexão com MySQL
engine = create_engine(
    "mysql+mysqlconnector://root:1426@localhost:3306/locadora",
    echo=False
)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
