SELECT

    order_id,

    COUNT(*) AS payment_count,

    SUM(payment_value) AS total_payment,

    MAX(payment_installments) AS max_installments

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_order_payments`

GROUP BY order_id