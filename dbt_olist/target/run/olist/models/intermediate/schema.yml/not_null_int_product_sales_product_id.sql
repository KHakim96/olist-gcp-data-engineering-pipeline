
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select product_id
from `olist-gcp-data-engineering`.`olist_analytics`.`int_product_sales`
where product_id is null



  
  
      
    ) dbt_internal_test