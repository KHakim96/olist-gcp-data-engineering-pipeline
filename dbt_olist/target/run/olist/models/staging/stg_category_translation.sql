

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_category_translation`
  OPTIONS()
  as SELECT

    product_category_name,

    product_category_name_english

FROM `olist-gcp-data-engineering`.`olist_raw`.`product_category_name_translation`;

