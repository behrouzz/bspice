from hypatie.catalogues import Catalogue

cat = Catalogue(name='hipparcos', where='Vmag < 3', n_max=1000)
df, meta = cat.download()

df = df[['HIP', '_RA_icrs', '_DE_icrs', 'Vmag', 'Plx']]
df.set_index('HIP').to_csv('hip3.csv')
