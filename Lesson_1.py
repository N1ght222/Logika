import pandas as pd
df = pd.read_csv('titanic.csv')
print(df.head())
print(df.groupby(by = 'Sex')['Survived'].mean())
print(df.pivot_table(index = 'Survived', columns = 'Pclass', values = 'Age', aggfunc = 'mean'))
df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'],axis = 1, inplace = True)
print(df['Embarked'].value_counts())
print(df['Embarked'].value_counts())
df['Embarked'].fillna('S', inplace = True)
df['Embarked'].fillna('S', inplace = True)
print(df.groupby(by = 'Pclass')['Age'].median())
age_1 = df[df['Pclass'] == 1]['Age'].median()
age_2 = df[df['Pclass'] == 2]['Age'].median()
age_3 = df[df['Pclass'] == 3]['Age'].median()
df.info()
def fill_age(row):
    if pd.isnull(row['Age']):
        if row['Pclass'] == 1:
            return age_1
        if row['Pclass'] == 2:
            return age_2
        return age_3
    return row['Age']
df['Age'] = df.apply(fill_age, axis = 1)

def fill_gender(gender):
    if gender == 'male':
        return 1
    return 0

df['Sex'] = df['Sex'].apply(fill_gender)
df.info()
print(pd.get_dummies(df['Embarked']))
df[list(pd.get_dummies(df['Embarked']).columns)] = pd.get_dummies(df['Embarked'])
df.drop('Embarked', axis = 1, inplace = True)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
df.info()
