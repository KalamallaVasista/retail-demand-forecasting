select
    item_id,
    store_id,
    d,
    units_sold
from {{ source('retail_demand_source', 'fact_sales') }}