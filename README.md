Developed by Dyllan Segura. Version 1.
Notes on improvements are currently inside the code; in the next version they will be removed and documented here along with the fixes. The project is actively under development.

Businessproject generates realistic synthetic datasets for an e-commerce business, including three dataframes (orders, customers, and products) that are exported into Excel tables. The data is designed for SQL analysis and Power BI visualization, as part of an exercise to apply tools from each program throughout the process.

Realistic distributions were considered: customer repetition, seasonal sales peaks (May and December), payment methods by category and weight. The dataset contains 15,000 orders with coherent dates, prices, and customer behavior. Dates range from 2021 to 2025, with order times between 8:00 and 21:00.

Python libraries used: NumPy, Pandas, Random, Datetime.
