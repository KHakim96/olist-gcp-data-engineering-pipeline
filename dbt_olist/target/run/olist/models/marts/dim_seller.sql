
  
    

    create or replace table `olist-gcp-data-engineering`.`olist_analytics`.`dim_seller`
      
    
    

    
    OPTIONS()
    as (
      SELECT DISTINCT

    seller_id,

    seller_zip_code_prefix,

    seller_city,

    seller_state

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_sellers`
    );
  