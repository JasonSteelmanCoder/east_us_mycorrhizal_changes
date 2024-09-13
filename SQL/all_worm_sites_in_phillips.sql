SELECT worm_species_occurrence.study_name, worm_species_occurrence.site_name 
FROM worm_species_occurrence
LEFT JOIN sites
ON worm_species_occurrence.study_name = sites.study_name AND worm_species_occurrence.site_name = sites.site_name
WHERE country = 'United States'
GROUP BY worm_species_occurrence.study_name, worm_species_occurrence.site_name
ORDER BY worm_species_occurrence.study_name, worm_species_occurrence.site_name;