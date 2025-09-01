from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import os # for setting environment variable

# set environment variable for security
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
server_address = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")

# Initialize SQLAlchemy base
Base = declarative_base()
# Database connection (replace with your PostgreSQL credentials)
engine = create_engine(f'postgresql://{user}:{password}@{server_address}/{dbname}')

# Dimension: Date
# This table stores date-related information for analysis, such as day, month, quarter, and year.
class DimDate(Base):
    __tablename__ = 'dimdate'
    date_id = Column(Integer, primary_key=True, autoincrement=True)
    full_date = Column(Date, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

# Dimension: Ship Mode
class DimShipMode(Base):
    __tablename__ = 'dimshipmode'
    ship_mode_id = Column(Integer, primary_key=True, autoincrement=True)
    ship_mode = Column(String(50), nullable=False)

# Dimension: Customer
class DimCustomer(Base):
    __tablename__ = 'dimcustomer'
    customer_id = Column(String(20), primary_key=True)
    customer_name = Column(String(80), nullable=False)
    segment = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    postal_code = Column(String(20))  # Optional, can be null
    region = Column(String(20))

# Dimension: Product
class DimProduct(Base):
    __tablename__ = 'dimproduct'
    product_id = Column(String(30), primary_key=True)
    category = Column(String(50), nullable=False)
    sub_category = Column(String(50))  # Optional, can be null
    product_name = Column(String(255), nullable=False)

# Dimension: Order Priority
class DimOrderPriority(Base):
    __tablename__ = 'dimorderpriority'
    order_priority_id = Column(Integer, primary_key=True, autoincrement=True)
    order_priority = Column(String(30), nullable=False)

# Fact Table: The `factorder` table stores transactional data for retail sales,
# linking to dimension tables such as `dimdate`, `dimshipmode`, `dimcustomer`,
# `dimproduct`, and `dimorderpriority` to provide detailed context for each order.
class FactOrder(Base):
    __tablename__ = 'factorder'
    order_id = Column(String(30), primary_key=True)
    order_date_id = Column(Integer, ForeignKey('dimdate.date_id'), nullable=False)
    ship_date_id = Column(Integer, ForeignKey('dimdate.date_id'), nullable=False)
    ship_mode_id = Column(Integer, ForeignKey('dimshipmode.ship_mode_id'), nullable=False)
    customer_id = Column(String(20), ForeignKey('dimcustomer.customer_id'), nullable=False)
    product_id = Column(String(30), ForeignKey('dimproduct.product_id'), nullable=False)
    order_priority_id = Column(Integer, ForeignKey('dimorderpriority.order_priority_id'), nullable=False)
    sales = Column(Float(precision=10, decimal_return_scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    discount = Column(Float(precision=4, decimal_return_scale=2), nullable=False)
    profit = Column(Float(precision=10, decimal_return_scale=2), nullable=False)
    shipping_cost = Column(Float(precision=10, decimal_return_scale=2), nullable=False)

# Create all tables in the database
Base.metadata.create_all(engine)
print('Tables Created successfully')
# Optional: Create a session for future data operations
Session = sessionmaker(bind=engine)
session = Session()