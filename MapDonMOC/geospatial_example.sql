POINT geo type
 LINESTRING geo type
 POLYGON geo type
 Multi-vertex LineStrings
 Polygon holes - interior rings
 Well Known Text import
 Importer support
 geo objects in INSERT statements
 internal representation: generated physical columns
 geospatial literals
ST_GeomFromText(wkt) support
Determine geo type, import geom to array literals
Array literal serialization
Codegen, hookup to specialized geo functions
 geo function call codegen, specialization
 ST_Distance (POINT, POINT)
 ST_Distance (POINT, LINESTRING)
 ST_Distance (POINT, POLYGON)
 ST_Distance (LINESTRING, POINT)
 ST_Distance (LINESTRING, LINESTRING)
 ST_Distance (LINESTRING, POLYGON)
 ST_Distance (POLYGON, POINT)
 ST_Distance (POLYGON, LINESTRING)
 ST_Distance (POLYGON, POLYGON)
 ST_Contains (POINT, POINT)
 ST_Contains (POINT, LINESTRING)
 ST_Contains (POINT, POLYGON)
 ST_Contains (LINESTRING, POINT)
 ST_Contains (POLYGON, POINT)
 ST_Contains (POLYGON, LINESTRING)
 ST_Contains (POLYGON, POLYGON)
 GPU: Broken buffer allocation for 2+ physical columns - an issue for POLYGONs
 Support geo column select, projection, e.g. SELECT point_column FROM geo_table;
 Rebase

 > cat geo.csv
"pz", "p", "l"
"POINT(0 0)", "POINT(0 0)", "LINESTRING( 0 0,  0  0)"
"POINT(0 0)", "POINT(1 1)", "LINESTRING( 2 0,  2  2)"
"POINT(0 0)", "POINT(2 2)", "LINESTRING( 4 0,  4  4)"
"POINT(0 0)", "POINT(3 3)", "LINESTRING( 6 0,  6  6)"
"POINT(0 0)", "POINT(4 4)", "LINESTRING( 8 0,  8  8)"
"POINT(0 0)", "POINT(5 5)", "LINESTRING(10 0, 10 10)"
"POINT(0 0)", "POINT(6 6)", "LINESTRING(12 0, 12 12)"
"POINT(0 0)", "POINT(7 7)", "LINESTRING(14 0, 14 14)"
"POINT(0 0)", "POINT(8 8)", "LINESTRING(16 0, 16 16)"
"POINT(0 0)", "POINT(9 9)", "LINESTRING(18 0, 18 18)"

> cat geo1.csv
"pz", "p", "l"
POINT(0 0); POINT(10 10); LINESTRING(20 0, 20 20)
POINT(0 0); POINT(11 11); LINESTRING(22 0, 22 22)
POINT(0 0); POINT(12 12); LINESTRING(24 0, 24 24)
POINT(0 0); POINT(13 13); LINESTRING(26 0, 26 26)
POINT(0 0); POINT(14 14); LINESTRING(28 0, 28 28)
POINT(0 0); POINT(15 15); LINESTRING(30 0, 30 30)
POINT(0 0); POINT(16 16); LINESTRING(32 0, 32 32)
POINT(0 0); POINT(17 17); LINESTRING(34 0, 34 34)
POINT(0 0); POINT(18 18); LINESTRING(36 0, 36 36)
POINT(0 0); POINT(19 19); LINESTRING(38 0, 38 38)

> ./bin/mapdql -p HyperInteractive --port 11100
User mapd connected to database mapd
mapdql> drop table geo;
mapdql> CREATE TABLE geo (pz POINT, p POINT, l LINESTRING) WITH (fragment_size=2);
mapdql> \d geo
CREATE TABLE geo (
pz POINT,
p POINT,
l LINESTRING)
WITH (FRAGMENT_SIZE = 2)
mapdql> copy geo from '../geo.csv';
Result
Loaded: 10 recs, Rejected: 0 recs in 1.456000 secs
mapdql> copy geo from '../geo1.csv' with (delimiter=';');
Result
Loaded: 10 recs, Rejected: 0 recs in 0.218000 secs
mapdql> insert into geo values('POINT(0 0)', 'POINT(20 20)', 'LINESTRING(40 0, 40 40)');
mapdql> select count(*) from geo;
EXPR$0
21
mapdql> select count(*) from geo where ST_Distance(pz,p) < 100.0;
EXPR$0
21
mapdql> select count(*) from geo where ST_Distance(pz,p) < 10.0;
EXPR$0
8
mapdql> select count(*) from geo where ST_Distance(pz,p) < 5.0;
EXPR$0
4
mapdql> select count(*) from geo where ST_Contains(pz,p);
EXPR$0
1
mapdql> select count(*) from geo where ST_Contains(p,p);
EXPR$0
21




mapdql> SELECT ST_Distance('POINT(0 0)', 'POINT(1 1)') from geo limit 1;
EXPR$0
1.414214
mapdql> SELECT ST_Distance('LINESTRING(-1 0, 0 1)', 'POINT(0 0)') from geo limit 1;
EXPR$0
0.707107



mapdql> create table t1 (id INT, resultcol INT, pointcol POINT);
mapdql> insert into t1 values(0, 100, 'POINT(0 0)');
mapdql> insert into t1 values(1, 101, 'POINT(1 1)');
mapdql> insert into t1 values(2, 102, 'POINT(2 2)');
mapdql> insert into t1 values(3, 103, 'POINT(3 3)');
mapdql> insert into t1 values(4, 104, 'POINT(4 4)');
mapdql> insert into t1 values(5, 105, 'POINT(5 5)');
mapdql> create table t2 (id INT);
mapdql> insert into t2 values(-1);
mapdql> insert into t2 values(1);
mapdql> insert into t2 values(3);
mapdql> insert into t2 values(5);
mapdql>
mapdql> SELECT t1.resultcol FROM t1 JOIN t2 ON t1.id = t2.id;
resultcol
101
103
105
mapdql> SELECT t1.resultcol FROM t1 JOIN t2 ON t1.id = t2.id WHERE ST_DISTANCE(t1.pointcol, 'POINT(0 0)') > 2.0;
resultcol
103
105
mapdql> SELECT t1.resultcol FROM t1 JOIN t2 ON t1.id = t2.id WHERE ST_CONTAINS('POLYGON((4 0, 4 4, 0 4, 0 0, 4 0))', t1.pointcol);
resultcol
101
103
mapdql> SELECT t1.resultcol FROM t1 JOIN t2 ON t1.id = t2.id WHERE ST_CONTAINS('POLYGON((4 0, 4 4, 0 4, 0 0, 4 0), (2 0, 2 2, 0 2, 0 0, 2 0))', t1.pointcol);
resultcol
103
mapdql> SELECT t1.resultcol FROM t1 JOIN t2 ON t1.id = t2.id WHERE ST_CONTAINS('POLYGON((4 0, 4 4, 0 4, 0 0, 4 0), (2 0, 2 2, 0 2, 0 0, 2 0))', t1.pointcol) OR ST_DISTANCE(t1.pointcol, 'POINT(6 6)') < 1.5;
resultcol
103
105
mapdql>
mapdql>
mapdql> create table t3 (pointcol POINT);
mapdql> insert into t3 values('POINT(2.5 2.5)');
mapdql> insert into t3 values('POINT(6 6)');
mapdql>
mapdql> SELECT t1.resultcol FROM t1 JOIN t3 ON ST_DISTANCE(t1.pointcol, t3.pointcol) < 1.45;
resultcol
102
103
105
mapdql> 
