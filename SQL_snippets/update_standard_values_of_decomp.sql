-- set a standard unit of per year
UPDATE cleaned_try_decomp
SET unitname = 'yr-1'

-- copy over the values that are already measured per year
UPDATE cleaned_try_decomp
SET stdvalue = origvaluestr::double precision
WHERE 
	origunitstr = 'yr-1' 
	OR origunitstr = '1/y'

-- copy Cornelissen values into the stdvalue column of the cleaned_try_decomp table
-- note that stdvalue will be based on all of the measurements for a given species made by Cornelissen.
UPDATE cleaned_try_decomp
SET stdvalue = k_values_cornelissen.k, comment = 'stdvalue is calculated based on all measurements of this species taken by Cornelissen and reported in g/g'
FROM k_values_cornelissen
WHERE 
	origunitstr = 'g/g'
    AND lastname = 'Cornelissen'
	AND LOWER(TRIM(BOTH ' ' FROM cleaned_try_decomp.speciesname)) = LOWER(TRIM(BOTH ' ' FROM k_values_cornelissen.species))


-- Copy Quested values into the stdvalue column of the cleaned_try_decomp table
-- note that stdvalue will be based on all of the measurements for a given species made by Quested.
UPDATE cleaned_try_decomp
SET stdvalue = k_values_quested.k, comment = 'stdvalue is calculated based on all measurements of this species taken by Quested and reported in g/g'
FROM k_values_quested
WHERE 
	origunitstr = 'g/g'
    AND reference LIKE 'Quested, H. M%'
	AND LOWER(TRIM(BOTH ' ' FROM cleaned_try_decomp.speciesname)) = LOWER(TRIM(BOTH ' ' FROM k_values_quested.species))

-- Copy Laughlan values into stdvalue column of the cleaned_try_decomp table
UPDATE cleaned_try_decomp
SET stdvalue = laughlan_relevant_trees.k_in_per_year
FROM laughlan_relevant_trees
WHERE cleaned_try_decomp.observationid = laughlan_relevant_trees.observationid
