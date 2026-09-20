select
    store_id,
    state_id
from {{ source('retail_demand_source', 'dim_store') }}