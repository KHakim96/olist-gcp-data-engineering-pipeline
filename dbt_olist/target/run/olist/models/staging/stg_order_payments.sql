

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_order_payments`
  OPTIONS()
  as SELECT

    order_id,

    payment_sequential,

    payment_type,

    payment_installments,

    payment_value

FROM `olist-gcp-data-engineering`.`olist_raw`.`olist_order_payments_dataset`;

