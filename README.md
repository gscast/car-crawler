# CAR-Dataset

O CAR é um registro público eletrônico de âmbito nacional, obrigatório para todos os imóveis rurais, com a finalidade de integrar as informações ambientais das propriedades e posses rurais referentes à situação das Áreas de Preservação Permanente - APP, das áreas de Reserva Legal, das florestas e dos remanescentes de vegetação nativa, das Áreas de Uso Restrito e das áreas consolidadas, compondo base de dados para controle, monitoramento, planejamento ambiental e econômico e combate ao desmatamento.

-------------------------------------------------------------------------------------------------------
# Uso
A fim de reunir e integrar dados sobre o CAR, foram elaboradas ferramentas a fim de utilizar os shapefiles, disponíveis no no SICAR:

    - crawler/bot.py: crawler para baixar os shapefiles de todas as cidades de uma UF
    - src/collect_shp.r: gera um arquivo .dbf integrando as informações contidas nos shapefiles.
    - src/csv2shp.r: converte a tabela CSV em um SHP com mesma estrutura do shapefile.
    - src/get_oldest_date.r: retorna o CAR em função da primeira data de registro disponível.
    - src/uncompress_dbf.py: automatiza a extração dos arquivos shapefile.