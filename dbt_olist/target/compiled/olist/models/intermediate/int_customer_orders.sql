SELECT

    o.order_id,

    o.customer_id,

    c.customer_unique_id,

    c.customer_city,

    c.customer_state,

    o.order_status,

    o.order_purchase_timestamp,

    o.order_approved_at,

    o.order_delivered_carrier_date,

    o.order_delivered_customer_date,

    o.order_estimated_delivery_date

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_orders` AS o

LEFT JOIN `olist-gcp-data-engineering`.`olist_analytics`.`stg_customers` AS c

    ON o.customer_id = c.customer_id