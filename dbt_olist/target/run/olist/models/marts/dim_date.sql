
  
    

    create or replace table `olist-gcp-data-engineering`.`olist_analytics`.`dim_date`
      
    
    

    
    OPTIONS()
    as (
      SELECT DISTINCT

    DATE(order_purchase_timestamp) AS order_date

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_orders`

WHERE order_purchase_timestamp IS NOT NULL
    );
  