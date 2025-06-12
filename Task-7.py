import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to (or create) SQLite database
conn = sqlite3.connect(r"E:\Elevate Labs\Task-7\sales_data.db")
cursor = conn.cursor()

# Step 2: Create a sales table (only if it doesn’t already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')

# Step 3: Insert some sample data if table is empty
cursor.execute("SELECT COUNT(*) FROM sales")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("Apple", 10, 1.0),
        ("Banana", 5, 0.5),
        ("Apple", 4, 1.0),
        ("Orange", 8, 1.2),
        ("Banana", 7, 0.5)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()

# Step 4: Query total quantity sold and total revenue per product
query = '''
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue 
FROM sales 
GROUP BY product
'''
df = pd.read_sql_query(query, conn)

# Step 5: Print the sales summary
print("SALES SUMMARY")
print(df)

# Step 6: Create a bar chart for revenue per product
df.plot(kind='bar', x='product', y='revenue', legend=False)
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.xlabel("Product")
plt.tight_layout()

# Save and show chart
plt.savefig(r"E:\Elevate Labs\Task-7\sales_chart.png")
plt.show()

# Step 7: Close the database connection
conn.close()
