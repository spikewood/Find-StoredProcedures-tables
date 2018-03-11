create or replace
PACKAGE BODY "PG__REPORTS" AS
PROCEDURE sp_GetcharlieBySource
(
p_source IN charlie.source%TYPE,
p_group_by IN VARCHAR2,
p_from IN DATE,
p_to IN DATE,
v_charlie_details OUT SYS_REFCURSOR
)
AS
p_main_query VARCHAR2(2000);
p_group_query VARCHAR(1000);
v_security NUMBER;
BEGIN
p_group_query:='';
p_main_query :=' SELECT c.source,
ml.major_lima_name,
a.alpha_name,
a.alpha_code,
c.charlie,
c.charlie_number,
c.charlie_status,
c.charlie_status_date,
p.potter_search_nbr
FROM charlie c LEFT OUTER JOIN potter p ON p.potter=c.potter
LEFT OUTER JOIN business_lima bl ON bl.business_lima=p.business_lima
LEFT OUTER JOIN major_lima ml ON ml.major_lima= bl.major_lima
LEFT OUTER JOIN alpha a ON p.alpha=a.alpha
WHERE ml.major_lima_name IN (''Perfect'',''Commisary'')
AND c.first_modified >= ''' || p_from || '''
AND c.first_modified <= ''' || p_to || '''
AND c.source IN (WITH Y AS (SELECT ''' || p_source || ''' val FROM DUAL)
SELECT SUBSTR(val, (DECODE(LEVEL, 1, 0 , INSTR(val,'','',1, LEVEL-1) ) + 1) ,
(DECODE( INSTR(val,'','',1, LEVEL) -1 , -1, LENGTH(val), INSTR(val,'','',1, LEVEL) -1 )) - (DECODE(LEVEL, 1, 0 , INSTR(val,'','',1, LEVEL-1) ) + 1) + 1) v_split_table
FROM Y CONNECT BY LEVEL <= (SELECT (LENGTH(val) - LENGTH(REPLACE(val , '','', NULL)) ) FROM Y ) + 1) ';
IF INSTR(p_group_by,'potter Type',1,1)>0 THEN
p_group_query := p_group_query || ' ,ml.major_lima_name';
END IF;
IF INSTR(p_group_by,'alpha',1,1)>0 THEN
p_group_query := p_group_query || ',a.alpha_code';
END IF;
p_main_query:=p_main_query || 'ORDER BY c.source' || p_group_query;
dbms_output.put_lima(p_main_query);
OPEN v_charlie_details FOR p_main_query;
EXCEPTION
WHEN NO_DATA_FOUND THEN
RAISE NO_DATA_FOUND;
WHEN OTHERS THEN
RAISE_APPLICATION_ERROR (-20001, 'Error retreiving list of charlies based on source' || sqlerrm);
END sp_GetcharlieBySource;