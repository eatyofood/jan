
SAVE_PATH = ''
SAVE_NAME = SAVE_PATH + ' '
# Save it...
# create directory if first time
if not os.path.exists(SAVE_PATH):
os.mkdir(SAVE_PATH)

# append file or create it
if not os.path.exists():
df.to_csv(save_name)
print('first_copy saved')
else:
# load old data
odf = pd.read_csv(save_name).set_index('Date')
# append
ndf = odf.append(df)
# save
ndf.to_csv(save_name)
print('appended')




