import plotly.express as px
import pandas as pd

def survival_demographics():
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
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

