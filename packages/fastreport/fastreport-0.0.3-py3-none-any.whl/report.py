def classification_report(df_features,df_target,test_size=0.3):
    '''

    df_features: Pandas DataFrame
    df_target: Pandas Series
    test_size: If float, should be between 0.0 and 1.0 and represent the proportion of the
    dataset to include in the test split.
    '''
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report,confusion_matrix,roc_auc_score,roc_curve,accuracy_score,recall_score,precision_score
    from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neighbors import KNeighborsClassifier
    from warnings import filterwarnings
    filterwarnings('ignore')
    if df_features.isna().sum().sum()==0:
        df_cat=df_features.select_dtypes(include="object")
        df_num=df_features.select_dtypes(exclude="object")
        if df_cat.shape[1]!=0:
            encoding=pd.get_dummies(df_cat,drop_first=True)
            X=pd.concat([encoding,df_num],axis=1)
        else:
            X=df_features
        labelencoder = LabelEncoder()
        y = labelencoder.fit_transform(df_target)


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        algo=[LogisticRegression(),GaussianNB(),DecisionTreeClassifier(),RandomForestClassifier(),
              GradientBoostingClassifier(),AdaBoostClassifier()]
        results=pd.DataFrame(columns=["Algorithm_name",'Train_accuracy','Test_accuracy',"Test_Roc_Auc_score",'Test_recall','Test_precision'])
        for i in algo:

            i.fit(X_train, y_train)
            train_pred_i=i.predict(X_train)
            train_acc=accuracy_score(y_train,train_pred_i)
            test_pred_i=i.predict(X_test)
            test_acc=accuracy_score(y_test,test_pred_i)
            recall=recall_score(y_test,test_pred_i)
            precision=precision_score(y_test,test_pred_i)
            roc_auc=roc_auc_score(y_test,test_pred_i)
            row={"Algorithm_name":str(i)[:-2],'Train_accuracy':train_acc,"Test_accuracy":test_acc,"Test_Roc_Auc_score":roc_auc,'Test_recall':recall,"Test_precision":precision}
            results=results.append(row,ignore_index=True)
        return results
    else:
        print("The data contains missing values, first handle missing values and then pass the data")
