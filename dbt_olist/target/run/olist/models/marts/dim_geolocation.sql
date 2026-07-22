
  
    

    create or replace table `olist-gcp-data-engineering`.`olist_analytics`.`dim_geolocation`
      
    
    

    
    OPTIONS()
    as (
      SELECT DISTINCT

    geolocation_zip_code_prefix,

    geolocation_city,

    geolocation_state,

    geolocation_lat,

    geolocation_lng

FROM `olist-gcp-data-engineering`.`olist_analytics`.`stg_geolocation`
    );
  