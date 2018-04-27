/*
	��MySql���ݿ��Ͻ������ݴ���  limit 10
	�û�����Ʒȫ���ϵ��ƶ�����Ϊ���ݣ�tianchi_fresh_comp_train_user D
	��Ʒ�Ӽ���tianchi_fresh_comp_train_item P
	1)��ĿҪ����ҪԤ���û���19���Ƿ�����P���е���Ʒ��
	2)��16,17�ŵ��û�����������Ԥ��18���û��Ĺ��������������Ԥ��ģ�͡�ʹ�þ�����ģ��
	3)��17,18�ŵ��û�����������Ԥ��19���û��Ĺ��������
	ע�⣺
		����������ȡ������ѵ�����������18�Ų��Ṻ��������������18�Ź���������������ö࣬
		Ҳ��������������������̫�������ģ��ѧϰ�������Եģ�ѧϰ����ģ����ȫ�����á�
		���ԣ�������Ҫѡ��ѵ������������18�Ź����˵ģ���ѡ��ͬ��������������������ĸ�������Ϊ�µ�ѵ������
		������ѵ����ȥѧϰ������ģ�ͣ�����������Ч��
	4)���������ѡ��
*/
--����P�е�����������D���е�����
create table user_item_1
(
	user_id					INTEGER,
	item_id					VARCHAR(50),
	behavior_type 	INTEGER,
	user_geohash		VARCHAR(50),
	item_category		VARCHAR(50),
	time						VARCHAR(50),
	item_geohash		VARCHAR(50)
);

insert into user_item_1
select	a.user_id,a.item_id,a.behavior_type,a.user_geohash,a.item_category,a.time
from tianchi_fresh_comp_train_item b
left join
	tianchi_fresh_comp_train_user a
on b.item_id=a.item_id and b.item_category=a.item_category
where a.user_id is not NULL
;

--ͳ��16��17���û�������������ұ�ʶ���û��Ƿ���18�Ž����˹�����Ϊ
CREATE TABLE day1617_18_detail AS
select
	t.*,
	case when (substr(time,1,10)='2014-12-16' OR substr(time,1,10)='2014-12-17') AND behavior_type=1 THEN 1 ELSE 0 END AS Is_2day_liulan,
	case when (substr(time,1,10)='2014-12-16' OR substr(time,1,10)='2014-12-17') AND behavior_type=2 THEN 1 ELSE 0 END AS Is_2day_shoucang,
	case when (substr(time,1,10)='2014-12-16' OR substr(time,1,10)='2014-12-17') AND behavior_type=3 THEN 1 ELSE 0 END AS Is_2day_jiagou,
	case when (substr(time,1,10)='2014-12-16' OR substr(time,1,10)='2014-12-17') AND behavior_type=4 THEN 1 ELSE 0 END AS Is_2day_buy,
	case when substr(time,1,10)='2014-12-18' and behavior_type=4 then 1 else 0 end as Is_buy
from user_item_1 t
;

--ͳ�Ƴ�17��18���û�������Ϊ
CREATE TABLE day1718_19_detail AS
select
	t.*,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=1 THEN 1 ELSE 0 END AS Is_2day_liulan,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=2 THEN 1 ELSE 0 END AS Is_2day_shoucang,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=3 THEN 1 ELSE 0 END AS Is_2day_jiagou,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=4 THEN 1 ELSE 0 END AS Is_2day_buy
from user_item_1 t
;

--ͳ�Ƴ�2�ű����Ӧ���ڸ��ֽ�����Ϊ��������
CREATE TABLE day1617_18_train_data AS
SELECT *
FROM
(
	SELECT
		user_id,item_id,
		SUM(CASE WHEN Is_2day_liulan=1 THEN 1 ELSE 0 END) AS 2day_view,
		SUM(CASE WHEN Is_2day_shoucang=1 THEN 1 ELSE 0 END) AS 2day_favor,
		SUM(CASE WHEN Is_2day_jiagou=1 THEN 1 ELSE 0 END) AS 2day_tocar,
		SUM(CASE WHEN Is_2day_buy=1 THEN 1 ELSE 0 END) AS 2day_buy,
		SUM(CASE WHEN Is_buy=1 THEN 1 ELSE 0 END) AS DAY18_buy
FROM day1617_18_detail
GROUP BY user_id,item_id
) t
WHERE 2day_view>0 OR 2day_favor>0 OR 2day_tocar>0 OR 2day_buy>0
;

CREATE TABLE day1718_19_predict_data AS
SELECT *
FROM
(
	SELECT
		user_id,item_id,
		SUM(CASE WHEN Is_2day_liulan=1 THEN 1 ELSE 0 END) AS 2day_view,
		SUM(CASE WHEN Is_2day_shoucang=1 THEN 1 ELSE 0 END) AS 2day_favor,
		SUM(CASE WHEN Is_2day_jiagou=1 THEN 1 ELSE 0 END) AS 2day_tocar,
		SUM(CASE WHEN Is_2day_buy=1 THEN 1 ELSE 0 END) AS 2day_buy
FROM day1718_19_detail
GROUP BY user_id,item_id
) t
WHERE 2day_view>0 OR 2day_favor>0 OR 2day_tocar>0 OR 2day_buy>0
;





--�����Ҫ����������������Լ�ͬ�������ĸ�������������յ�ѵ������train_datatable
--��ѡ������
CREATE TABLE positive AS select * from day1617_18_train_data t where DAY18_buy>=1;
--��һ�������ж��ٸ�
SELECT COUNT(1) FROM positive;
--����������5000������ô���Ǿ������ȡ����10000��
CREATE TABLE negative AS SELECT * FROM day1617_18_train_data WHERE DAY18_buy=0 LIMIT 300;
--����ٰ����ű����һ��
CREATE TABLE train_datatable AS
SELECT * FROM positive
UNION ALL
SELECT * FROM negative;


--����ѵ��������
select * from (
SELECT 'user_id','item_id','2day_view','2day_favor','2day_tocar','2day_buy','DAY18_buy'
union
SELECT user_id,item_id,2day_view,2day_favor,2day_tocar,2day_buy,DAY18_buy FROM train_datatable
) t
INTO OUTFILE 'train_datatable.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n';


select * from (
SELECT 'user_id','item_id','2day_view','2day_favor','2day_tocar','2day_buy'
union
SELECT user_id,item_id,2day_view,2day_favor,2day_tocar,2day_buy FROM day1718_19_predict_data
) t
INTO OUTFILE 'day1718_19_predict_data.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n';