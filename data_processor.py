#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Surf Spot Web Scraper - Data Processing Functions

This module contains functions for processing and cleaning the 
extracted data from the web scraper.
"""

def clean_df(df):
    """
    Clean the DataFrame by removing empty columns and rows.
    
    Args:
        df (pandas.DataFrame): DataFrame to clean
        
    Returns:
        pandas.DataFrame: Cleaned DataFrame
    """
    # Remove columns with empty or '' labels
    df = df.drop(columns=[col for col in df.columns if col == '' or col is None])

    # Remove columns where all data points are empty
    df = df.drop(columns=[
        col for col in df.columns 
        if df[col].isnull().all() or (len(df[col]) > 0 and df[col][0] == "")
    ])

    return df
