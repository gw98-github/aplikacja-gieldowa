from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false
from app import db

Base = declarative_base()


class Apisource(Base):
    __tablename__ = 'API_source'
    id = Column(Integer, primary_key=True)
    api_name = Column(String, unique=True, nullable=False)
    last_checked = Column(DateTime, nullable=False)


class Stock (Base):
    __tablename__ = 'Stock'
    id = Column(Integer, primary_key=True)
    stock_name = Column(String, unique=False, nullable=False)
    last_checked = Column(DateTime, nullable=False)
    api_id = Column(Integer, ForeignKey('apisource.id'))


class Company (Base):
    __tablename__ = 'Company'
    id = Column(Integer, primary_key=True)
    company_name = Column(String, unique=False, nullable=False)
    stock_id = Column(Integer, ForeignKey('stock.id'))


class Action (Base):
    __tablename__ = 'Action'
    id = Column(Integer, primary_key=True)
    value = Column(Float, unique=False, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'))
