WITH association_counts
AS (
	WITH county_trees
  AS (
    SELECT plt_cn, invyr, tree, tree.spcd, ref_species.association
    FROM tree 
    LEFT JOIN ref_species
    ON tree.spcd = ref_species.spcd
    WHERE 

      tree.invyr > 1979 AND tree.invyr < 1995 AND										-- at T1
      -- tree.invyr > 2017 AND tree.invyr < 2023 AND								-- at T2

      tree.statecd = 44 AND  
      tree.unitcd = 1 AND
      tree.countycd = 7

    ORDER BY association ASC
  )
  SELECT association, count(association)
  FROM county_trees
  GROUP BY association
)
SELECT  
  sum(count) AS total_trees,
  round((SELECT count FROM association_counts WHERE association = 'AM')/sum(count) *100, 0) AS percent_am,
  round((SELECT count FROM association_counts WHERE association = 'EM')/sum(count) *100, 0) AS percent_em,
  round((SELECT count FROM association_counts WHERE association = 'AM') / (SELECT count FROM association_counts WHERE association = 'EM')::decimal, 2) AS ratio_of_am_to_em
FROM association_counts;

