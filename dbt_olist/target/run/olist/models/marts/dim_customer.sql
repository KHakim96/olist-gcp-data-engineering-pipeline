
  
    

    create or replace table `olist-gcp-data-engineering`.`olist_analytics`.`dim_customer`
      
    
    

    
    OPTIONS()
    as (
      SELECT DISTINCT

    customer_id,

    customer_unique_id,

    customer_city,

    customer_state

FROM `olist-gcp-data-engineering`.`olist_analytics`.`int_customer_orders`
    );
  