
  
    

    create or replace table `olist-gcp-data-engineering`.`olist_analytics`.`fact_payments`
      
    
    

    
    OPTIONS()
    as (
      SELECT *

FROM `olist-gcp-data-engineering`.`olist_analytics`.`int_payment_summary`
    );
  