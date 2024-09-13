-- Split new_try_data into three tables, each representing only one trait
CREATE TABLE cleaned_try_decomp
AS (
	SELECT * FROM new_try_data WHERE traitid = 39
)

CREATE TABLE cleaned_try_c_n
AS (
	SELECT * FROM new_try_data WHERE traitid = 150
)

CREATE TABLE cleaned_try_bark_diameter
AS (
	SELECT * FROM new_try_data WHERE traitid = 839
)



-- remove empty column from each new table
ALTER TABLE cleaned_try_bark_diameter
DROP COLUMN stdvaluestr

ALTER TABLE cleaned_try_c_n
DROP COLUMN stdvaluestr

ALTER TABLE cleaned_try_decomp
DROP COLUMN stdvaluestr





-- set a standard unit for bark to diameter (it's a ratio)
UPDATE cleaned_try_bark_diameter
SET unitname = 'mm/mm'

-- standardize values to match the standard unit
UPDATE cleaned_try_bark_diameter
SET stdvalue = origvaluestr::double precision
WHERE origunitstr = 'mm/mm'

UPDATE cleaned_try_bark_diameter
SET stdvalue = origvaluestr::double precision / 100
WHERE origunitstr = '%'

UPDATE cleaned_try_bark_diameter 
SET stdvalue = origvaluestr::double precision
WHERE origunitstr IS NULL

