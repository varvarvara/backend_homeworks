from sqlalchemy import create_engine, Column, Integer, Numeric, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

database_url = "postgresql+psycopg2://localhost:5432/mydb"
engine = create_engine(database_url)

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

loans = text("""
CREATE OR REPLACE FUNCTION get_taxed_price(product_id_param INT)
RETURNS NUMERIC AS $$
DECLARE
    current_price NUMERIC;
BEGIN
    SELECT price INTO current_price 
    FROM products 
    WHERE id = product_id_param;

    IF current_price > 5000 THEN
        RETURN current_price * 1.15;
    ELSE
        RETURN current_price + 1.05;
    END IF;
END;
$$ LANGUAGE plpgsql;
""")

Base.metadata.create_all(engine)

with engine.begin() as conn:
    conn.execute(loans)

with engine.begin() as conn:
    product_id = conn.execute(
        text("""
            INSERT INTO products (name, price)
            VALUES ('Ноутбук', 6000)
            RETURNING id
        """)
    ).scalar_one()

with engine.connect() as conn:
    taxed_price = conn.execute(
        text("SELECT get_taxed_price(:pid)"),
        {"pid": product_id}
    ).scalar_one()

print(f"id={product_id}, цена с налогом={taxed_price}")
