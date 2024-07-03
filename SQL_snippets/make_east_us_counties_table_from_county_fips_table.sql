
-- This program makes a table of FIPS for all of the counties in the Eastern US. 

-- For this program to run properly, download county_fips_master.csv from https://github.com/kjhealy/fips-codes/blob/master/county_fips_master.csv, 
-- then, copy the csv into your database as county_fips.

CREATE TABLE east_us_counties
AS (
  SELECT fips, county_name, state_abbr, state_name, state AS statecd, county AS countycd, region_name, division_name
  FROM county_fips
  WHERE state_name IN (
    'Alabama', 
    'Connecticut', 
    'Delaware',
		'Florida',
		'Georgia',
		'Illinois',
		'Indiana',
		'Kentucky',
		'Maine',
		'Maryland',
		'Massachusetts',
		'Michigan',
		'Mississippi',
		'New Hampshire',
		'New Jersey',
		'New York',
		'North Carolina',
		'Ohio',
		'Pennsylvania',
		'Rhode Island',
		'South Carolina',
		'Tennessee',
		'Vermont',
		'Virginia',
		'West Virginia',
		'Wisconsin'
  )
);

-- Delete a city that merged into another county and therefore has 'NA' for statecd and countycd
DELETE FROM east_us_counties WHERE county_name = 'Bedford city' AND state_abbr = 'VA'

-- cast statecd and countycd as smallint for consistency with other tables
ALTER TABLE east_us_counties
ALTER COLUMN statecd
TYPE smallint
USING statecd::smallint;

ALTER TABLE east_us_counties
ALTER COLUMN countycd
TYPE smallint
USING countycd::smallint;

-- Clean up by deleting the original table from the database:

-- DROP TABLE county_fips;    