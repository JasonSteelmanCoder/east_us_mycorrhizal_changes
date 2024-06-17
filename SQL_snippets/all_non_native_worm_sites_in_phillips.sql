-- This query selects all of the locations (latitude and longitude) of sites with non-native worm species in the Phillips data.

SELECT latitude_decimal_degrees, longitude_decimal_degrees
FROM worm_species_occurrence 
JOIN sites
ON worm_species_occurrence.study_name = sites.study_name AND worm_species_occurrence.site_name = sites.site_name
WHERE country = 'United States'
AND native = 'Non-native';