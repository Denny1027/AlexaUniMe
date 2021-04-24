import pandas as pd
from preprocessing import preprocessing as pp
from sklearn.preprocessing import StandardScaler
from ml_classes import ann


ds = pd.read_csv("./files/Churn_Modelling.csv")
x = ds.iloc[:, 3: -1].values
y = ds.iloc[:, -1].values

pp.label_encoder(x, 2)
x = pp.one_hot_encoder(x, 1)

x_train, x_test, y_train, y_test = pp.train_test_split(x, y)

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

machine = ann.ClassificatorNeuralNetwork(6, 6, 1, name="my_test")
machine.load_ann()
# machine.train(x_train, y_train)
pr = machine.predict(sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]]))
print(pr)