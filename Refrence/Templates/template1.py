import sqlalchemy as sql
import pandas as pd
eng = sql.create_engine('postgresql://postgres:password@localhost/stock_market')

# List tables 
con = eng.connect()
print(eng.table_names())


#Load Data From The Base
a=pd.read_sql_query('select * from "PW_15min"',con=eng).set_index('date')

# Add Columns If Not In Database
left_overs = set(df.columns) - set(a.columns)
print('columns in Database:',len(left_overs),left_overs)
if len(left_overs) > 0:
    for col in left_overs:
        con.execute('ALTER TABLE {} ADD COLUMN "{}" TEXT NULL;'.format(table_name,col))
        


# Save Data To Base
df.to_sql(table_name,con,if_exists = 'append', index = True)

con.close()

#Removing Duplicate Columns
#print(len(a))
#print(len(a.groupby('Text').agg('first')))
#a.groupby('Text').agg('first')