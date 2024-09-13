ALTER TABLE worms_drake
ADD statecd smallint;

ALTER TABLE worms_drake
ADD countycd smallint;

UPDATE worms_drake
SET statecd = SUBSTRING(fips, 1, 2)::smallint;

UPDATE worms_drake
SET countycd = 
    CASE
  	    WHEN TRIM(LEADING '0' FROM SUBSTRING(fips, 3)) != ''
  	    THEN TRIM(LEADING '0' FROM SUBSTRING(fips, 3))::smallint
   	    ELSE NULL
    END
;