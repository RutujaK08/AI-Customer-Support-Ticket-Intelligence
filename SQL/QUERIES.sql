USE customer_support_db;

SELECT
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean;

SELECT
    COUNT(DISTINCT `Customer Email`) AS Total_Customers
FROM customer_support_tickets_clean;

SELECT
    `Ticket Status`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Ticket Status`
ORDER BY Total_Tickets DESC;

SELECT
    `Ticket Priority`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Ticket Priority`
ORDER BY Total_Tickets DESC;

SELECT
    `Ticket Type`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Ticket Type`
ORDER BY Total_Tickets DESC;

SELECT
    `Ticket Channel`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Ticket Channel`
ORDER BY Total_Tickets DESC;

SELECT
    `Product Purchased`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Product Purchased`
ORDER BY Total_Tickets DESC;

SELECT
    ROUND(AVG(`Customer Satisfaction Rating`), 2)
    AS Average_Satisfaction
FROM customer_support_tickets_clean;

SELECT
    `Customer Satisfaction Rating`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
WHERE `Customer Satisfaction Rating` IS NOT NULL
GROUP BY `Customer Satisfaction Rating`
ORDER BY `Customer Satisfaction Rating`;

SELECT
    `Ticket Type`,
    ROUND(AVG(`Customer Satisfaction Rating`), 2) AS Average_Rating
FROM customer_support_tickets_clean
WHERE `Customer Satisfaction Rating` IS NOT NULL
GROUP BY `Ticket Type`
ORDER BY Average_Rating DESC;

SELECT
    `Ticket Priority`,
    ROUND(AVG(`Customer Satisfaction Rating`), 2) AS Average_Rating
FROM customer_support_tickets_clean
WHERE `Customer Satisfaction Rating` IS NOT NULL
GROUP BY `Ticket Priority`
ORDER BY Average_Rating DESC;

SELECT
    `Product Purchased`,
    ROUND(AVG(`Customer Satisfaction Rating`), 2) AS Average_Rating,
    COUNT(`Customer Satisfaction Rating`) AS Rated_Tickets
FROM customer_support_tickets_clean
WHERE `Customer Satisfaction Rating` IS NOT NULL
GROUP BY `Product Purchased`
ORDER BY Average_Rating DESC;

SELECT
    ROUND(AVG(TIMESTAMPDIFF(
        MINUTE,
        `Ticket Date`,
        `First Response Time`
    )), 2) AS Average_Response_Minutes
FROM customer_support_tickets_clean
WHERE `First Response Time` IS NOT NULL
  AND `Ticket Date` IS NOT NULL;
  
  SELECT
    `Ticket ID`,
    `Ticket Date`,
    `First Response Time`,
    TIMESTAMPDIFF(
        MINUTE,
        `Ticket Date`,
        `First Response Time`
    ) AS Response_Minutes
FROM customer_support_tickets_clean
WHERE `First Response Time` IS NOT NULL
LIMIT 10;

DESCRIBE customer_support_tickets_clean;
SELECT
    `Ticket Date`,
    `First Response Time`,
    `Time to Resolution`
FROM customer_support_tickets_clean
LIMIT 10;

SELECT
    COUNT(*) AS Total_Tickets,
    SUM(`First Response Time` IS NULL) AS Missing_Response,
    SUM(`Time to Resolution` IS NULL) AS Missing_Resolution,
    SUM(`Customer Satisfaction Rating` IS NULL) AS Missing_Satisfaction
FROM customer_support_tickets_clean;

SELECT
    `Ticket Priority`,
    ROUND(AVG(TIMESTAMPDIFF(
        MINUTE,
        `Ticket Date`,
        `First Response Time`
    )), 2) AS Average_Response_Minutes
FROM customer_support_tickets_clean
WHERE `First Response Time` IS NOT NULL
  AND `Ticket Date` IS NOT NULL
GROUP BY `Ticket Priority`
ORDER BY Average_Response_Minutes ASC;

SELECT
    `Ticket Priority`,
    ROUND(AVG(TIMESTAMPDIFF(
        MINUTE,
        `Ticket Date`,
        `Time to Resolution`
    )), 2) AS Average_Resolution_Minutes
FROM customer_support_tickets_clean
WHERE `Time to Resolution` IS NOT NULL
  AND `Ticket Date` IS NOT NULL
GROUP BY `Ticket Priority`
ORDER BY Average_Resolution_Minutes ASC;

SELECT
    `Ticket Status`,
    COUNT(*) AS Total_Tickets,
    COUNT(`Time to Resolution`) AS Resolved_Records,
    SUM(`Time to Resolution` IS NULL) AS Missing_Resolution_Records
FROM customer_support_tickets_clean
GROUP BY `Ticket Status`
ORDER BY Total_Tickets DESC;

SELECT
    `Ticket Status`,
    COUNT(*) AS Total_Tickets,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_support_tickets_clean),
        2
    ) AS Percentage
FROM customer_support_tickets_clean
GROUP BY `Ticket Status`
ORDER BY Total_Tickets DESC;

SELECT
    `Ticket Priority`,
    COUNT(*) AS Total_Tickets,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_support_tickets_clean),
        2
    ) AS Percentage
FROM customer_support_tickets_clean
GROUP BY `Ticket Priority`
ORDER BY Total_Tickets DESC;

SELECT
    `Ticket Type`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Ticket Type`
ORDER BY Total_Tickets DESC;

SELECT
    `Ticket Channel`,
    COUNT(*) AS Total_Tickets,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_support_tickets_clean),
        2
    ) AS Percentage
FROM customer_support_tickets_clean
GROUP BY `Ticket Channel`
ORDER BY Total_Tickets DESC;

SELECT
    `Product Purchased`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Product Purchased`
ORDER BY Total_Tickets DESC;

SELECT
    CASE
        WHEN LOWER(`Ticket Status`) = 'closed' THEN 'Closed'
        ELSE 'Unresolved / Pending'
    END AS Ticket_Category,
    COUNT(*) AS Total_Tickets,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_support_tickets_clean),
        2
    ) AS Percentage
FROM customer_support_tickets_clean
GROUP BY Ticket_Category;

SELECT
    COUNT(*) AS Total_Tickets,
    SUM(`First Response Time` IS NULL) AS Missing_Response,
    SUM(`Time to Resolution` IS NULL) AS Missing_Resolution,
    SUM(`Customer Satisfaction Rating` IS NULL) AS Missing_Satisfaction
FROM customer_support_tickets_clean;

SELECT
    `Ticket ID`,
    `Ticket Priority`,
    CASE
        WHEN LOWER(`Ticket Priority`) = 'critical' THEN 'Immediate Attention'
        WHEN LOWER(`Ticket Priority`) = 'high' THEN 'High Attention'
        WHEN LOWER(`Ticket Priority`) = 'medium' THEN 'Normal Attention'
        WHEN LOWER(`Ticket Priority`) = 'low' THEN 'Low Attention'
        ELSE 'Unknown'
    END AS Priority_Category
FROM customer_support_tickets_clean;

SELECT
    `Ticket ID`,
    `Ticket Priority`,
    CASE
        WHEN LOWER(`Ticket Priority`) = 'critical'
            THEN 'Immediate Attention'
        WHEN LOWER(`Ticket Priority`) = 'high'
            THEN 'High Attention'
        WHEN LOWER(`Ticket Priority`) = 'medium'
            THEN 'Normal Attention'
        WHEN LOWER(`Ticket Priority`) = 'low'
            THEN 'Low Attention'
        ELSE 'Unknown'
    END AS Priority_Category
FROM customer_support_tickets_clean;

SELECT
    `Ticket ID`,
    `Customer Satisfaction Rating`,
    CASE
        WHEN `Customer Satisfaction Rating` >= 4
            THEN 'Satisfied'
        WHEN `Customer Satisfaction Rating` = 3
            THEN 'Neutral'
        WHEN `Customer Satisfaction Rating` <= 2
            THEN 'Dissatisfied'
        ELSE 'Not Rated'
    END AS Satisfaction_Category
FROM customer_support_tickets_clean;

SELECT
    `Ticket ID`,
    `Ticket Status`,
    CASE
        WHEN LOWER(`Ticket Status`) = 'closed'
            THEN 'Completed'
        WHEN LOWER(`Ticket Status`) = 'open'
            THEN 'Unresolved'
        WHEN LOWER(`Ticket Status`) LIKE '%pending%'
            THEN 'Waiting for Response'
        ELSE 'Other'
    END AS Status_Category
FROM customer_support_tickets_clean;

SELECT
    `Ticket ID`,
    `Customer Name`,
    `Product Purchased`,
    `Ticket Type`,
    `Ticket Priority`,
    `Ticket Status`
FROM customer_support_tickets_clean
WHERE LOWER(`Ticket Priority`) = 'critical';

SELECT
    `Ticket Type`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Ticket Type`
HAVING COUNT(*) > (
    SELECT AVG(Ticket_Count)
    FROM (
        SELECT COUNT(*) AS Ticket_Count
        FROM customer_support_tickets_clean
        GROUP BY `Ticket Type`
    ) AS Average_Count
)
ORDER BY Total_Tickets DESC;

SELECT
    `Product Purchased`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Product Purchased`
ORDER BY Total_Tickets DESC
LIMIT 5;

SELECT
    `Ticket Type`,
    COUNT(*) AS Total_Tickets
FROM customer_support_tickets_clean
GROUP BY `Ticket Type`
ORDER BY Total_Tickets DESC
LIMIT 5;

SELECT
    `Product Purchased`,
    ROUND(AVG(`Customer Satisfaction Rating`), 2) AS Average_Rating,
    COUNT(`Customer Satisfaction Rating`) AS Rated_Tickets
FROM customer_support_tickets_clean
WHERE `Customer Satisfaction Rating` IS NOT NULL
GROUP BY `Product Purchased`
ORDER BY Average_Rating ASC
LIMIT 5;

WITH Status_Count AS (
    SELECT
        `Ticket Status`,
        COUNT(*) AS Total_Tickets
    FROM customer_support_tickets_clean
    GROUP BY `Ticket Status`
)
SELECT *
FROM Status_Count
ORDER BY Total_Tickets DESC;

WITH Ticket_Count AS (
    SELECT
        `Ticket Type`,
        COUNT(*) AS Total_Tickets
    FROM customer_support_tickets_clean
    GROUP BY `Ticket Type`
),
Satisfaction AS (
    SELECT
        `Ticket Type`,
        ROUND(AVG(`Customer Satisfaction Rating`), 2) AS Average_Rating
    FROM customer_support_tickets_clean
    WHERE `Customer Satisfaction Rating` IS NOT NULL
    GROUP BY `Ticket Type`
)
SELECT
    t.`Ticket Type`,
    t.Total_Tickets,
    s.Average_Rating
FROM Ticket_Count t
LEFT JOIN Satisfaction s
    ON t.`Ticket Type` = s.`Ticket Type`
ORDER BY t.Total_Tickets DESC;

SELECT
    `Product Purchased`,
    COUNT(*) AS Total_Tickets,
    RANK() OVER (
        ORDER BY COUNT(*) DESC
    ) AS Product_Rank
FROM customer_support_tickets_clean
GROUP BY `Product Purchased`;

SELECT
    `Ticket Type`,
    COUNT(*) AS Total_Tickets,
    DENSE_RANK() OVER (
        ORDER BY COUNT(*) DESC
    ) AS Type_Rank
FROM customer_support_tickets_clean
GROUP BY `Ticket Type`;

SELECT
    `Ticket ID`,
    `Ticket Priority`,
    ROW_NUMBER() OVER (
        PARTITION BY `Ticket Priority`
        ORDER BY `Ticket ID`
    ) AS Ticket_Row_No
FROM customer_support_tickets_clean;

SELECT
    `Ticket Type`,
    COUNT(*) AS Total_Tickets,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_support_tickets_clean),
        2
    ) AS Percentage_Contribution
FROM customer_support_tickets_clean
GROUP BY `Ticket Type`
ORDER BY Percentage_Contribution DESC;

SELECT
    `Product Purchased`,
    ROUND(AVG(`Customer Satisfaction Rating`), 2) AS Average_Rating,
    RANK() OVER (
        ORDER BY AVG(`Customer Satisfaction Rating`) DESC
    ) AS Satisfaction_Rank
FROM customer_support_tickets_clean
WHERE `Customer Satisfaction Rating` IS NOT NULL
GROUP BY `Product Purchased`;

SELECT
    `Ticket Channel`,
    COUNT(*) AS Total_Tickets,
    RANK() OVER (
        ORDER BY COUNT(*) DESC
    ) AS Channel_Rank
FROM customer_support_tickets_clean
GROUP BY `Ticket Channel`;

SELECT
    `Product Purchased`,
    COUNT(*) AS Total_Tickets,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_support_tickets_clean),
        2
    ) AS Ticket_Percentage
FROM customer_support_tickets_clean
GROUP BY `Product Purchased`
ORDER BY Total_Tickets DESC
LIMIT 10;

SELECT
    `Ticket Type`,
    COUNT(*) AS Total_Tickets,
    ROUND(AVG(`Customer Satisfaction Rating`), 2) AS Average_Rating
FROM customer_support_tickets_clean
WHERE `Customer Satisfaction Rating` IS NOT NULL
GROUP BY `Ticket Type`
ORDER BY Average_Rating ASC, Total_Tickets DESC;

SELECT
    `Ticket ID`,
    `Customer Name`,
    `Product Purchased`,
    `Ticket Type`,
    `Ticket Priority`,
    `Ticket Status`
FROM customer_support_tickets_clean
WHERE LOWER(`Ticket Priority`) IN ('critical', 'high')
  AND LOWER(`Ticket Status`) <> 'closed'
ORDER BY
    CASE
        WHEN LOWER(`Ticket Priority`) = 'critical' THEN 1
        WHEN LOWER(`Ticket Priority`) = 'high' THEN 2
    END;
    
    SELECT
    `Ticket Channel`,
    COUNT(*) AS Total_Tickets,
    ROUND(
        AVG(`Customer Satisfaction Rating`), 2
    ) AS Average_Rating
FROM customer_support_tickets_clean
GROUP BY `Ticket Channel`
ORDER BY Total_Tickets DESC;

SELECT
    COUNT(*) AS Total_Tickets,

    COUNT(DISTINCT `Customer Email`) AS Unique_Customers,

    SUM(
        CASE WHEN LOWER(`Ticket Status`) = 'closed'
        THEN 1 ELSE 0 END
    ) AS Closed_Tickets,

    SUM(
        CASE WHEN LOWER(`Ticket Status`) = 'open'
        THEN 1 ELSE 0 END
    ) AS Open_Tickets,

    SUM(
        CASE WHEN LOWER(`Ticket Status`) LIKE '%pending%'
        THEN 1 ELSE 0 END
    ) AS Pending_Tickets,

    ROUND(
        AVG(`Customer Satisfaction Rating`), 2
    ) AS Average_Satisfaction,

    SUM(
        CASE WHEN LOWER(`Ticket Priority`) = 'critical'
        THEN 1 ELSE 0 END
    ) AS Critical_Tickets

FROM customer_support_tickets_clean;