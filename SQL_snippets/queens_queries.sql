SELECT * FROM ny_plot WHERE countycd = 81;



SELECT ny_county.statecd, ny_county.unitcd, ny_county.countycd, ny_county.countynm, ny_plot.plot
FROM ny_county
JOIN ny_plot
ON ny_county.countycd = ny_plot.countycd
WHERE ny_county.countynm = 'Queens';