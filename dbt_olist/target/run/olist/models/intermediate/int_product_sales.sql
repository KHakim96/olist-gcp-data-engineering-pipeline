

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`int_product_sales`
  OPTIONS()
  as SELECT

    product_id,

    COUNT(*) AS total_items_sold,

    SUM(price) AS total_sales,

    AVG(price) AS average_price

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_order_items`

GROUP BY product_id;

