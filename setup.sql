CREATE DATABASE med_data;

\connect med_data;

CREATE TABLE pima(
pregnancies SMALLINT,
glucose NUMERIC,
diaBP NUMERIC,
skinthickness NUMERIC,
insulin NUMERIC,
BMI NUMERIC,
dpf NUMERIC,
age SMALLINT,
outcome BOOLEAN, 
diabetes BOOLEAN GENERATED ALWAYS AS 
(CASE 
	WHEN glucose > 139 THEN TRUE 
	WHEN CAST(outcome AS BOOLEAN) = TRUE THEN TRUE 
	ELSE FALSE END) STORED 
);

CREATE TABLE fram(
male BOOLEAN,
age NUMERIC,
education NUMERIC,
currentSmoker BOOLEAN,
cigsPerDay NUMERIC,
BPMeds NUMERIC,
prevalentStroke NUMERIC,
prevalentHyp NUMERIC,
diabetes NUMERIC,
totChol NUMERIC,
sysBP NUMERIC,
diaBP NUMERIC,
BMI NUMERIC,
heartRate NUMERIC,
glucose NUMERIC,
TenYearCHD BOOLEAN
);

\copy pima FROM 'diabetes.csv' DELIMITER ',' CSV HEADER;
\copy fram FROM 'framingham.csv' DELIMITER ',' CSV HEADER;