### Keyword extractor

This repo contains code to 

- Train the tfidf and store it in Cloud Storage
- A module that reads this model from storage and has a function to extract keywords. 
- A vm setup to run this on Compute Engine

_To do: Use the code + new code for getting data from cloud storage and make this a proper module_

##### Keyword Train
The ````keyword_train.py```` file has code that

- Fetches 1 million abstracts from bigquery
- Trains the tfidf model
- Writes that model to disk

In order to upload to the cloud, that is in bash in the vm_setup file

_To do: Try and train this with a bigger feature vector and more abstracts, ideally the whole corpus we have in BQ if possible_

##### Keyword Extractor
The ````keyword_extractor.py```` file should be made module that we can import.
It should:

- Fetch the latest model that is stored in ````gs://biotech_lee/keyword_extractor````. This consists of two pickled files

- Contain a function that receives two arguments, text and question.  The output should be a list of keywords.
Maybe a list of tuples which contain keyword and score


 ##### VM Setup
 
 This machine is most likely a massive overkill, but it works for sure for **training**
 
 - 64CPU 240 Giga RAM
 - Zone Europe west 4 Netherlands
 - Ubuntu 18.04
 - 30 Giga Disk
 
 _To do: Try smaller machines to see what is the minimum we need. I did manual authentication, maybe do this in a better way._
 

For production, we tested the keyword_extractor on a standard 3.75G and had no problems at all.  Around 200 Mb used in python memory.


##### Examples

Some results using the huge model trained model, which is almost the same as the small one:

doc="Do idioblasts have a positive effect on the renal glands?"
- effect renal 0.692
- positive effect 0.532
- renal 0.357
- positive 0.274
- effect 0.187


doc = "Do sevoflurane and isoflurane have the same effects on the renal tubules?"
- sevoflurane 0.675
- isoflurane 0.643
- renal 0.363

 doc = "What molecule increases antibodies for HPV?"
- hpv 0.86
- molecule 0.51



##### Deployment

The CircleCi config is set up so that when we merge to master, 
the files in GCS are automatically updated to reflect the version
 in master.  However, in order for the dash-server to use this new version,
 dash-server needs to be redeployed (you can just do a dummy merge to 
 dash-server master or re run from CircleCi UI).
