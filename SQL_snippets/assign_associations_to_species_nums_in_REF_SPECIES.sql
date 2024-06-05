-- Create a ref_species column
ALTER TABLE ref_species
ADD association text;

-- Assign AM/EM based on tedersoo data
UPDATE ref_species
SET association = 'AM'
WHERE ref_species.genus IN (
  SELECT mycorrhiza_brundrett_tedersoo.genus FROM mycorrhiza_brundrett_tedersoo WHERE mycorrhiza_brundrett_tedersoo.mycorrhiza = 'AM'
);

UPDATE ref_species
SET association = 'EM'
WHERE ref_species.genus IN (
  SELECT mycorrhiza_brundrett_tedersoo.genus FROM mycorrhiza_brundrett_tedersoo WHERE mycorrhiza_brundrett_tedersoo.mycorrhiza = 'EM'
);

UPDATE ref_species
SET association = 'Ericoid'
WHERE ref_species.genus IN (
  SELECT mycorrhiza_brundrett_tedersoo.genus FROM mycorrhiza_brundrett_tedersoo WHERE mycorrhiza_brundrett_tedersoo.mycorrhiza = 'Ericoid'
);

UPDATE ref_species
SET association = 'EM-AM'
WHERE ref_species.genus IN (
  SELECT mycorrhiza_brundrett_tedersoo.genus FROM mycorrhiza_brundrett_tedersoo WHERE mycorrhiza_brundrett_tedersoo.mycorrhiza = 'EM-AM'
);

-- Try to assign AM/EM to "Unknown" associations based on data from "Rediscovered treasures" paper
UPDATE ref_species
SET association = 'AM'
WHERE ref_species.association IS NULL 
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_akhmetzhanova WHERE association = 'AM');

UPDATE ref_species
SET association = 'EM'
WHERE ref_species.association IS NULL
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_akhmetzhanova WHERE association = 'Ectomycorrhiza');

UPDATE ref_species
SET association = 'Ericoid'
WHERE ref_species.association IS NULL 
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_akhmetzhanova WHERE association = 'Ericoid');

-- Assign AM/EM to unknown associations based on data from mkt's table
UPDATE ref_species
SET association = 'AM'
WHERE ref_species.association IS NULL 
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_mkt WHERE association = 'AM');

UPDATE ref_species
SET association = 'ECM'
WHERE ref_species.association IS NULL
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_mkt WHERE association = 'ECM');

UPDATE ref_species
SET association = 'Ericoid'
WHERE ref_species.association IS NULL 
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_mkt WHERE association = 'Ericoid');
 
UPDATE ref_species
SET association = 'AM-ECM'
WHERE ref_species.association IS NULL 
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_mkt WHERE association = 'AM-ECM');

UPDATE ref_species
SET association = 'non-mycorrhizal'
WHERE ref_species.association IS NULL 
AND ref_species.genus IN (SELECT genus FROM mycorrhiza_mkt WHERE association = 'non-mycorrhizal');

 