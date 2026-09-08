import requests
import duckdb
import pandas as pd
import random
from datetime import datetime, timedelta

def fetch_api_data():
    print("Fetching raw data from E-Commerce REST API...")
    users_res = requests.get('https://fakestoreapi.com/users')
    products_res = requests.get('https://fakestoreapi.com/products')
    
    # Duplicate users to create a realistic 100-customer dataset
    base_users = users_res.json()
    users = []
    for i in range(50):
        for u in base_users:
            u_copy = u.copy()
            u_copy['id'] = u['id'] + (i * 10)
            users.append(u_copy)
            
    products = products_res.json()
    return users, products

def simulate_event_stream_and_orders(users, products):
    print("Simulating customer funnel drop-offs and order histories...")
    random.seed(42)
    
    orders = []
    events = []
    discount_codes = ['PROMO10', 'SUMMER20', 'WELCOME15', 'NODISCOUNT']
    
    base_date = datetime.now() - timedelta(days=90)
    order_id = 1000
    
    for user in users:
        user_id = user['id']
        
        # Real-world Funnel Drop-off Simulation
        # 100% view page, 70% view product, 40% add to cart, 20% checkout, 8% purchase
        event_date = base_date + timedelta(days=random.randint(1, 85))
        
        # Step 1: Page View (100%)
        events.append({"event_id": f"EVT_{random.randint(100000, 999999)}", "user_id": user_id, "event_type": "page_view", "event_timestamp": event_date.strftime("%Y-%m-%d %H:%M:%S")})
        
        if random.random() < 0.75:
            # Step 2: Product View (75%)
            events.append({"event_id": f"EVT_{random.randint(100000, 999999)}", "user_id": user_id, "event_type": "product_view", "event_timestamp": event_date.strftime("%Y-%m-%d %H:%M:%S")})
            
            if random.random() < 0.45:
                # Step 3: Add to Cart (45%)
                events.append({"event_id": f"EVT_{random.randint(100000, 999999)}", "user_id": user_id, "event_type": "add_to_cart", "event_timestamp": event_date.strftime("%Y-%m-%d %H:%M:%S")})
                
                if random.random() < 0.25:
                    # Step 4: Checkout Start (25%)
                    events.append({"event_id": f"EVT_{random.randint(100000, 999999)}", "user_id": user_id, "event_type": "checkout_start", "event_timestamp": event_date.strftime("%Y-%m-%d %H:%M:%S")})
                    
                    if random.random() < 0.60:
                        # Step 5: Purchase (60% of checkouts)
                        events.append({"event_id": f"EVT_{random.randint(100000, 999999)}", "user_id": user_id, "event_type": "purchase", "event_timestamp": event_date.strftime("%Y-%m-%d %H:%M:%S")})
                        
                        # Generate 1 to 6 orders per customer to vary RFM segmentation
                        num_orders = random.choices([1, 2, 3, 5], weights=[0.5, 0.3, 0.15, 0.05])[0]
                        for _ in range(num_orders):
                            order_id += 1
                            ord_date = base_date + timedelta(days=random.randint(1, 88))
                            selected_product = random.choice(products)
                            qty = random.randint(1, 2)
                            applied_discount = random.choice(discount_codes)
                            discount_pct = 0.20 if applied_discount == 'SUMMER20' else (0.15 if applied_discount == 'WELCOME15' else (0.10 if applied_discount == 'PROMO10' else 0.0))
                            
                            gross_amount = round(selected_product['price'] * qty, 2)
                            discount_amount = round(gross_amount * discount_pct, 2)
                            net_amount = round(gross_amount - discount_amount, 2)
                            
                            orders.append({
                                "order_id": order_id,
                                "user_id": user_id,
                                "order_timestamp": ord_date.strftime("%Y-%m-%d %H:%M:%S"),
                                "product_id": selected_product['id'],
                                "category": selected_product['category'],
                                "quantity": qty,
                                "unit_price": selected_product['price'],
                                "gross_amount": gross_amount,
                                "discount_code": applied_discount,
                                "discount_amount": discount_amount,
                                "net_amount": net_amount
                            })
                    
    return pd.DataFrame(users), pd.DataFrame(orders), pd.DataFrame(events)

def load_to_duckdb(df_users, df_orders, df_events):
    print("Loading raw data into DuckDB database...")
    con = duckdb.connect('ecommerce.duckdb')
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    con.execute("CREATE OR REPLACE TABLE raw.users AS SELECT * FROM df_users;")
    con.execute("CREATE OR REPLACE TABLE raw.orders AS SELECT * FROM df_orders;")
    con.execute("CREATE OR REPLACE TABLE raw.events AS SELECT * FROM df_events;")
    con.close()

if __name__ == '__main__':
    users, products = fetch_api_data()
    df_users, df_orders, df_events = simulate_event_stream_and_orders(users, products)
    load_to_duckdb(df_users, df_orders, df_events)
    print("Injected realistic funnel drop-offs & varied RFM order data!")