-- This script replaces some NA values in the phillips data's 'native' column with values provided by Mac Callaham.

    -- make a column in phillips for Mac's data
    ALTER TABLE worm_sp_occur_phillips
    ADD native_mac text

    -- fill the column in with Mac's data
    UPDATE worm_sp_occur_phillips
    SET native_mac = phillips_nativeness.native_to_easternus
    FROM phillips_nativeness
    WHERE LOWER(TRIM(BOTH ' ' FROM worm_sp_occur_phillips.speciesbinomial)) = LOWER(TRIM(BOTH ' ' FROM phillips_nativeness.speciesbinomial))
  
    -- update parts of the 'native' column in phillips, based on Mac's data
	UPDATE worm_sp_occur_phillips
    SET native = CASE 
        WHEN native = 'NA' AND native_mac = 'nonnative' THEN 'Non-native'
        WHEN native = 'NA' AND native_mac = 'native' THEN 'Native'
        ELSE native
    END
    
    -- discard the column with Mac's data
    ALTER TABLE worm_sp_occur_phillips
    DROP COLUMN native_mac