from flask import Flask
import pandas as pd

app = Flask(__name__)

df = pd.read_csv(r"C:\Users\kartik_patel\Downloads\EmployeeFinalData.csv")
print(df)
print(df[['Name','EQ']])

@app.route('/')
def hello_mitr():
    """This function will be executed when the server is started.
    """
    return "Welcome MITR!"

@app.get('/top_list_of_employees/<string:bu>/<string:loc>')
def get_top_list_of_employees(bu: str,loc: str):
    df2 = df.copy()
    if bu != "All":
        df2=df2[df2["BU"]==bu]
    if loc != "All":
        df2=df2[df2["Location"]==loc]
    df2=df2[df2["stresslevel"]=='Depressed']
    df2 = df2[['Name', 'EmailID', 'Location', 'DU', 'BU', 'Project', 'EQ', 'stresslevel']]
    print(df2.reset_index().to_json())
    return df2.reset_index().to_json(orient = 'records')

@app.get('/distribution_of_employees/<string:bu>/<string:loc>')
def get_distribution_of_employees(bu: str,loc: str):
    df2 = df.copy()
    if bu != "All":
        df2=df2[df2["BU"]==bu]
    if loc != "All":
        df2=df2[df2["Location"]==loc]
    df2 = df2[["EmailID", "stresslevel"]].groupby("stresslevel").count()
    df2=df2.reset_index()
    df2.rename(columns={'EmailID':'Count'}, inplace = True)
    return df2.to_json(orient = 'records')

@app.get('/get_distribution_params/<string:params>')
def get_distribution_param(params: str):
    df2 = df.copy()
    df2 = df2[df2["stresslevel"] == "Depressed"][["EmailID", params]].groupby(params).count().reset_index()
    return df2.to_json(orient = 'records')

@app.get('/top_depressed_projects')
def get_top_depressed_projects():
    df2 = df.copy()
    df2 = df2[["EQ","Project"]].groupby("Project").mean().reset_index().sort_values('EQ', ascending=True).head(10)
    return df2.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)