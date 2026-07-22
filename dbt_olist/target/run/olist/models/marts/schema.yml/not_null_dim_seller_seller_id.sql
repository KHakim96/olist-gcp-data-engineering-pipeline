
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select seller_id
from `olist-gcp-data-engineering`.`olist_analytics`.`dim_seller`
where seller_id is null



  
  
      
    ) dbt_internal_test