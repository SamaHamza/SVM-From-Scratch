# -*- coding: utf-8 -*-
"""SVM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SXz50AAxIjYZh3Pr7_OlKSAQRxrcgzVr

### Importing the needed libraries:
"""

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#Reading the dataset:
data = pd.read_csv('/content/breast-cancer.csv')

data.head()

"""# Understanding the dataset:

---


> To perform SVM we need to understand how our dataset distributes among most of the features. Therefore, data visualization is an important step here!



"""

px.histogram(data_frame=data, x='diagnosis', color='diagnosis',color_discrete_sequence=['#05445E','#75E6DA'])

px.scatter(data_frame=data,x='symmetry_worst',color='diagnosis',color_discrete_sequence=['#05445E','#75E6DA'])

px.scatter(data_frame=data,x='concavity_worst',color='diagnosis',color_discrete_sequence=['#05445E','#75E6DA'])

px.scatter(data_frame=data,x='fractal_dimension_worst',color='diagnosis',color_discrete_sequence=['#05445E','#75E6DA'])

"""<h3  ><b> As the figure show the dataset is non-linearly separable.</b></h3>

---


"""

data.head()

#drop redundant or irrelevant to the target columns
data.drop('id', axis=1, inplace=True)

#encode the label into 1/0
data['diagnosis'] = (data['diagnosis'] == 'M').astype(int)

#Get highly correlated features

corr = data.corr()
plt.figure(figsize=(20,20))
sns.heatmap(corr, cmap='mako_r',annot=True)
plt.show()

# Get the absolute value of the correlation
cor_target = abs(corr["diagnosis"])

#removing the highly correlated features from the dataset:
# Select highly correlated features (thresold = 0.2)
relevant_features = cor_target[cor_target>0.2]

# Collect the names of the features
names = [index for index, value in relevant_features.iteritems()]

# Drop the target variable from the results
names.remove('diagnosis')

# Display the results
print(names)

data.describe().T

data.head()

#Assign data and labels
X = data[names].values
y = data['diagnosis']

#Scale the data (StandardScaler)
def scale(X):

    # Calculate the mean and standard deviation of each feature
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)

    # Standardize the data
    X = (X - mean) / std
    return X
X = scale(X)

# Splittiny our data into training and testing:
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42) #split the  data into traing and validating

"""# Model Implementation:

---



<h4><b<How the algorithm works</b></h4>
Our goal is to find a hyperplane that separates the data into 2 categories (Binary Classification)

<h3>Key Points:</h3>
<ul><li>Hyperplane:</li>
A hyperplane is a subspace whose dimensions is less than of it's ambient space for example in n-dimensional subspace the hyperplane will be (n-1)-dimensional

For SVMS the goal of this hyperplane has to Maximize margin between the two classes

Hyperplane equation is :

<p align ="center">wx−b=0≥1,aty=1</p>
<p align ="center">wx−b=0≤1,aty=−1,</p>



---



>       In general:                         y(wx−b)=0≥1



---



<br/>

<li>Margin:</li>
Margin is the distance between the hyperplane and the data-points closest to it (support vectors)




---



>           Gradients Equation:           For yi(wxi−b)≥1

---



<p align ="center">∂J/∂w=2λw</p>
<p align ="center">∂J∂b=0</p>
For yi(wxi−b)<1:

<p align ="center">∂J∂w=2λw−yixiM
∂J∂b=−yi</p>
where J is the cost function of SVM, λ is the regularization parameter, w is the weight vector, b is the bias term, xi is the i-th data point, and yi is the corresponding label.</ul>
"""

#start our svm code:
class SVM:

    #Initializes the SVM model parameters
    def __init__(self, iterations=2000, lr=0.01, lambdaa=0.01):

        self.lambdaa = lambdaa
        self.iterations = iterations
        self.lr = lr
        self.w = None
        self.b = None

    #Initializes the weights and bias.
    def initialize_parameters(self, X):

        m, n = X.shape
        self.w = np.zeros(n)
        self.b = 0

    #Update equation for the weights and bias using gradient descent.
    def gradient_descent(self, X, y):

        y_ = np.where(y <= 0, -1, 1)
        for i, x in enumerate(X):
            if y_[i] * (np.dot(x, self.w) - self.b) >= 1:
                dw = 2 * self.lambdaa * self.w
                db = 0
            else:
                dw = 2 * self.lambdaa * self.w - np.dot(x, y_[i])
                db = y_[i]
            self.update_parameters(dw, db)

    #Updates the weights and bias (Applying it!)
    def update_parameters(self, dw, db):

        self.w = self.w - self.lr * dw
        self.b = self.b - self.lr * db

    #Training function: Fits the SVM to the data.
    def fit(self, X, y):

        self.initialize_parameters(X)
        for i in range(self.iterations):
            self.gradient_descent(X, y)

    #Testing part: Predicts the class labels for the test data.
    def predict(self, X):

        # get the outputs
        output = np.dot(X, self.w) - self.b
        # get the signs of the labels depending on if it's greater/less than zero
        label_signs = np.sign(output)
        #set predictions to 0 if they are less than or equal to -1 else set them to 1
        predictions = np.where(label_signs <= -1, 0, 1)
        return predictions

# Computes the accuracy of a classification model.
def accuracy(y_true, y_pred):

    total_samples = len(y_true)
    correct_predictions = np.sum(y_true == y_pred)
    return (correct_predictions / total_samples)

model = SVM()
# Convert X to a pandas DataFrame (you may already have a DataFrame in your data)
X_train_df = pd.DataFrame(X_train)

# Convert the DataFrame to numeric values
X_train_numeric = X_train_df.astype(float).values

model.fit(X_train_numeric,y_train)
predictions = model.predict(X_test)

accuracy(y_test, predictions)

"""# Lets see if there is a huge difference between the built in library or the mannual one."""

#Sklearn Implementation
from sklearn.svm import SVC
skmodel = SVC()
skmodel.fit(X_train, y_train)
sk_predictions = skmodel.predict(X_test)

accuracy(y_test, sk_predictions)