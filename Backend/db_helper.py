import psycopg2
import os


def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


# Insert items of an order
def insert_order_item(food_item, quantity, order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO order_items (order_id, food_name, quantity)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (order_id, food_item, quantity))

        conn.commit()
        cursor.close()
        conn.close()

        return 1

    except Exception as e:
        print("Error inserting order item:", e)
        return -1


# Insert order tracking status
def insert_order_tracking(order_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO orders (id, status)
    VALUES (%s, %s)
    """
    cursor.execute(query, (order_id, status))

    conn.commit()
    cursor.close()
    conn.close()


# Get total order price
def get_total_order_price(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT SUM(f.price * oi.quantity)
    FROM order_items oi
    JOIN food_items f ON oi.food_name = f.name
    WHERE oi.order_id = %s
    """
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result if result else 0


# Get next order ID
def get_next_order_id():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT COALESCE(MAX(id), 0) + 1 FROM orders"
    cursor.execute(query)
    next_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return next_id


# Get order status
def get_order_status(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT status FROM orders WHERE id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else None

