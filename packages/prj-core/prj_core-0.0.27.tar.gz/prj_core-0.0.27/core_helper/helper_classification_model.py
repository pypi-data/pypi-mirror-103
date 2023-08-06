# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:44:39 2021

@author: User
"""
import core_helper.helper_general as hg
hg.set_base_path()

import json
import os
import math
import sys

import pandas as pd
import numpy as np
import time
from datetime import datetime

#import core_helper.helper_plot as hp
import src.Prj_Core.core_helper.helper_plot as hp

#import model.general as g
import src.Prj_Core.core_helper.model.general as g

import src.Prj_Core.core_helper.model.neg_bagging_fraction__lgb_model as nbf_lgb_model
import src.Prj_Core.core_helper.model.scale_pos_weight__lgb_model as spw_lgb_model
import src.Prj_Core.core_helper.model.custom_bagging__lgb_model as cb_lgb_model

#import model.neg_bagging_fraction__lgb_model as nbf_lgb_model
#import model.scale_pos_weight__lgb_model as spw_lgb_model
#import model.custom_bagging__lgb_model as cb_lgb_model

def modelar_clasificacion_binaria(strategy, X_train=None,y_train=None,X_test=None,y_test=None,url=None):
    start = time.time()
    if (strategy=="neg_bagging_fraction__lgb_model"):
        model , predicted_probas   = nbf_lgb_model.modelar(X_train,y_train,X_test,y_test,url)
    if (strategy=="scale_pos_weight__lgb_model"):
        model , predicted_probas   = spw_lgb_model.modelar(X_train,y_train,X_test,y_test,url)
    if (strategy=="custom_bagging__lgb_model"):
        model , predicted_probas   = cb_lgb_model.modelar(X_train,y_train,X_test,y_test,url)

    kpis = generar_reporte(model,predicted_probas,X_test,y_test,url)
    print("Time elapsed: ", time.time() - start)
    
    return model , predicted_probas  , kpis
    

def generar_reporte(model,predicted_probas, X_test, y_test,url):    
    kpis = hp.print_kpis_rendimiento_modelo(y_test,predicted_probas,url)   
    if  isinstance(model, list)==False:
        hp.print_shap_plot(model, X_test, url)      
    g.generate_summary_evaluation(X_test,predicted_probas,y_test,url) 
    return kpis
    
    
def predecir_clasificacion_binaria(model, X=None, umbral=0.5):
    print("inicio predecir_clasificacion_binaria")
    if  isinstance(model, list)==False:    
        predicted_probas = model.predict_proba(X)
        y_prob_uno = predicted_probas[:,1]
    else:
        y_pred,y_prob_uno , predicted_probas = cb_lgb_model.predict_proba(model, X)
    
    y_pred_uno = np.where(y_prob_uno >= umbral, 1, 0).tolist()
    print("fin  predecir_clasificacion_binaria")
    return y_pred_uno, y_prob_uno , predicted_probas



def get_result_df(KPIs_list):
    df = pd.DataFrame(columns=["Macro Región","Modelo","T Train","T Test",'Precision', 'Recall', 'F1','Average Precision','ROC AUC'])
    for idx, result  in enumerate(KPIs_list):
        mr = result[0]
        mod = result[1]
        
        t_train = result[2]
        t_test = result[3]
        
        Ks = result[4]
        result_rd = [mr,mod,t_train,t_test]+[round(num, 3) for num in list(Ks)]
        df.loc[idx] = result_rd

        #df.loc[i] = list(KPIs)

    return df

def get_kpi_df_nacional(PATH_RESULT="resultado",grupos_grados=None):
    df_resumen = None
    grupos_grados = {"1 prim": [4],"2 prim": [5], "3-5 prim": [6,7,8], "6 prim": [9], "1-4 sec": [10,11,12,13],"5 sec": [14]}
    lista_mr = ["centro","norte","sur","oriente","lima"]
    
    list_df = []
    for key, grupo_grado  in grupos_grados.items():
        path = "{}/{}/{}".format(PATH_RESULT,key,"resultados.xlsx")
    
        df = pd.read_excel (path,index_col=0)
        idx = df.groupby(['Macro Región'])['Average Precision'].transform(max) == df['Average Precision']
        df = df[idx].copy()
        df["key_grupo_grado"] = key
        list_df.append(df)
    
    df_resumen = pd.concat(list_df)
    return df_resumen



def export_resultado_final_nacional(alto=0.75,medio=0.5,path="resultado"):
    grupos_grados = {"1 prim": [4],"2 prim": [5], "3-5 prim": [6,7,8], "6 prim": [9], "1-4 sec": [10,11,12,13],"5 sec": [14]}
    lista_mr = ["centro","norte","sur","oriente","lima"]
    hg.validar_directorio(path)
    PATH_RESULT = path
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    #"norte","sur"
    #grupos_grados = { "3-5 prim": [6,7,8]}
    #lista_mr = ["norte"]
    df_resumen = get_kpi_df_nacional(PATH_RESULT,grupos_grados)
        
    dt = {'COD_MOD':str,'COD_MOD_T':str,'ANEXO':int,'ANEXO_T':int,'EDAD':int,
      'N_DOC':str,'COD_MOD_T_MENOS_1':str,
      'ANEXO_T_MENOS_1':int,'NUMERO_DOCUMENTO_APOD':str,'ID_PERSONA':int}
    
    list_result = []
    columns = ['ID_PERSONA','custom_bagging__lgb_model', 'scale_pos_weight__lgb_model', 'neg_bagging_fraction__lgb_model']
    
    for key, grupo_grado  in grupos_grados.items():
        
        for macro_region in lista_mr:
            best_model = df_resumen[(df_resumen.key_grupo_grado==key) & (df_resumen['Macro Región']==macro_region)].Modelo.iloc[0]
            print(best_model," - ",macro_region," - ",key)
            specific_url = '{}/{}/{}/{}'.format(PATH_RESULT,key,macro_region,"X_t_mas_1.csv")
            df=pd.read_csv(specific_url,dtype=dt, encoding="utf-8",usecols=columns) 
            df['RISK_SCORE'] = df[best_model] 
            list_result.append(df)
            
          
    df_nacional = pd.concat(list_result)
    df_nacional.drop_duplicates(subset ="ID_PERSONA",  keep = "first", inplace = True)
      
    df_nacional['PREDICCION']=None
    df_nacional.loc[(df_nacional['RISK_SCORE']>=alto) & (df_nacional['RISK_SCORE']<=1), 'PREDICCION'] = 3
    df_nacional.loc[(df_nacional['RISK_SCORE']>=medio) & (df_nacional['RISK_SCORE']<alto), 'PREDICCION'] = 2
    df_nacional.loc[df_nacional['RISK_SCORE']<medio, 'PREDICCION'] = 1
    df_nacional.PREDICCION = df_nacional.PREDICCION.astype(int)      
    
    cls_export = ["ID_PERSONA","RISK_SCORE",'PREDICCION']
    print("Total de registros : ",df_nacional.shape)
    df_nacional[cls_export].to_stata("{}/nacional_{}.dta".format(PATH_RESULT,dt_string)) 
    return df_nacional





'''            
def split_x_y(ID_GRADO,macro_region,modalidad="EBR"):

    lista_regiones = get_macro_region(macro_region)
    list_join_n=[]
    list_join_n_mas_1=[]
    for region in lista_regiones:

        url_dir = "{}/{}/".format(region,ID_GRADO)
        print(url_dir)
        try:
            df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        except:
            continue
        
        #df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        df_join_n['REGION']= region
        df_join_n_mas_1['REGION']= region
        
        ############tempEEE#######
        df_join_n['D_REGION']= region
        df_join_n_mas_1['D_REGION']= region
        ########################
        
        
        print(region)
        print(df_join_n.DESERCION.value_counts())
        list_join_n.append(df_join_n)
        list_join_n_mas_1.append(df_join_n_mas_1)

    df_join_n = pd.concat(list_join_n)
    df_join_n_mas_1 = pd.concat(list_join_n_mas_1)

    fe_df(df_join_n,df_join_n_mas_1)

    X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval , ID_P_T,ID_P_T_MAS_1, y = tranform_data(df_join_n,df_join_n_mas_1,False)
    

    return X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval ,  ID_P_T,ID_P_T_MAS_1 , y
   

def get_saved_join_data(url_dir,sub_dir="data",modalidad="EBR"):
    
    if not url_dir:
        url_dir="../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir+"/"
    else:
        url_dir = '{}/{}'.format("../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir,url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    if (modalidad=="EBR"):
        specific_url = url_dir+"data.csv"
        specific_url_eval = url_dir+"data_eval.csv"
    else:
        specific_url = url_dir+"data_{}.csv".format(modalidad)
        specific_url_eval = url_dir+"data_eval_{}.csv".format(modalidad)        
    
    dt = {'COD_MOD':str,'COD_MOD_T':str,'ANEXO':int,'ANEXO_T':int,'EDAD':int,
          'N_DOC':str,'COD_MOD_T_MENOS_1':str,
          'ANEXO_T_MENOS_1':int,'NUMERO_DOCUMENTO_APOD':str,'ID_PERSONA':int}

    df=pd.read_csv(specific_url,dtype=dt, encoding="utf-8") 
    df_eval=pd.read_csv(specific_url_eval,dtype=dt, encoding="utf-8") 
    
    return df,df_eval

 ''' 