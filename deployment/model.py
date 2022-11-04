from pyexpat.errors import XML_ERROR_TEXT_DECL
import pandas as pd
import numpy as np
from sklearn  import pipeline, preprocessing
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn import metrics as mt
import pickle
# from data_acquisition import scrap_data



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
    df = df.drop(['ID','Floor', 'IsIsolated', 'SchoolDistance', 'ShopDistance', 'TransportDistance', 'HasSeaView', 'RegionCode', 'TotalRoomCount', 'HasBalcony', 'GardenArea', 'HasAttic', 'HasDiningRoom', 'LivingRoomArea', 'NetHabitableSurface', 'street'], axis=1)
    
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

def model_pipeline(df):
    
    X = df.drop(['Price','PostCode'], axis=1)
    Y = df['Price']
    cols_categorical_forOneHotEncoding = ['FloodZoneType', 'Sub type', 'HeatingType', 'KitchekType', 'Region','BuildingCondition', 'Province', 'locality']
    cols_categorical_forBinaryEncoding = ['Type', 'HasBasement', 'HasLift', 'IsDoubleGlaze', 'HasGarden']

    categorical_features = cols_categorical_forOneHotEncoding + cols_categorical_forBinaryEncoding
    numeric_features = ['NetHabitableSurface(msq)', 'BuildingAge']

    numeric_transformer = Pipeline(steps=[('scaler', preprocessing.StandardScaler())])
    categorical_transformer = Pipeline(steps=[('encoder', preprocessing.OneHotEncoder(handle_unknown="ignore"))])
   

    preprocessor = ColumnTransformer(
        transformers=[
        ('numeric', numeric_transformer, numeric_features),
        ('categorical', categorical_transformer, categorical_features)
    ]) 
    
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

    model_pipeline = Pipeline(steps=[("preprocess",  preprocessor), ('model', RandomForestRegressor(n_estimators=28,random_state=0))])

    model_pipeline.fit(x_train, y_train)
    pred_y = model_pipeline.predict(x_test)
    score= mt.r2_score(y_test, pred_y)
    return model_pipeline, score

def main():
    # path_to_data = scrap_data.start_gathering_data()
    path_to_data = "C:/BeCode/LocalRepos/documents/real_estate_data_25to29.csv"
    df = pd.read_csv(path_to_data)
    df = clean_data(df)
    print(df.columns)
    # model, score = model_pipeline(df)
    # print(f"the r2 score of the molel is {score}")
    # pickle.dump(model, open('model.pkl','wb'))

main()