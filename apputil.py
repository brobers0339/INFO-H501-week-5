import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')


def survival_demographics():
    ages = [0, 12, 19, 59, float('inf')]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['Age'], bins=ages, labels=labels, right=True, include_lowest=True)
    df['age_group'] = df['age_group'].astype('category')

    df_grouped = df.groupby(['Pclass', 'Sex', 'age_group']).agg(
        n_passengers = ('PassengerId', 'count'),
        n_survivors = ('Survived', 'sum')
    )
    df_grouped['survival_rate'] = df_grouped['n_survivors'] / df_grouped['n_passengers']
    return df_grouped

def family_groups():
    df['family_size'] = df['Parch'] + df['SibSp'] + 1
    family_grouped = df.groupby(['Pclass', 'family_size']).agg(
        n_passengers = ('PassengerId', 'count'),
        avg_fare = ('Fare', 'mean'),
        min_fare = ('Fare', 'min'),
        max_fare = ('Fare', 'max')
    )
    return family_grouped

def last_names():
    last_names = df['Name'].str.split(',', expand=True)[0].str.strip()
    return last_names.value_counts()


