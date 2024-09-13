-- find average birk thickness values and concatenate sources
SELECT 
	*,
  ROUND((COALESCE(hammond, 0) + COALESCE(babl, 0) + COALESCE(schafer, 0) + COALESCE(stan, 0) + COALESCE(hengst, 0) + COALESCE(jackson, 0) + COALESCE(pellegrini, 0) + COALESCE(russell, 0) + COALESCE(graves, 0) + COALESCE(try_34741, 0) + COALESCE(stevens, 0) + COALESCE(shearman, 0) + COALESCE(scavotto, 0))::decimal 
  / NULLIF((
  	CASE WHEN hammond IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN babl IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN schafer IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN stan IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN hengst IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN jackson IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN pellegrini IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN russell IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN graves IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN try_34741 IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN stevens IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN shearman IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN scavotto IS NOT NULL THEN 1 ELSE 0 END
  ), 0), 4) AS average_bt,
  
    'Average of: ' ||
    CASE WHEN hammond IS NOT NULL THEN 'Hammond ' || hammond || ' ' ELSE '' END ||
    CASE WHEN babl IS NOT NULL THEN 'Babl ' || babl || ' ' ELSE '' END ||
    CASE WHEN schafer IS NOT NULL THEN 'Schafer ' || schafer || ' ' ELSE '' END ||
    CASE WHEN stan IS NOT NULL THEN 'Stan ' || stan || ' ' ELSE '' END ||
    CASE WHEN hengst IS NOT NULL THEN 'Hengst ' || hengst || ' '  ELSE '' END ||
    CASE WHEN jackson IS NOT NULL THEN 'Jackson ' || jackson || ' '  ELSE '' END ||
    CASE WHEN pellegrini IS NOT NULL THEN 'Pellegrini ' || pellegrini || ' '  ELSE '' END ||
    CASE WHEN russell IS NOT NULL THEN 'Russell ' || russell || ' '  ELSE '' END ||
    CASE WHEN graves IS NOT NULL THEN 'Graves ' || graves || ' '  ELSE '' END ||
    CASE WHEN try_34741 IS NOT NULL THEN 'Try_34741 ' || try_34741 || ' '  ELSE '' END ||
    CASE WHEN stevens IS NOT NULL THEN 'Stevens ' || stevens || ' '  ELSE '' END ||
    CASE WHEN shearman IS NOT NULL THEN 'Shearman ' || shearman || ' '  ELSE '' END ||
    CASE WHEN scavotto IS NOT NULL THEN 'Scavotto ' || scavotto || ' '  ELSE '' END
    AS sources
  
FROM duplicate_sources_bt


-- do the same for C:N
SELECT 
	*,
  ROUND((COALESCE(try_34741, 0) + COALESCE(zhang, 0) + COALESCE(zimmer, 0) + COALESCE(hendrix, 0) + COALESCE(poulette, 0))::decimal
  / NULLIF(
  	CASE WHEN try_34741 IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN zhang IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN zimmer IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN hendrix IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN poulette IS NOT NULL THEN 1 ELSE 0 END
  , 0), 4) AS average_cn,
	
  'Average of: ' ||
  CASE WHEN try_34741 IS NOT NULL THEN 'Try_34741 ' || try_34741 || ', ' ELSE '' END ||
  CASE WHEN zhang IS NOT NULL THEN 'Zhang ' || zhang || ', ' ELSE '' END ||
  CASE WHEN zimmer IS NOT NULL THEN 'Zimmer ' || zimmer || ', ' ELSE '' END ||
  CASE WHEN hendrix IS NOT NULL THEN 'Hendrix ' || hendrix || ', ' ELSE '' END ||
  CASE WHEN poulette IS NOT NULL THEN 'Poulette ' || poulette || ', ' ELSE '' END
  AS sources
  
FROM duplicate_sources_cn


-- same for k
SELECT 
	*, 
  ROUND((try_34741 + zhang)::decimal / 2, 4) AS mean_k,
  'Average of: TRY_34741 ' || try_34741 || ', Zhang ' || zhang AS sources
FROM duplicate_sources_k
