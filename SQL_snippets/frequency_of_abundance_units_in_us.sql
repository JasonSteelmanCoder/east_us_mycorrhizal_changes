SELECT abundance_unit, count(abundance_unit) AS frequency 
FROM worm_species_occurrence 
LEFT JOIN sites
ON worm_species_occurrence.study_name = sites.study_name AND worm_species_occurrence.site_name = sites.site_name
WHERE country = 'United States'
GROUP BY abundance_unit 
ORDER BY frequency;