'''from sklearn.datasets import load_iris
iris=load_iris()
X=iris.data
Y=iris.target
print(f"shape of featured (X):(X.shape)")
print(f"shape of labels (Y):(Y.shape)")
print("\nfirst 5 rows of features (z):")
print(X[:5])
print("\nfirst 5 labels (Y):")
print(Y[:5])

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.50,random_state=42)
print(f"Training samples : {X_train.shape}")
print(f"Testing samples : {X_test.shape}")

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
knn=KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train,Y_train)
Y_pred = knn.predict(X_test)
accuracy = accuracy_score(Y_test,Y_pred)
print("model's predictions: ",Y_pred)
print("actual answers:   ",Y_test)
print(f"Model Accuracy: {accuracy*100:.2f}%")'''

import re
text="python is easy and fun"
pattern=r"\s"
new_text=re.sub(pattern,"_",text)
print(new_text)
