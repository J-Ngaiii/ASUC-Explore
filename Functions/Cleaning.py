import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import re
import unittest
import pytest
import spacy
nlp_model = spacy.load("en_core_web_md")
from sklearn.metrics.pairwise import cosine_similarity 
from rapidfuzz import fuzz, process

def type_test(df, str_cols=None, int_cols=None, float_cols=None, date_cols=None):
    """
    Function checks the types of all entries in designated columns for the inputted dataframe.
    Checks if designated columns contain only the designated datatype or NaN values.
    """

    if (str_cols is None) and (int_cols is None) and (float_cols is None) and (date_cols is None):
        raise ValueError('No columns to check inputted')    
    if str_cols is not None:
        if df[str_cols].applymap(lambda x: isinstance(x, str) or pd.isna(x)).all().all(): print(f"String test complete with no errors!")
        else: print(f"ERROR string columns do not have just strings or NaN values")
    if int_cols is not None: 
        if df[int_cols].applymap(lambda x: isinstance(x, int) or pd.isna(x)).all().all(): print(f"Int test complete with no errors!")
        else: print(f"ERROR int columns do not have just int or NaN values")
    if float_cols is not None:
        if df[float_cols].applymap(lambda x: isinstance(x, float) or pd.isna(x)).all().all(): print(f"Float test complete with no errors!")
        else: print(f"ERROR float columns do not have just float or NaN values")
    if date_cols is not None:
        if df[date_cols].applymap(lambda x: isinstance(x, pd.Timestamp) or pd.isna(x)).all().all(): print(f"Datetime test complete with no errors!")
        else: print(f"ERROR datetime columns do not have just datetime or NaN values")

def row_test(cleaned_df, raw_df=None, num=None):
    """
    Checks to see if the #rows in the original dataframs is the same as the #rows in the cleaned dataframe.
    """
    
    if (raw_df is None) and (num is None):
        raise ValueError('No 2nd or 3rd argument detected. Please input either raw dataframe or specified number of rows to check cleaned dataframe against.')
    if (raw_df is not None) and (num is not None):
        raise ValueError('Row test cannot take three inputs. Either compare against raw dataframe or input number of rows cleaned dataframe is suppoed to have')
    
    if raw_df is not None: 
        if raw_df.shape[0] == cleaned_df.shape[0]: print(f"Number of rows consistent at {cleaned_df.shape[0]}")
        else: print(f"ERROR number of rows inconsistent, raw df has {raw_df.shape[0]} rows while cleaned df has {cleaned_df.shape[0]} rows")
    if num is not None:
        if num == cleaned_df.shape[0]: print(f"Number of rows consistent, df has {cleaned_df.shape[0]} rows")
        else: print(f"ERROR number of columns inconsistent, supposed to be {num} but df actually has {cleaned_df.shape[0]} rows") 

def col_test(cleaned_df, raw_df=None, num=None):
    """
    Checks to see if the columns in the original dataframs is the same as the columns in the cleaned dataframe and/or if they have the same number of columns
    """
    
    if (raw_df is None) and (num is None):
        raise ValueError('No 2nd or 3rd argument detected. Please input either raw dataframe or specified number of columns to check cleaned dataframe against.')
    
    if raw_df is not None: 
        if (raw_df.columns == cleaned_df.columns).all(): print(f"Name of columns consistent, df has columns {list(cleaned_df.columns)}")
        else: print(f"ERROR name of columns inconsistent, raw df has columns {list(raw_df.columns)} while cleaned df has columns {list(cleaned_df.columns)}")
    if num is not None:
        if num == len(cleaned_df.columns): print(f"Number of columns consistent, df has {len(cleaned_df.columns)} columns")
        else: print(f"ERROR number of columns inconsistent, supposed to be {num} but df actually has {len(cleaned_df.columns)} columns") 

def col_mismatch_test(df1, df2, print_matches=False, d1offset=0):
    """
    Takes in two dataframes with semi-sorted columns and checks if a the nth column in df1 is the same as the nth column in df2.
    If not then checks if a column of the same name is in df2 at all but just in a different spot

    Note this isn't a fully comprehensive test that checks every combination of possible matches and mismatches, it's just here to make spotting matched and mismatched columns easier.
    Burden of figuring out how to resolve mismatched or extra columns is on the programmer.
    """
    
    df1_cols = pd.Series(df1.columns[d1offset:])
    df2_cols = pd.Series(df2.columns)

    # Shape comparison and initialization
    same_shape = len(df1_cols) == len(df2_cols)
    excluded = None
    if len(df1_cols) > len(df2_cols):
        match = df1_cols[:len(df2_cols)].equals(df2_cols)
        excluded = df1_cols[len(df2_cols):]
        larger = 'df1'
    elif len(df1_cols) < len(df2_cols):
        match = df1_cols.equals(df2_cols[:len(df1_cols)])
        excluded = df2_cols[len(df1_cols):]
        larger = 'df2'
    else:
        match = df1_cols.equals(df2_cols)
    
    # Display results
    if match:
        if same_shape:
            print("No mismatches in columns between df1 and df2")
        else:
            print(f"No mismatches in examined columns but {larger} columns {excluded} excluded due to mismatched shape")
    else:
        if not same_shape:
            print(f"Shape discrepancy: {larger} is the larger dataframe by {np.abs(len(df1_cols) - len(df2_cols))} column(s)")
        for i in range(min(len(df1_cols), len(df2_cols))):
            if df1_cols[i] == df2_cols[i]:
                if print_matches:
                    print(f"Column {i+1} MATCHES ('{df1_cols[i]}' for df1 and '{df2_cols[i]}' for df2)")
            else:
                if df1_cols[i] in df2_cols.values:
                    print(f"Column {i+1} MISMATCH ('{df1_cols[i]}' for df1 and '{df2_cols[i]}' for df2) but '{df1_cols[i]}' IS in df2")
                else:
                    print(f"Column {i+1} MISMATCH ('{df1_cols[i]}' for df1 and '{df2_cols[i]}' for df2) and '{df1_cols[i]}' NOT in df2")

    # If extra columns in the larger dataframe, list them
    if excluded is not None and len(excluded) > 0:
        print(f"Extra columns in {larger}: {list(excluded)}")