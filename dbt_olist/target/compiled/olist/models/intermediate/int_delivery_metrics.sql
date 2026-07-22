SELECT

    order_id,

    customer_id,

    order_status,

    order_purchase_timestamp,

    order_approved_at,

    order_delivered_carrier_date,

    order_delivered_customer_date,

    order_estimated_delivery_date,

    -- Purchase → Customer
    DATE_DIFF(
        DATE(order_delivered_customer_date),
        DATE(order_purchase_timestamp),
        DAY
    ) AS delivery_days,

    -- Purchase → Carrier
    DATE_DIFF(
        DATE(order_delivered_carrier_date),
        DATE(order_purchase_timestamp),
        DAY
    ) AS shipping_days,

    -- Estimated → Actual
    DATE_DIFF(
        DATE(order_delivered_customer_date),
        DATE(order_estimated_delivery_date),
        DAY
    ) AS delay_days,

    CASE
        WHEN order_delivered_customer_date
             <= order_estimated_delivery_date
        THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_orders`

WHERE order_delivered_customer_date IS NOT NULL