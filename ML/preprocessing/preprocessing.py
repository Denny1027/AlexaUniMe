def split_dataset(x_num, y_num, ds):
    """
    Questa funzione permette di dividere automaticamente un file .csv caricato tramite la funzione "read_csv()".

    Solitamente, le var. dipendenti si trovano nelle prime x posizioni, mentre le var. indipendenti si trovano nelle
        ultime y colonne del file.
    :param x_pos: prime x colonne del file csv (x compreso). Rappresentano variabili dipendenti
    :param y_pos: ultime y colonne del file csv. Rappresentano variabili indipendenti
    :return: x numpy set, y numpy set
    """

    x = ds.iloc[:, : x_num].values
    y = ds.iloc[:, -y_num:].values

    return x, y


def scores(y_true, y_pred):
    from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
    print("--Confusion Matrix--")
    print(confusion_matrix(y_true, y_pred))
    print("--------------------")
    print("Accuracy Score = ", accuracy_score(y_true, y_pred))
    print("Precision Score = ", precision_score(y_true, y_pred))
    print("Recall Score = ", recall_score(y_true, y_pred))


def label_encoder(xds, column):
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    xds[:, column] = le.fit_transform(xds[:, column])
    print("Label Encoded:")
    for i in range(len(le.classes_)):
        print(i, ":", le.classes_[i])


def one_hot_encoder(xds, column):
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    import numpy as np

    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [column])], remainder='passthrough')
    ret = np.array(ct.fit_transform(xds))

    print("One Hot Encoding")
    for i in range(len(ct.get_feature_names())):
        if 'encoder__x0_' in ct.get_feature_names()[i]:
            print("Colonna ", i+1, "= ", ct.get_feature_names()[i].replace("encoder__x0_", ""))

    return ret


def train_test_split(x, y, test_size = 0.2, random_seed=0):
    from sklearn.model_selection import train_test_split
    return train_test_split(x, y, test_size=test_size, random_state=random_seed)

