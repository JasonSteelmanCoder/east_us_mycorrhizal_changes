
-- This program makes a table of FIPS for all of the counties in the Eastern US. 

-- For this program to run properly, download county_fips_master.csv from https://github.com/kjhealy/fips-codes/blob/master/county_fips_master.csv, 
-- then, copy the csv into your database as county_fips.

CREATE TABLE east_us_fips
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

-- Clean up by deleting the original table from the database:

-- DROP TABLE county_fips;    