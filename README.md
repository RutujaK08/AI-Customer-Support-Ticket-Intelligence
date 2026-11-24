# AI Customer Support Ticket Intelligence

## Project Overview

Customer support teams receive thousands of tickets from customers reporting product issues, service complaints, and other concerns. Analyzing these tickets helps businesses understand customer problems, monitor support performance, and improve customer experience.

**AI Customer Support Ticket Intelligence** is a data analytics project focused on analyzing customer support ticket data to identify trends, understand customer issues, evaluate ticket performance, and generate meaningful business insights.

The project uses Python for data cleaning and exploratory data analysis, SQL for querying and business analysis, and Power BI for interactive data visualization.

## Business Objectives

- Analyze customer support ticket patterns and trends.
- Identify the most common customer complaints and ticket categories.
- Understand ticket distribution across different priorities and statuses.
- Analyze customer satisfaction and support performance.
- Identify data quality issues and missing values.
- Present actionable insights through interactive dashboards.

## Dataset Information

- **Dataset:** Customer Support Ticket Dataset
- **Total Records:** 8,469
- **Total Columns:** 17
- **Format:** CSV

### Key Dataset Attributes

- Ticket ID
- Customer Name
- Customer Age
- Customer Gender
- Product Purchased
- Date of Purchase
- Ticket Type
- Ticket Subject
- Ticket Description
- Ticket Status
- Resolution
- Ticket Priority
- Ticket Channel
- First Response Time
- Time to Resolution
- Customer Satisfaction Rating

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Data cleaning and exploratory analysis |
| Pandas | Data manipulation and transformation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| SQL | Data querying and business analysis |
| Power BI | Interactive dashboard development |
| GitHub | Project version control and documentation |

## Project Workflow

### 1. Data Cleaning & Preprocessing – Python

- Loaded and explored the raw dataset.
- Checked for duplicate records.
- Identified and analyzed missing values.
- Handled inconsistent and placeholder values.
- Converted date columns into appropriate datetime formats.
- Performed data validation and quality checks.
- Prepared the dataset for further analysis.

### 2. Exploratory Data Analysis – Python

Performed exploratory analysis to understand:

- Ticket distribution by status and priority.
- Customer and product-related patterns.
- Ticket types and support channels.
- Customer satisfaction trends.
- Missing data patterns.
- Customer and ticket characteristics.

### 3. SQL Analysis

Used SQL to explore the customer support dataset and answer business-related questions through data queries, aggregations, filtering, and analytical operations.

### 4. Power BI Dashboard

Developed a four-page interactive Power BI dashboard to present customer support analytics.

The dashboard focuses on:

- Ticket volume and status analysis.
- Ticket priority and category analysis.
- Customer and product-related insights.
- Support performance and ticket trends.

## Key Business Questions

1. What is the overall distribution of customer support tickets?
2. Which ticket types occur most frequently?
3. Which products receive the highest number of complaints?
4. How are tickets distributed across different priorities?
5. What is the distribution of open, closed, and pending tickets?
6. How does customer satisfaction vary across ticket categories?
7. Which customer support channels are most frequently used?
8. What patterns can be identified in ticket resolution data?

## Project Structure

```text
AI-Customer-Support-Ticket-Intelligence/
│
├── Dataset/
│   ├── raw/
│   │   └── customer_support_tickets.csv
│   │
│   └── processed/
│       └── cleaned_customer_support_tickets.csv
│
├── Python/
│   └── customer_support_analysis.py
│
├── SQL/
│   └── QUERIES.sql
│
├── PowerBI/
│   └── Screenshots/
│       ├── Page1_Ticket_Overview.png
│       ├── Page2_Ticket_Analysis.png
│       └── Page3_Customer_Insights.png
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

*Update the folder and file names above to match your final GitHub repository structure.*

## Key Learnings

- Practical experience in handling real-world-style customer support data.
- Identifying and investigating data quality issues.
- Applying Python for data cleaning and exploratory analysis.
- Writing SQL queries to extract meaningful business insights.
- Designing interactive dashboards using Power BI.
- Translating analytical findings into business-oriented insights.

## Future Improvements

- Advanced customer complaint text analysis.
- Automated ticket categorization.
- AI-assisted ticket summarization and resolution recommendations.
- Further optimization of customer support performance analysis.

## Conclusion

This project demonstrates an end-to-end data analytics workflow, from raw data exploration and preprocessing to SQL analysis and interactive Power BI reporting.

It highlights how data analytics can help businesses better understand customer issues, evaluate support operations, and make informed decisions to improve customer experience.

---

**Author:** Rutuja Kundangar

**GitHub:** https://github.com/RutujaK08

