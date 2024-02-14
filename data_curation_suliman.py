import argparse
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import seaborn as sns


## Read config file 
parser = argparse.ArgumentParser()
parser.add_argument('--include-all-cases', action=argparse.BooleanOptionalAction)
args = parser.parse_args()
include_all_cases = args.include_all_cases

## Read tables as dataframes
df_admin = pd.read_csv("pseudon_tbladmin.csv")
df_headcircumf = pd.read_csv("pseudon_tblheadcircumf.csv")
df_height = pd.read_csv("pseudon_tblheight.csv")
df_weight = pd.read_csv("pseudon_tblweight.csv")

## Q1 Merge tables into single one containing clinical information
df_measures = pd.merge(df_headcircumf, pd.merge(df_height, df_weight, on=["patnr", "fallnr", "startdat"], how="outer"),\
					   on=["patnr", "fallnr", "startdat"], how="outer")
if include_all_cases:
	df_merged = pd.merge(df_admin, df_measures, on=["patnr", "fallnr"], how="outer")
else:
	df_merged = pd.merge(df_admin, df_measures, on=["patnr", "fallnr"], how="inner")

## Q2 Rename columns accordingly
names_dict = {"patnr": "patientNumber", "gebdat": "dateOfBirth", "verstorben":"deceased", "fallnr": "caseNumber", "fallart": "caseDoctor", "eindat": "entryDate",\
			 "ausdat": "exitDate", "startdat": "dateOfMeasure"}
df_merged = df_merged.rename(columns=names_dict)

## Q3/Q4/Q5 Correct inconsistent height and weight into cm and kg respectively
df_merged[["weight_value", "weight_unit"]] = df_merged[["weight_value", "weight_unit"]].apply(lambda x: (x[0]/1000, "kg") if x[1]=="g" else x, axis=1)

## Q6 Convert date from object to datetime and apply YYYY-MM-DD HH:MM format
df_merged["dateOfBirth"] = pd.to_datetime(df_merged["dateOfBirth"], format="%d/%m/%Y %H:%M", errors="coerce").dt.strftime("%Y-%m-%d %H:%M")
df_merged["entryDate"] = pd.to_datetime(df_merged["entryDate"], format="%d/%m/%Y %H:%M", errors="coerce").dt.strftime("%Y-%m-%d %H:%M")
df_merged["exitDate"] = pd.to_datetime(df_merged["exitDate"], format="%d/%m/%Y %H:%M", errors="coerce").dt.strftime("%Y-%m-%d %H:%M")
df_merged["dateOfMeasure"] = pd.to_datetime(df_merged["dateOfMeasure"], format="%Y-%m-%d %H:%M:%S", errors="coerce").dt.strftime("%Y-%m-%d %H:%M")

## Q7 Transform sex values from M/W to Man/Woman
df_merged["sex"] = df_merged["sex"].apply(lambda x: "Man" if x=="M" else ("Woman" if x=="W"else np.nan))

## Persist final table
if include_all_cases:
	df_merged.to_csv("tbl_combined_all_cases_included.csv", index=False)
	print(df_merged.shape)
	print(df_merged)
else:
	df_merged.to_csv("tbl_combined.csv", index=False)
	print(df_merged.shape)
	print(df_merged)