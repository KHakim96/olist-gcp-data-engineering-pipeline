SELECT

    COUNT(DISTINCT fo.order_id) AS total_orders,

    COUNT(DISTINCT dc.customer_unique_id) AS total_customers,

    SUM(fp.total_payment) AS total_revenue,

    AVG(fp.total_payment) AS average_order_value

FROM `olist-gcp-data-engineering`.`olist_analytics`.`fact_orders` AS fo

LEFT JOIN `olist-gcp-data-engineering`.`olist_analytics`.`dim_customer` AS dc

    ON fo.customer_id = dc.customer_id

LEFT JOIN `olist-gcp-data-engineering`.`olist_analytics`.`fact_payments` AS fp

    ON fo.order_id = fp.order_id