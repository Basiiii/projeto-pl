IMPORT TABLE estacoes FROM "data/estacoes.csv";
IMPORT TABLE observacoes FROM "data/observacoes.csv";

PRINT TABLE estacoes;
PRINT TABLE observacoes;

SELECT * FROM observacoes;

SELECT Id,Local FROM estacoes;

SELECT * FROM observacoes WHERE Temperatura > 16;

SELECT * FROM estacoes LIMIT 2;

CREATE TABLE ventos_fortes SELECT * FROM observacoes WHERE IntensidadeVentoKM > 10;
PRINT TABLE ventos_fortes;

CREATE TABLE estacoes_obs FROM estacoes JOIN observacoes USING Id;
PRINT TABLE estacoes_obs;

PROCEDURE print_all DO
  PRINT TABLE estacoes;
  PRINT TABLE observacoes;
  PRINT TABLE ventos_fortes;
  PRINT TABLE estacoes_obs;
END

CALL print_all;

EXPORT TABLE estacoes_obs AS "data/estacoes_obs.csv";
EXPORT TABLE ventos_fortes AS "data/ventos_fortes.csv";
