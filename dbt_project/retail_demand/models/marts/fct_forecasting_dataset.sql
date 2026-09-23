with demand_features as (

    select
        item_id,
        store_id,
        date,
        d,
        wm_yr_wk,
        dept_id,
        cat_id,
        state_id,
        units_sold,
        sell_price,
        weekday,
        wday,
        month,
        year,
        event_name_1,
        event_type_1,
        event_name_2,
        event_type_2,
        snap_ca,
        snap_tx,
        snap_wi,
        lag_1,
        lag_7,
        lag_28,
        rolling_mean_7,
        rolling_mean_28

    from {{ ref('int_demand_features') }}

)

select *
from demand_features

where lag_28 is not null