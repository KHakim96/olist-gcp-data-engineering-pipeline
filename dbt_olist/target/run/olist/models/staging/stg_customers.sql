

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_customers`
  OPTIONS()
  as SELECT

    customer_id,

    customer_unique_id,

    customer_zip_code_prefix,

    customer_city,

    customer_state

FROM `olist-gcp-data-engineering`.`olist_raw`.`olist_customers_dataset`;

