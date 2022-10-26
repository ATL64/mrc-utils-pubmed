import asn1
from google.cloud import storage

#x = asn1.parse("pubmed_data_2017_3_num_80000.txt")
#print(len(x))

storage_client = storage.Client()
blobs = storage_client.list_blobs('your_bucket')

# Modify this line in order to set requirements about the file names
files = [blob.name for blob in blobs if blob.name.startswith('pubmed_data/2017')]

# Something needs to be done about the parsed data.
# Probably I will just call to_json instead of parse
for file in files:
    print(file)
    x = asn1.parse(file, from_gc=True)
    print(len(x))
    #print(x[0])
