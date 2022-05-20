files = os.listdir('data/dansk_statistik/')
#print(files)

dfs = []

for file in files:

    df = pd.read_excel('/home/nadia/Documents/master/second_semester/geospatial/exam/data/dansk_statistik/{}'.format(file)) #, skiprows=[0,1,108,109]

    remove = []

    for kommune in df['Unnamed: 0']:
        if kommune not in kommuner:
            remove.append(kommune)

    for kommune in kommuner:
        if kommune not in df['Unnamed: 0'].values:
            df.loc[len(df.index)] = [kommune] + [np.nan for x in range(len(df.columns)-1)]

    df = df[~df['Unnamed: 0'].isin(remove)]

    df.sort_values(by=['Unnamed: 0'], inplace=True)
    df = df.drop(['Unnamed: 0'], axis=1)

    df.columns = [''.join(file.split('.')[0]) + '_' + col for col in df.columns]

    df.reset_index(drop=True, inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    dfs.append(df)

df = pd.concat(dfs, axis=1)

for col in df.columns:
    if 'antal' in col and 'folketal' not in col and int(col.split('_')[-1]) >= 2010 and int(col.split('_')[-1]) <= 2021:
        #print(df[col])
        df[col] = df[col].replace('..', np.nan)
        df['norm_' + col] = df[col].astype(float) / df['folketal_antal_{}'.format(col.split('_')[-1])]
        #make the column an int
    #elif 'antal' in col and 'folketal' not in col:
        #df = df.drop([col], axis=1)

final_df = pd.read_csv("data/danish_diseases_socio.csv")

final_df = pd.concat([final_df, df], axis=1)
#print(final_df)

print(final_df)

final_df.to_csv('data/final_data.csv', index=False)