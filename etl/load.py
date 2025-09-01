from transform import transform
from Createtable import DimDate, DimShipMode, DimCustomer, DimProduct, DimOrderPriority, FactOrder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

def load():
    df, all_dates = transform()
    # set environment variable for security
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    server_address = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    
    # Set up SQLAlchemy engine and session
    engine = create_engine(f'postgresql://{user}:{password}@{sever_address}/{dbname}') # change user & password with your database
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Load dimdate
        for date in all_dates:
            # Extract date parts
            day = date.day
            month = date.month
            quarter = ((date.month - 1) // 3) + 1
            year = date.year
            # Check if date already exists to avoid duplicates
            if not session.query(DimDate).filter_by(full_date=date.date()).first():
                dim_date = DimDate(
                    full_date=date.date(),
                    day=day,
                    month=month,
                    quarter=quarter,
                    year=year
                )
                session.add(dim_date)

        # Load dimshipmode
        for _, row in df.iterrows():
            if not session.query(DimShipMode).filter_by(ship_mode=row['Ship Mode']).first():
                dim_shipmode = DimShipMode(
                    ship_mode=row['Ship Mode']
                )
                session.add(dim_shipmode)

        # Load dimproduct
        for _,row in df.iterrows():
            if not session.query(DimProduct).filter_by(product_id=row['Product ID']).first():
                dim_product = DimProduct(
                    product_id=row['Product ID'],
                    category=row['Category'],
                    sub_category=row['Sub-Category'],
                    product_name=row['Product Name']
                )
                session.add(dim_product)

        # Load dimorderpriority
        for _,row in df.iterrows():
            if not session.query(DimOrderPriority).filter_by(order_priority=row['Order Priority']).first():
                dim_order_priority= DimOrderPriority(
                    order_priority=row['Order Priority']
                )
                session.add(dim_order_priority)
            
        # Load dimcustomer
        for _, row in df.iterrows():
            if not session.query(DimCustomer).filter_by(customer_id=row['Customer ID']).first():
                dim_customer = DimCustomer(
                    customer_id=row['Customer ID'],
                    customer_name=row['Customer Name'],
                    segment=row['Segment'],
                    city=row['City'],
                    state=row['State'],
                    country=row['Country'],
                    postal_code=row['Postal Code'],
                    region=row.get('Region', None)
                )
                session.add(dim_customer)
        
        session.commit()
        print("Dimension tables loaded.")

        for _, row in df.iterrows():
            # Lookup foreign keys
            order_date_id = session.query(DimDate).filter_by(full_date=row['Order Date'].date()).first().date_id
            ship_date_id = session.query(DimDate).filter_by(full_date=row['Ship Date'].date()).first().date_id
            ship_mode_id = session.query(DimShipMode).filter_by(ship_mode=row['Ship Mode']).first().ship_mode_id
            customer_id = row['Customer ID']
            product_id = row['Product ID']
            order_priority_id = session.query(DimOrderPriority).filter_by(order_priority=row['Order Priority']).first().order_priority_id

            # Insert fact row
            if not session.query(FactOrder).filter_by(order_id=row['Order ID']).first():
                session.add(FactOrder(
                    order_id=row['Order ID'],
                    order_date_id=order_date_id,
                    ship_date_id=ship_date_id,
                    ship_mode_id=ship_mode_id,
                    customer_id=customer_id,
                    product_id=product_id,
                    order_priority_id=order_priority_id,
                    sales=row['Sales'],
                    quantity=row['Quantity'],
                    discount=row['Discount'],
                    profit=row['Profit'],
                    shipping_cost=row['Shipping Cost']
                ))        
        
        # commit load fact order
        session.commit()
        print("Fact table loaded")
    # Catch errors and undo them
    except Exception as e:
        session.rollback()
        print("Error", e)
    finally:
        session.close()

if __name__ == "__main__":
    load()