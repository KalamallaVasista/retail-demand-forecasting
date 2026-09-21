with sales as (

    select
        item_id,
        store_id,
        d,
        units_sold
    from {{ ref('stg_fact_sales') }}

),

dates as (

    select
        date,
        d,
        wm_yr_wk,
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
    from {{ ref('stg_dim_date') }}

),

products as (

    select
        item_id,
        dept_id,
        cat_id
    from {{ ref('stg_dim_product') }}

),

stores as (

    select
        store_id,
        state_id
    from {{ ref('stg_dim_store') }}

),

prices as (

    select
        store_id,
        item_id,
        wm_yr_wk,
        sell_price
    from {{ ref('stg_fact_prices') }}

)

select
    sales.item_id,
    sales.store_id,
    dates.date,
    sales.d,
    dates.wm_yr_wk,
    products.dept_id,
    products.cat_id,
    stores.state_id,
    sales.units_sold,
    prices.sell_price,
    dates.weekday,
    dates.wday,
    dates.month,
    dates.year,
    dates.event_name_1,
    dates.event_type_1,
    dates.event_name_2,
    dates.event_type_2,
    dates.snap_ca,
    dates.snap_tx,
    dates.snap_wi

from sales

inner join dates
    on sales.d = dates.d

inner join products
    on sales.item_id = products.item_id

inner join stores
    on sales.store_id = stores.store_id

left join prices
    on sales.item_id = prices.item_id
    and sales.store_id = prices.store_id
    and dates.wm_yr_wk = prices.wm_yr_wk