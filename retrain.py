from training import data_ingestion, data_preprocessing, model_training_and_evaluation

if __name__=='__main__':
    df = data_ingestion.load_data()

    pipeline, X_train, y_train, X_test,y_test = data_preprocessing.preprocess_data(df)
    
    best_model, best_params = model_training_and_evaluation.model_training_and_eval(pipeline=pipeline, 
                                                                                    X_train=X_train, 
                                                                                    y_train=y_train, 
                                                                                    X_test=X_test, 
                                                                                    y_test=y_test)

    model_training_and_evaluation.save_model_and_params(best_model, best_params)