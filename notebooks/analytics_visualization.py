import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost', port=5432,
    dbname='analytics_db',
    user='analytics_user',
    password='analytics_pass'
)
print('Connected to PostgreSQL ✅')

# Load data
valid_df = pd.read_sql('SELECT * FROM valid_records', conn)
invalid_df = pd.read_sql('SELECT * FROM invalid_records', conn)
anomaly_df = pd.read_sql('SELECT * FROM anomalies', conn)
summary_df = pd.read_sql('SELECT * FROM summary_metrics ORDER BY computed_at DESC LIMIT 1', conn)

print(f'Valid Records  : {len(valid_df)}')
print(f'Invalid Records: {len(invalid_df)}')
print(f'Anomalies      : {len(anomaly_df)}')

# Chart 1 - Validation Pie Chart
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie([len(valid_df), len(invalid_df)],
       labels=['Valid Records', 'Invalid Records'],
       colors=['#2ecc71', '#e74c3c'],
       autopct='%1.1f%%', startangle=90)
ax.set_title('Data Validation Summary', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../data/chart_validation.png', dpi=150)
plt.show()
print('Chart 1 saved ✅')

# Chart 2 - Revenue by Region
region_df = valid_df.groupby('region')['total_amount'].sum().reset_index()
region_df = region_df.sort_values('total_amount', ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=region_df, x='region', y='total_amount', palette='Blues_d', ax=ax)
ax.set_title('Total Revenue by Region', fontsize=14, fontweight='bold')
ax.set_xlabel('Region')
ax.set_ylabel('Total Revenue ($)')
for p in ax.patches:
    ax.annotate(f'${p.get_height():,.0f}',
                (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('../data/chart_revenue_region.png', dpi=150)
plt.show()
print('Chart 2 saved ✅')

# Chart 3 - Revenue by Category
cat_df = valid_df.groupby('category')['total_amount'].sum().reset_index()
cat_df = cat_df.sort_values('total_amount', ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=cat_df, x='category', y='total_amount', palette='Oranges_d', ax=ax)
ax.set_title('Total Revenue by Category', fontsize=14, fontweight='bold')
ax.set_xlabel('Category')
ax.set_ylabel('Total Revenue ($)')
for p in ax.patches:
    ax.annotate(f'${p.get_height():,.0f}',
                (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('../data/chart_revenue_category.png', dpi=150)
plt.show()
print('Chart 3 saved ✅')

# Chart 4 - Daily Revenue Trend
valid_df['transaction_date'] = pd.to_datetime(valid_df['transaction_date'])
daily_df = valid_df.groupby('transaction_date')['total_amount'].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(daily_df['transaction_date'], daily_df['total_amount'],
        marker='o', color='#3498db', linewidth=2)
ax.fill_between(daily_df['transaction_date'], daily_df['total_amount'],
                alpha=0.1, color='#3498db')
ax.set_title('Daily Revenue Trend', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../data/chart_daily_trend.png', dpi=150)
plt.show()
print('Chart 4 saved ✅')

# Chart 5 - Anomaly Distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

type_counts = anomaly_df['anomaly_type'].value_counts()
axes[0].pie(type_counts.values, labels=type_counts.index,
            autopct='%1.1f%%', colors=['#e74c3c', '#f39c12'])
axes[0].set_title('Anomalies by Type')

axes[1].bar(anomaly_df['record_id'], anomaly_df['anomaly_score'], color='#e74c3c')
axes[1].set_title('Anomaly Scores by Record')
axes[1].set_xlabel('Record ID')
axes[1].set_ylabel('Z-Score')
axes[1].axhline(y=2.5, color='black', linestyle='--', label='Threshold (2.5)')
axes[1].legend()

plt.suptitle('Anomaly Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../data/chart_anomalies.png', dpi=150)
plt.show()
print('Chart 5 saved ✅')

# Summary
print('\n' + '='*50)
print('ANALYTICS PLATFORM - PIPELINE SUMMARY')
print('='*50)
s = summary_df.iloc[0]
print(f'Total Records Ingested : {s["total_records"]}')
print(f'Valid Records          : {s["valid_records"]}')
print(f'Invalid Records        : {s["invalid_records"]}')
print(f'Anomalies Detected     : {s["anomaly_count"]}')
print(f'Total Revenue          : ${s["total_revenue"]:,.2f}')
print(f'Avg Order Value        : ${s["avg_order_value"]:,.2f}')
print(f'Top Region             : {s["top_region"]}')
print(f'Top Category           : {s["top_category"]}')
print('='*50)

conn.close()
print('\nAll charts saved to /data folder ✅')