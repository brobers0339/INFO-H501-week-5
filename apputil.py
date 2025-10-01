import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')


def survival_demographics():
    """
    Analyze survival patterns on the Titanic 
    by passenger class, sex, and age group.

    Returns:
        Pandas DataFrame 
            grouped by 'Pclass', 'Sex', and 'age_group'
            with columns: 'n_passengers', 'n_survivors', and 'survival_rate'.
    """
    ages = [0, 12, 19, 59, float('inf')]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['Age'], bins=ages, labels=labels, right=True, include_lowest=True)
    df['age_group'] = df['age_group'].astype('category')

    age_grouped = df.groupby(['Pclass', 'Sex', 'age_group']).agg(
        n_passengers = ('PassengerId', 'count'),
        n_survivors = ('Survived', 'sum')
    ).reset_index()
    age_grouped['survival_rate'] = age_grouped['n_survivors'] / age_grouped['n_passengers']
    return age_grouped

def visualize_demographic():
    """
    Visualize survival patterns found in the above function (survival_demographics).

    Returns:
        Two plotly visualizations to visualize:
            survival rate by class of adult and teen women,
            survival rate by class of all children (male and female).
    """
    grouped_df = survival_demographics()
    women_filtered = grouped_df[
        (grouped_df['Sex'] == 'female') & (grouped_df['age_group'].isin(['Teen','Adult']))
    ]
    #For answering this question, we will be using "women" as adult and teen females. Children will be any gender child. 
    women_fig = px.bar(women_filtered, 
                       x='Pclass', 
                       y='survival_rate',
                       color= 'age_group',
                       barmode= 'group',
                       title= 'Survival Rate for Adult and Teen Women by Class'
    )

    women_fig.show()

    children_filtered = grouped_df[
        (grouped_df['age_group'] == 'Child')
    ]

    children_fig = px.bar(children_filtered,
                          x= 'Pclass',
                          y= 'survival_rate',
                          color= 'Sex',
                          barmode= 'group',
                          title= 'Survival Rate for All Children by Class'
    )

    children_fig.show()


def family_groups():
    """
    Analyze family size patterns on the Titanic 
    by passenger class and a calculate family size.
    Family size is calculated by adding parents, children, siblings,
    spouse, and themselves before adding the value to the dataset in a column.

    Returns:
        Pandas DataFrame 
            grouped by 'Pclass' and 'family_size'
            with columns: 'n_passengers', 'avg_fare', 'min_fare', and 'max_fare'.
    """
    df['family_size'] = df['Parch'] + df['SibSp'] + 1
    family_grouped = df.groupby(['Pclass', 'family_size']).agg(
        n_passengers = ('PassengerId', 'count'),
        avg_fare = ('Fare', 'mean'),
        min_fare = ('Fare', 'min'),
        max_fare = ('Fare', 'max'),
    ).reset_index()
    return family_grouped


def last_names():
    """
    List all of the last_names in the Titanic dataset
    and determine the count of instances for that last name.

    Returns:
        Pandas Series 
            keys are the last names in the dataset,
            values are the counts of instances of the last name.
    """
    last_names = df['Name'].str.split(',', expand=True)[0].str.strip()
    return last_names.value_counts()

#No, the table above and last name table do not agree with one another.
#We can see from one of the first listings shows a family value of 9, 
#but we can't see that value displayed in the table, meaning there are some discrepencies.

def visualize_families():
    """
    Visualize family size patterns found in the above function (family_groups).

    Returns:
        A plotly visualization to visualize:
            average family size sorted by class.
    """
    mean_class_family_size = family_groups().groupby('Pclass')['family_size'].mean().reset_index()
    family_size_fig = px.bar(mean_class_family_size, 
                       x='Pclass', 
                       y='family_size',
                       title= 'Average Family Size by Class'
    )

    family_size_fig.show()
