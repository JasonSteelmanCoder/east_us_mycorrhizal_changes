WITH county_trees
AS (
  SELECT plt_cn, invyr, tree, tree.spcd, ref_species.association
  FROM tree 
  LEFT JOIN ref_species
  ON tree.spcd = ref_species.spcd
  WHERE 
    tree.statecd = 44 AND
    tree.invyr > 1979 AND tree.invyr < 1995 AND
    tree.unitcd = 1 AND
    tree.countycd = 5
  ORDER BY association ASC
)
SELECT association, count(association)
FROM county_trees
GROUP BY association;
