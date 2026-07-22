

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`int_review_metrics`
  OPTIONS()
  as SELECT

    order_id,

    review_score,

    review_creation_date

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_order_reviews`;

