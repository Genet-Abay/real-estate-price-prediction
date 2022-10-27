import pandas as pd
import numpy as np
from sklearn  import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics as mt

from data_acquisition import scrap_data



def get_iqr_values(df_in, col_name):
    median = df_in[col_name].median()
    q1 = df_in[col_name].quantile(0.25) # 25th percentile / 1st quartile
    q3 = df_in[col_name].quantile(0.75) # 7th percentile / 3rd quartile
    iqr = q3-q1 #Interquartile range
    minimum  = q1-1.5*iqr # The minimum value or the |- marker in the box plot
    maximum = q3+1.5*iqr # The maximum value or the -| marker in the box plot
    return median, q1, q3, iqr, minimum, maximum

def remove_outliers(df_in, col_name):
    _, _, _, _, minimum, maximum = get_iqr_values(df_in, col_name)
    df_out = df_in.loc[(df_in[col_name] > minimum) & (df_in[col_name] < maximum)]
    return df_out



def clean_data(df):
    df = df.drop(['ID','Sub type','Floor', 'IsIsolated', 'SchoolDistance', 'ShopDistance', 'TransportDistance', 'HasSeaView', 'RegionCode', 'TotalRoomCount', 'HasBalcony', 'GardenArea', 'HasAttic', 'HasDiningRoom', 'LivingRoomArea', 'NetHabitableSurface', 'street'], axis=1)
    
    #remove rows where value of column NetHabitableSurface(17% missing) and BedroomCount(2%)is nan in order to avoid the bias from mean media or mode insertion
    #Remove rows with nan values in column province and region -> post code in that row also fault which can not be extracted from lookup table
    df = df.dropna(subset=['Price', 'NetHabitableSurface(msq)', 'BedroomCount', 'Province', 'Region'])

    #drop duplicate records
    df = df.drop_duplicates(keep='first')   

    #Hard to input with mode values for nan, better to introduce new value of 'unknown'   
    df.fillna({'KitchekType':'Unknown','BuildingCondition':'Unknown' },inplace=True)

    #creating new BuildingAge column from construction year so that it is easy to input nan values with mean age value
    df['BuildingAge'] = 2022 - df['ConstructionYear'] 
    df = df.drop('ConstructionYear', axis=1)
    mean_buildingAge = round(df['BuildingAge'].mean())    
    df.fillna({'BuildingAge':mean_buildingAge},inplace=True)

    #all non empty cells are TRUE, so the empty cells probably be FALSE 
    df.fillna({'HasLift':False, 'HasGarden': False, 'HasBasement': False, 'IsDoubleGlaze': False},inplace=True)

    #the following feature's nan values will be imputed by their respective mode values
    mode_heatingType = df['HeatingType'].mode()[0]  #common to the community
    mode_facadeCount = df['FacadeCount'].mode()[0] # common trend
    mode_floodzone = df['FloodZoneType'].mode()[0] #common location characterstics
    df.fillna({'HeatingType':mode_heatingType, 'FacadeCount':mode_facadeCount, 'FloodZoneType': mode_floodzone}, inplace=True)

    #removing outliers for selected columns
    col_names_toremove_outliers = ['Price', 'NetHabitableSurface(msq)',	'BedroomCount',	'FacadeCount',	'BuildingAge']
    for col in col_names_toremove_outliers:
        df=  remove_outliers(df, col)
    return df


def encode_onehot(dataframe, feature_names):
    df_dummies=[]
    for f in feature_names:
        dummies = pd.get_dummies(dataframe[[f]])
        dataframe = dataframe.drop(f, axis=1)
        df_dummies.append(dummies)

    cat_df_dummies = pd.concat(df_dummies, axis=1)
    final_df = pd.concat([dataframe, cat_df_dummies], axis=1)    
    return(final_df)

def encode_binary(dataframe, feature_names):
    for f in feature_names:
        dataframe[f] = dataframe[f].astype(int)     
    return(dataframe)

def encoding_categorical_features(df):    
    # creating consistent and smaller category
    df.loc[(df['FloodZoneType']!='NON_FLOOD_ZONE') & (df['FloodZoneType']!='POSSIBLE_FLOOD_ZONE'), 'FloodZoneType'] = 'FloodZone'
    df.loc[(df['KitchekType']=='HYPER_EQUIPPED') & (df['KitchekType']=='USA_HYPER_EQUIPPED')& (df['KitchekType']=='USA_INSTALLED'),  'KitchekType'] = 'INSTALLED'
    df.loc[(df['KitchekType']=='USA_SEMI_EQUIPPED'),  'KitchekType'] = 'SEMI_EQUIPPED'
    df.loc[(df['KitchekType']=='USA_UNINSTALLED'),  'KitchekType'] = 'NOT_INSTALLED'
    df.loc[(df['HeatingType']!='GAS') & (df['HeatingType']!='ELECTRIC')  & (df['HeatingType']!='FUELOIL'), 'HeatingType'] = 'Others'
    df.loc[(df['BuildingCondition']=='TO_BE_DONE_UP') & (df['BuildingCondition']!='TO_RESTORE'), 'BuildingCondition'] = 'TO_RENOVATE'
    df.loc[(df['FloodZoneType']!='NON_FLOOD_ZONE') & (df['FloodZoneType']!='POSSIBLE_FLOOD_ZONE'), 'FloodZoneType'] = 'FloodZone'
    df.loc[(df['KitchekType']=='HYPER_EQUIPPED') & (df['KitchekType']=='USA_HYPER_EQUIPPED')& (df['KitchekType']=='USA_INSTALLED'),  'KitchekType'] = 'INSTALLED'
    df.loc[(df['KitchekType']=='USA_SEMI_EQUIPPED'),  'KitchekType'] = 'SEMI_EQUIPPED'
    df.loc[(df['KitchekType']=='USA_UNINSTALLED'),  'KitchekType'] = 'NOT_INSTALLED'
    df.loc[(df['HeatingType']!='GAS') & (df['HeatingType']!='ELECTRIC')  & (df['HeatingType']!='FUELOIL'), 'HeatingType'] = 'Others'
    df.loc[(df['BuildingCondition']=='TO_BE_DONE_UP') & (df['BuildingCondition']!='TO_RESTORE'), 'BuildingCondition'] = 'TO_RENOVATE'
    
    #One-hot or binary encoding for selected column
    cols_categorical_forOneHotEncoding = ['FloodZoneType', 'HeatingType', 'KitchekType', 'Region','BuildingCondition', 'Province', 'locality']
    cols_categorical_forBinaryEncoding = ['HasBasement', 'HasLift', 'IsDoubleGlaze', 'HasGarden']

    df=encode_binary(df, cols_categorical_forBinaryEncoding)
    df = encode_onehot(df, cols_categorical_forOneHotEncoding)

    #encoding appartment type as binary aftr change of name
    df.rename(columns={'Type': 'IsHouse'}, inplace=True)
    df["IsHouse"] = np.where(df["IsHouse"] == "HOUSE", 1, 0)
    return df



def training_model(df):
    scale_standard= preprocessing.StandardScaler()
    X = df.drop(['Price','PostCode'], axis=1)
    Y = df['Price']
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)


    cols_toscale = ['NetHabitableSurface(msq)', 'BuildingAge']
    x_train = x_train.copy()
    x_test = x_test.copy()
    x_train[cols_toscale] = scale_standard.fit_transform(x_train[cols_toscale])
    x_test[cols_toscale] = scale_standard.fit_transform(x_test[cols_toscale])

    #create  models 
    rforest_regr = RandomForestRegressor(n_estimators=28,random_state=0)
   
    rforest_regr.fit(x_train,y_train)  

    #model score
    rforest_y_predicted = rforest_regr.predict(x_test)
    score = mt.r2_score(y_test, rforest_y_predicted)
    
    return(rforest_regr, score)



def main():
    path_to_data = scrap_data.start_gathering_data()
    df = pd.read_csv(path_to_data)
    df = clean_data(df)
    df = encoding_categorical_features(df)
    model, score = training_model(df)
    print(f"the score of the molel is {score}")


main()