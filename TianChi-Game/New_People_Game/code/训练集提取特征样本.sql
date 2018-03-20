/*
	在MySql数据库上进行数据处理  limit 10
	用户在商品全集上的移动端行为数据：tianchi_fresh_comp_train_user D
	商品子集：tianchi_fresh_comp_train_item P
	1)题目要求需要预测用户在19号是否购买了P表中的商品，
	2)由16,17号的用户交互数据来预测18号用户的购买情况，来构建预测模型。使用决策树模型
	3)由17,18号的用户交互数据来预测19号用户的购买情况。
	注意：
		对于我们提取出来的训练集数据里，在18号不会购买的项的数据量比18号购买的项的数据量多得多，
		也就是正负样本比例相差得太大！这对于模型学习是灾难性的，学习出的模型完全不能用。
		所以，我们需要选出训练集里所有在18号购买了的，再选出同等数量或者相差不多的数量的负样本作为新的训练集，
		利用新训练集去学习决策树模型，这样才能起效果
	4)特征情况的选择
*/
--根据P中的数据来过滤D表中的数据
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

--统计16、17号用户交互情况，并且标识出用户是否在18号进行了购买行为
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

--统计出17、18号用户交互行为
CREATE TABLE day1718_19_detail AS
select
	t.*,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=1 THEN 1 ELSE 0 END AS Is_2day_liulan,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=2 THEN 1 ELSE 0 END AS Is_2day_shoucang,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=3 THEN 1 ELSE 0 END AS Is_2day_jiagou,
	case when (substr(time,1,10)='2014-12-17' OR substr(time,1,10)='2014-12-18') AND behavior_type=4 THEN 1 ELSE 0 END AS Is_2day_buy
from user_item_1 t
;

--统计出2张表的相应日期各种交互行为的总数量
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





--最后还需要抽出所有正样本，以及同等数量的负样本，组成最终的训练集表train_datatable
--先选出正例
CREATE TABLE positive AS select * from day1617_18_train_data t where DAY18_buy>=1;
--看一看正例有多少个
SELECT COUNT(1) FROM positive;
--假设正例有5000个，那么我们就随机抽取负例10000个
CREATE TABLE negative AS SELECT * FROM day1617_18_train_data WHERE DAY18_buy=0 LIMIT 300;
--最后再把两张表合在一起
CREATE TABLE train_datatable AS
SELECT * FROM positive
UNION ALL
SELECT * FROM negative;


--导出训练集数据
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