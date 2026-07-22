

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_order_items`
  OPTIONS()
  as SELECT

    order_id,

    order_item_id,

    product_id,

    seller_id,

    shipping_limit_date,

    price,

    freight_value

FROM `olist-gcp-data-engineering`.`olist_raw`.`olist_order_items_dataset`;

