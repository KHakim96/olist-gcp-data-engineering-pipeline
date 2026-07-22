
  
    

    create or replace table `olist-gcp-data-engineering`.`olist_analytics`.`fact_reviews`
      
    
    

    
    OPTIONS()
    as (
      SELECT *

FROM `olist-gcp-data-engineering`.`olist_analytics`.`int_review_metrics`
    );
  