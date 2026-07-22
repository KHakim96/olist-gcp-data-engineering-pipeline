SELECT DISTINCT

    DATE(order_purchase_timestamp) AS order_date

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_orders`

WHERE order_purchase_timestamp IS NOT NULL