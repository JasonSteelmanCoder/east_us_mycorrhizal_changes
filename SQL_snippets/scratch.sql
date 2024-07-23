

ROUND(
    (
        SUM(totaln)
        / (SUM(dayssample * criteria1::DECIMAL / 100)) 
        * 365
    )::DECIMAL
    , 3
) AS n_kg_ha_yr