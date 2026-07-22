
  
    

    create or replace table `olist-gcp-data-engineering`.`olist_analytics`.`fact_order_items`
      
    
    

    
    OPTIONS()
    as (
      SELECT *

FROM `olist-gcp-data-engineering`.`olist_analytics`.`int_order_items`
    );
  