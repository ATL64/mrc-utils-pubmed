# File-parsers

This repository contains the parsers used for the Biotech-MRC project.

Since the pubmed data is available in asn1 format, currently we have a parser capable of converting an asn1 file into a json file.
To convert a file from asn1 into json, the following command needs to be executed:

```
import asn1
asn1.to_json(input_file_path, output_file_path=None, from_gc=False, input_bucket=None)
```

Note that the json format of the output file will be 1-line json. See the help text of the function for further details on the optional parameters.

Other functions available from the asn1 module are:
- `get_abstracts(input_file)`. Returns a dictionary whose keys are the pmids of the pubmed entries in input_file, and the values are the corresponding abstracts.
- `parse(input_file, file_path, from_gc=False, input_bucket=None)`. Returns a python list of dictionaries. Each dictionary contains all the data of a pubmed entry.
