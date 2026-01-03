import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Generate 10,000 orders
np.random.seed(42)
n_orders = 10000

# Create realistic e-commerce data
orders = pd.DataFrame({
    'order_id': [f'ORD{str(i).zfill(6)}' for i in range(1, n_orders + 1)],
    'customer_id': [f'CUST{random.randint(1, 2000):05d}' for _ in range(n_orders)],
    'order_date': [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(n_orders)],
    'product_id': [f'PROD{random.randint(1, 500):04d}' for _ in range(n_orders)],
    'product_name': np.random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
                                       'Webcam', 'USB Cable', 'Charger', 'Phone', 'Tablet'], n_orders),
    'quantity': np.random.randint(1, 5, n_orders),
    'unit_price': np.random.uniform(10, 1000, n_orders).round(2),
    'country': np.random.choice(['Canada', 'USA', 'UK', 'Germany', 'France'], n_orders),
    'status': np.random.choice(['pending', 'shipped', 'delivered', 'cancelled'], n_orders, p=[0.1, 0.3, 0.5, 0.1])
})

# Calculate total
orders['total_amount'] = (orders['quantity'] * orders['unit_price']).round(2)

# Add some data quality issues (real world scenarios)
# 1. Missing values (2% of customer_ids)
orders.loc[orders.sample(frac=0.02).index, 'customer_id'] = None

# 2. Duplicate orders (1%)
duplicates = orders.sample(frac=0.01)
orders = pd.concat([orders, duplicates], ignore_index=True)

# 3. Invalid dates (0.5% - future dates)
invalid_dates_idx = orders.sample(frac=0.005).index
orders.loc[invalid_dates_idx, 'order_date'] = datetime.now() + timedelta(days=random.randint(1, 30))

# Save files
orders.to_csv('orders_2026_01_02.csv', index=False)
print(f"Generated {len(orders)} orders with intentional data quality issues")
print(f"Missing customer_ids: {orders['customer_id'].isna().sum()}")
print(f"Duplicate order_ids: {orders['order_id'].duplicated().sum()}")