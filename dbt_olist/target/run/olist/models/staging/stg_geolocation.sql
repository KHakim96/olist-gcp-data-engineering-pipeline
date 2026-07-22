

  create or replace view `olist-gcp-data-engineering`.`olist_analytics`.`stg_geolocation`
  OPTIONS()
  as SELECT

    geolocation_zip_code_prefix,

    geolocation_lat,

    geolocation_lng,

    geolocation_city,

    geolocation_state

FROM `olist-gcp-data-engineering`.`olist_raw`.`olist_geolocation_dataset`;

