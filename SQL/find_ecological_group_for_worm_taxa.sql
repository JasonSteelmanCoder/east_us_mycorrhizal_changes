SELECT worm_sp_occur_phillips.family, worm_sp_occur_phillips.genus, worm_sp_occur_phillips.ecological_group 
FROM ecological_groups
LEFT JOIN worm_sp_occur_phillips
ON ecological_groups.family = worm_sp_occur_phillips.family AND ecological_groups.genus = worm_sp_occur_phillips.genus
GROUP BY worm_sp_occur_phillips.family, worm_sp_occur_phillips.genus, worm_sp_occur_phillips.ecological_group

UNION
  
SELECT worm_sp_occur_phillips.family, worm_sp_occur_phillips.genus, worm_sp_occur_phillips.ecological_group 
FROM ecological_groups
LEFT JOIN worm_sp_occur_phillips
ON ecological_groups.name = worm_sp_occur_phillips.speciesbinomial
GROUP BY worm_sp_occur_phillips.family, worm_sp_occur_phillips.genus, worm_sp_occur_phillips.ecological_group

ORDER BY ecological_group;