import pandas as pd
import numpy as np
import pandas_ta as pta
import os

import sqlalchemy as sql
import pandas as pd
eng = sql.create_engine('postgresql://postgres:password@localhost/stock_market')

# List tables 
con = eng.connect()
table_df = pd.DataFrame(eng.table_names())
#print(table_df)



dailys = [table for table in eng.table_names() if '1d' in table]
print(dailys)

table_name = dailys[2] # this will become a loop
#Load Data From The Base
df=pd.read_sql_query('select * from "{}"'.format(table_name),con=eng).set_index('date')
df

from finding_fire import jenay

jenay(df)

# Pull Weekly Time Frame Out

from finding_fire import monthly_pull,monthly_push,weekly_pull,weekly_push,jenay

#pull weekly out of daily
wdf = weekly_pull(df)


jenay(wdf)

### Now We Can Add Some Weekly Indicators

from finding_fire import sola

import cufflinks as cf
cf.go_offline(connected=False)

wdf['rsi'] = pta.rsi(wdf.close)
sola(wdf[['rsi']])

### Mix It Back With The Daily Data Frame

df = weekly_push(df,wdf)
jenay(df,line_one='week_high',line_two='week_low')

# Now Let's Add The Monthly Time Frame

from finding_fire import monthly_pull

mdf = monthly_pull(df)
jenay(mdf)

pd.set_option('display.max_columns',None)

mdf['rsi'] = pta.rsi(mdf.close)

### And Mix It Back With The Daily Time Frame

df = monthly_push(df,mdf)

from finding_fire import scale

sola(scale(df[['high','low','week_low','week_high','month_low','month_high']]))
sola(df[['high','low','week_low','week_high','month_low','month_high']])

# Structuring An Algo With Time Frames

### Telescope - algo first time daily-RSI is above weekly-RSI which is above monthly-RSI

df['rsi'] = pta.rsi(df.close)
df['rsi_telescope'] = (df['rsi'] > df['week_rsi']) & (df['week_rsi']> df['month_rsi'])
df['buy'] = (df['rsi_telescope'].shift()== False) & (df['rsi_telescope']== True)
jenay(df,scale_one='buy')

sola(df[['rsi','week_rsi','month_rsi']])

from finding_fire import one_stop,vally_stop,pct_targets

results = []

# copy and paste this to send it to the refrence database
strat = 'First-RSI-Telescop'
target_type = 'percent'
UP,DN = 50,25
ups = [5,15,25,50,75,100]
dns = [5,10,20,30,40]
for UP in ups:
    for DN in dns:
        strat_name = strat + 'UP_PCT:' + str(UP)+'DN_PCT:' + str(DN)
        pct_targets(df,up_pct = UP,dn_pct=DN)
        result = one_stop(df,strat_name=strat_name)
        result['up_target'] = UP
        result['dn_target'] = DN
        result['target_type'] = target_type
        result['data']        = table_name
        results.append(result)

### NOTES: i would like to add tranches to this strat
- i think it would preform well if there was a requirement for 10ma to dip below 50ma and turn around ( 'positive delta' ) 
    - or use this as a second tranche

rdf = pd.concat(results)
rdf

rdf['data'] = table_name

rdf

print(strat)

rdf = rdf.set_index('strat_name')
rdf

rdf.sort_values('final_pnl')[['final_pnl','win_pct']].iplot(theme='solar',kind='bar')

description = '''
When Daily-Weekly-Monthly RSI's are all above each others last close for the first time buy

'''
notes = '''### NOTES: i would like to add tranches to this strat
- i think it would preform well if there was a requirement for 10ma to dip below 50ma and turn around ( 'positive delta' ) 
    - or use this as a second tranche

'''


up_targets = ups
dn_targets = dns
target_type= 'percent'
report_path= ''


table_name

from datetime import datetime

refrence = dict(strat = 'First-RSI-Telescop',
target_type = 'percent',
data       = table_name,
ups = [5,15,25,50,75,100],
dns = [5,10,20,30,40],
notes = notes,
               report_path = '/Research/ProjectReports/First-RSI-Telescope.ipynb',
               description = description,
               test_date   = datetime.now(),
               results     = rdf.index)


refrence_df = pd.DataFrame([refrence])
refrence_df

import sqlalchemy as sql
import pandas as pd

database = 'research'
eng = sql.create_engine('postgresql://postgres:password@localhost/{}'.format(database))

# List tables 
con    = eng.connect()
tables = eng.table_names()
tdf    = pd.DataFrame(tables)
print(tdf)

table_name = 'backtests'

#Load Data From The Base
a=pd.read_sql_query('select * from "{}"'.format(table_name),con=eng).set_index('date')

# Add Columns If Not In Database
left_overs = set(rdf.columns) - set(a.columns)
print('columns in Database:',len(left_overs),left_overs)
if len(left_overs) > 0:
    for col in left_overs:
        con.execute('ALTER TABLE {} ADD COLUMN "{}" TEXT NULL;'.format(table_name,col))
                        
                    
                    
# Save Data To Base
rdf.to_sql(table_name,con,if_exists = 'append', index = True)

                    
                    #Removing Duplicate Columns
                    #print(len(a))
                    #print(len(a.groupby('Text').agg('first')))
                    #a.groupby('Text').agg('first')

eng = sql.create_engine('postgresql://postgres:password@localhost/{}'.format(database))
table_name = 'logs'



#Load Data From The Base
a=pd.read_sql_query('select * from "{}"'.format(table_name),con=eng).set_index('date')

# Add Columns If Not In Database
left_overs = set(refrence_df.columns) - set(a.columns)
print('columns in Database:',len(left_overs),left_overs)
if len(left_overs) > 0:
    for col in left_overs:
        con.execute('ALTER TABLE {} ADD COLUMN "{}" TEXT NULL;'.format(table_name,col))
                        
                    
                    
# Save Data To Base
refrence_df.to_sql(table_name,con,if_exists = 'append', index = True)
con.close()

# Plot A Grid Map

from finding_fire import grid_map

gdf = grid_map(rdf,'up_target','dn_target')


UP,DN = 75,40

strat_name = strat + 'UP_PCT:' + str(UP)+'DN_PCT:' + str(DN)
pct_targets(df,up_pct = UP,dn_pct=DN)
result = one_stop(df,strat_name=strat_name,plot=True)
result['up_target'] = UP
result['dn_target'] = DN
result['target_type'] = target_type
result['data']        = table_name
results.append(result)
