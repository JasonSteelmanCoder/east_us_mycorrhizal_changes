
-- Find species without a value under 'native'
SELECT family, genus, speciesbinomial, worm_sp_occur_phillips.native
FROM phillips_sites_fips
LEFT JOIN worm_sp_occur_phillips 
ON phillips_sites_fips.site_name = worm_sp_occur_phillips.site_name
WHERE worm_sp_occur_phillips.native != 'Non-native' AND worm_sp_occur_phillips.native != 'Native' AND worm_sp_occur_phillips.speciesbinomial != 'NA' 
GROUP BY family, genus, speciesbinomial, worm_sp_occur_phillips.native
ORDER BY family, genus;
 

-- Find species listed as nearctic, in order to check if they are specifically from the East US
SELECT family, genus, species, worms_drake.name, 'true' AS native_to_east_us 
FROM worms_drake 
WHERE worms_drake.origin = 'Nearctic'
GROUP BY family, genus, species, worms_drake.name;


