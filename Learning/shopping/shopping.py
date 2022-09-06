import csv
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    df = pd.read_csv (filename)
    df["Weekend"]=df[["Weekend"]].astype(int)
    df["Revenue"]=df[["Revenue"]].astype(int)
    df.loc[df['Month'] == "Jan", 'Month'] = 0
    df.loc[df['Month'] == "Feb", 'Month'] = 1
    df.loc[df['Month'] == "Mar", 'Month'] = 2
    df.loc[df['Month'] == "Apr", 'Month'] = 3
    df.loc[df['Month'] == "May", 'Month'] = 4
    df.loc[df['Month'] == "June", 'Month'] = 5
    df.loc[df['Month'] == "Jul", 'Month'] = 6
    df.loc[df['Month'] == "Aug", 'Month'] = 7
    df.loc[df['Month'] == "Sep", 'Month'] = 8
    df.loc[df['Month'] == "Oct", 'Month'] = 9
    df.loc[df['Month'] == "Nov", 'Month'] = 10
    df.loc[df['Month'] == "Dec", 'Month'] = 11
    df['VisitorType'] = (df.VisitorType == 'Returning_Visitor').astype(int)
    df["Month"]=df["Month"].astype(int)
    df["VisitorType"]=df["VisitorType"].astype(int)
    edf=df.iloc[:, 0:17]
    ldf=df.iloc[:, 17]
    evidence=edf.values.tolist()
    labels=ldf.values.tolist()
    return evidence,labels

def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    sump=0
    sumpt=0
    sumnt=0
    sumn=0
    for i in range(len(labels)):
        if predictions[i]==1:
            if labels[i]==predictions[i]:
                sump=sump+1
            sumpt=sumpt+1
            
        elif predictions[i]==0:
            if labels[i]==predictions[i]:
                sumn=sumn+1
            sumnt=sumnt+1
    return sump/sumpt,sumn/sumnt


if __name__ == "__main__":
    main()
