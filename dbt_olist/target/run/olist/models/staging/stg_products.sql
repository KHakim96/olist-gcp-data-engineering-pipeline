

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_products`
  OPTIONS()
  as SELECT

    product_id,

    product_category_name,

    product_name_lenght,

    product_description_lenght,

    product_photos_qty,

    product_weight_g,

    product_length_cm,

    product_height_cm,

    product_width_cm

FROM `olist-gcp-data-engineering`.`olist_raw`.`olist_products_dataset`;

