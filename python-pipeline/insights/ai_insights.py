import os
import logging

logger = logging.getLogger(__name__)

def generate_insights(summary: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "mock")

    if api_key == "mock" or not api_key:
        return _mock_insights(summary)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""
        You are a data analyst. Based on this sales data summary, provide 3 key business insights:
        - Total Records: {summary.get('total_records')}
        - Valid Records: {summary.get('valid_records')}
        - Invalid Records: {summary.get('invalid_records')}
        - Total Revenue: ${summary.get('total_revenue')}
        - Average Order Value: ${summary.get('avg_order_value')}
        - Anomalies Found: {summary.get('anomaly_count')}
        - Top Region: {summary.get('top_region')}
        - Top Category: {summary.get('top_category')}
        Keep it concise and actionable.
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.warning(f"OpenAI call failed: {e}. Falling back to mock.")
        return _mock_insights(summary)

def _mock_insights(summary: dict) -> str:
    total = summary.get("total_records", 0)
    invalid = summary.get("invalid_records", 0)
    revenue = summary.get("total_revenue", 0)
    anomalies = summary.get("anomaly_count", 0)
    region = summary.get("top_region", "N/A")
    category = summary.get("top_category", "N/A")
    invalid_pct = round((invalid / total * 100), 1) if total > 0 else 0

    return (
        f"1. Data Quality: {invalid_pct}% of records ({invalid}/{total}) failed validation. "
        f"Recommend reviewing data sources for missing customer and product IDs.\n"
        f"2. Revenue Performance: Total revenue of ${revenue} was generated with {anomalies} anomalous "
        f"transactions flagged for review — these may indicate fraud or data entry errors.\n"
        f"3. Growth Opportunity: {region} is the top-performing region and {category} leads in category "
        f"revenue. Consider increasing inventory and marketing spend in these segments."
    )