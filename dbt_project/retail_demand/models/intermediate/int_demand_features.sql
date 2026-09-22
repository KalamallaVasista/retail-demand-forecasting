with daily_demand as (

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
        snap_wi
    from {{ ref('int_daily_demand') }}

),

demand_features as (

    select
        *,

        lag(units_sold, 1) over (
            partition by item_id, store_id
            order by date
        ) as lag_1,

        lag(units_sold, 7) over (
            partition by item_id, store_id
            order by date
        ) as lag_7,

        lag(units_sold, 28) over (
            partition by item_id, store_id
            order by date
        ) as lag_28,

        avg(units_sold) over (
            partition by item_id, store_id
            order by date
            rows between 7 preceding and 1 preceding
        ) as rolling_mean_7,

        avg(units_sold) over (
            partition by item_id, store_id
            order by date
            rows between 28 preceding and 1 preceding
        ) as rolling_mean_28

    from daily_demand

)

select *
from demand_features