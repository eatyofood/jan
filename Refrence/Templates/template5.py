from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
import string
import re
import cufflinks as cf
cf.go_offline(connected=False)


text = u'This is a smiley face \U0001f602'
print(text) # with emoji

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

print(deEmojify(text))

def clean_text(text):
#print(text)
    #removing numbers
    text = re.sub(r'\d+', '', text)
    # remove emojis
    text = deEmojify(text)
    #splitting word up
    text = word_tokenize(text)

    text = [l for l in text if l not in string.punctuation]
    text = [word for word in text if not word in stopwords.words('english')]
    text = ' '.join(text)
    # only collect small words
    smal = [word for word in text.split() if (2<len(word)<5)]

    return text
        
    #else:
    #    tics = []
    #return tics
df['CleanText'] = df['Text'].apply(clean_text)

#s = [l for l in text if l not in string.punctuation]
#text =[ re.sub(r'\d+', '', w) for w in s]
def extract_tickers(s):
    '''
    give me tweets i spit out a list of words with NO DIGITS that had
    hash tag "$" in the word
    '''
    
    #s = df['Text'][5]
    #print(s)
    # grab Dollars
    s = [w for w in s.split(' ') if '$' in w]
    #print(s)
    goodli = []
    for w in s:
        result = ''.join([i for i in w if not i.isdigit()])
        #print('RESULT:',result, 'WORD:',w)
        if len(w) == len(result):
            #print('====GOOD====',w)
            goodli.append(re.sub(r'\d+', '', w.replace('$','')))
        else:
            #print('====NAH====',w)



    #print(goodli)
    return goodli

