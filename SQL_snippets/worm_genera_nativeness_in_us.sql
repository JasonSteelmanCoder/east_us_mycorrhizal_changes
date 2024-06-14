-- Note that some genera are listed both as non-native, and as NA

SELECT family, genus, native
FROM worm_species_occurrence
JOIN sites
ON worm_species_occurrence.study_name = sites.study_name AND worm_species_occurrence.site_name = sites.site_name
WHERE country = 'United States'
GROUP BY family, genus, native
ORDER BY native, family;