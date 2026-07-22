

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_order_reviews`
  OPTIONS()
  as SELECT

    review_id,

    order_id,

    review_score,

    review_comment_title,

    review_comment_message,

    review_creation_date,

    review_answer_timestamp

FROM `olist-gcp-data-engineering`.`olist_raw`.`olist_order_reviews_dataset`;

