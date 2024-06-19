SELECT family, genus, species, name 
FROM worms_drake 
WHERE 
    statecd IN (1, 9, 10, 12, 13, 17, 18, 21, 23, 24, 25, 26, 28, 33, 34, 36, 37, 39, 42, 44, 45, 47, 50, 51, 54, 55)
    AND origin != 'Nearctic'
GROUP BY family, genus, species, name
ORDER BY family, genus, species, name;

