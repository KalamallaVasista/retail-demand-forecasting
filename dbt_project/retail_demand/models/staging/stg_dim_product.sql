select
    item_id,
    dept_id,
    cat_id
from {{ source('retail_demand_source', 'dim_product') }}