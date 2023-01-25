CREATE TABLE "Full_Thrift_Store_List" (
	"postal_code"	INTEGER,
	"address"	TEXT,
	"category_name"	TEXT,
	"city"	TEXT,
	"latitude"	REAL,
	"longitude"	REAL,
	"neighborhood"	TEXT,
	"permanently_closed"	TEXT,
	"phone"	TEXT,
	"state"	TEXT,
	"temporarily_closed"	TEXT,
	"title"	TEXT,
	"total_score"	REAL,
	"website"	TEXT
)

CREATE TABLE "master_thrift_store" (
	"Name"	TEXT,
	"ZIP"	INTEGER,
	"Median_Income"	INTEGER,
	"Median_Age"	INTEGER,
	"Median_Male_Age"	INTEGER,
	"Median_Female_Age"	INTEGER
)

--Clean Out any non-Michigan ZIPs: There apparently are none

SELECT * FROM Full_Thrift_Store_List
WHERE postal_code NOT BETWEEN 48001 AND 49971;

--Check for and clean out any permanently closed businesses: 24 businesses found and deleted
SELECT * FROM Full_Thrift_Store_List
WHERE permanently_closed = 'TRUE' OR temporarily_closed = 'TRUE';

DELETE FROM Full_Thrift_Store_List WHERE permanently_closed = 'TRUE'  OR temporarily_closed = 'TRUE';

--Look at list of unique business types
SELECT DISTINCT(category_name) AS 'Unique Categories List'  FROM Full_Thrift_Store_List;

--Check for and clean out any non-thrift stores: removed 1005 businesses
SELECT * FROM Full_Thrift_Store_List
WHERE category_name NOT IN ('Thrift store', 'Charity', 'Second hand store', 'Non-profit organization', 'Donations center', 'Used clothing store', 'Clothes market') OR category_name IS NULL;

DELETE FROM Full_Thrift_Store_List 
WHERE category_name NOT IN ('Thrift store', 'Charity', 'Second hand store', 'Non-profit organization', 'Donations center', 'Used clothing store', 'Clothes market') OR category_name IS NULL;

--Clean data so that all state codes are 'MI'
SELECT COUNT(*) AS 'Count of MI State Code' FROM Full_Thrift_Store_List WHERE state <> 'MI'

UPDATE Full_Thrift_Store_List
SET state = CASE
	WHEN state <> 'MI' THEN 'MI'
END

--Count all businesses by ZIP and join that table to Master List for use in Data_Boy.py
SELECT postal_code,
COUNT(*) AS Business_Count
FROM Full_Thrift_Store_List
GROUP BY 1
ORDER BY 2 DESC;

CREATE TABLE "Business_Count_by_ZIP" (
	"postal_code"	INTEGER,
	"Business_Count"	INTEGER
)

--JOIN business count and ZIP list on ID ZIP
SELECT master_thrift_store.*,  Business_Count_by_ZIP.*
FROM master_thrift_store
JOIN Business_Count_by_ZIP
ON master_thrift_store.ZIP = Business_Count_by_ZIP.postal_code
ORDER BY ZIP;