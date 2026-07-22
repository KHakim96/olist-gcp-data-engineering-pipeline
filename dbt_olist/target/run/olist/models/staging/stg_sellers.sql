

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_sellers`
  OPTIONS()
  as SELECT

    seller_id,

    seller_zip_code_prefix,

    seller_city,

    seller_state

FROM `olist-gcp-data-engineering`.`olist_raw`.`olist_sellers_dataset`;

