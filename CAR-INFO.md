# Organização do dataset CAR

- [*Ipam Brasil*](/media/gabriel/Gabriel/Datasets/CAR/IPAM)

    O Ipam tem coletado anualmente o CAR para todas as unidades federativas desde 2017, e para o estado de Mato Grosso entre 2009 e 2014.

    | Nome                    |Data      |Observação                                 |
    |-------------------------|----------|-------------------------------------------|
    |IPAM Brasil 2020         |2020-02-18|Faltam algumas cidades (logger file)   |
    |IPAM Brasil Agosto   2019|2019-08-24|Disponíveis: AC, AM, AP, DF, MT, PA, RO, RR|
    |IPAM Brasil Maio     2019|2019-05-24|Pendente                                   |
    |IPAM Brasil Novembro 2018|2018-10-24|Falta SE, SP, TO                           |
    |IPAM Brasil Setembro 2019|2018-09-06|Pendente                                   |
    |IPAM BRASIL 2017         |2017-01-01|Pendente. Não disponívela data do SICAR    |
    |IPAM BRASIL 2016         |2016-01-01|Pendente. Não disponível a data do SICAR    |
    |IPAM MT 2009-2014        |2014-01-01|Arquivos Ok. Apenas MT                     |

--------------------------------------------------------------------------------------
- *Serviço Florestal Brasileiro (SFB-SQL)*

    Banco de Janeiro de 2017 com a data de migração dos registros para o SICAR.

--------------------------------------------------------------------------------------
- *IMAFLORA*

    Base de Dezembro de 2019, com os CARs para esse ano.

-------------------------------------------------------------------------------------
Em resumo, os datasets podem ser organizados de acordo com o ano e a disponibilidade para cada UF.


|Data     |MT                            |PA                            |Demais UFs        |
|---------|------------------------------|------------------------------|------------------|
|Pre 2014 |IPAM MT (2009-14)             |Base PNAS (2008-13) e SFB-SQL |SFB-SQL (min 2014)|
|2014     |IPAM MT (2009-14)             |SQL-SFB                       |SQL-SFB           |
|2015     |SQL-SFB                       |SQL-SFB                       |SQL-SFB           |
|2016     |SQL-SFB                       |SQL-SFB                       |SQL-SFB           |
|2017     |IPAM Brasil (2017)            |IPAM_Brasil (2017)            |IPAM_Brasil (2017)|
|2018     |IPAM Brasil (2018)            |IPAM_Brasil (2018)            |IPAM_Brasil (2018)|
|2019     |IPAM Brasil (2019)            |IPAM_Brasil (2019)            |IPAM_Brasil (2019)|
|2020     |IPAM Brasil (2020)            |IPAM_Brasil (2020)            |IPAM_Brasil (2020)|

-------------------------------------------------------------------------------------------
## Datasets Adicionais

Adicionalmente, tem-se bases antigas com o Car (no banco identificado como ProtCAR) em função das coordenads. Com isso, é possível obter o município a partir das coordenadas:

- [Base antiga MT (2005-2012)](/media/gabriel/Gabriel/Datasets/CAR/Bases_Antigas/datas_imoveis201703.sqlite)
- [Base antiga PA (2009-2013)](/media/gabriel/Gabriel/Datasets/CAR/Bases_Antigas/2014_02_21_PA_Fin_CAR_INTL_CARINTL_Limpo_FIN_mun_MF_DesmP2012.xlsx)

O objetivo, é reunir as informações de todos os datasets, de forma a obter a área em função do ano. Ou seja, um banco com a seguinte estrutura:

|CAR|ORIGEM_CAR|CODIGO_MUNICIPIO|PRIMEIRA_DATA|ORIGEM_PRIM_DATA|AREA_2009|AREA_2010|... |AREA_2020|
|---|----------|----------------|-------------|----------------|---------|---------|--- |---------|
|num|COORD/DATA|num             |Date         |FILE/DATA       |Date     | Date    |Date|Date     |