# API_KEY = 'DBBAC9ECDD'
import requests
# text = "first term married put your name you Stephen Lawson a with respect to o all right that's the velocity at this point in this frame right all right what else do we need put your name Andre yeah here a velocity of B with respect to K and what is that is that influenced by rotation can you describe what you mean by the velocity of B na physically so as if you were stationing sitting in on that frame right does a rotation have anything to do with what you see no so this is I sometimes to remind myself right here this is omega equals zero and you can just set that mega equal to zero what you would see is the it's what this term is do we need anything more named Christine let's deduce it if my my arm here this is the first arm and this is that a B link okay now if Omega with respect to this arm this thing weren't moving with there's no rotation rate relative thisthe thing whole thing would be straight"
import requests
import json

# Your long text goes here...
text = """    "answers": [
        "first term married put your name you\nStephen Lawson a with respect to o all\nright that's the velocity at this point\nin this frame right all right what else\ndo we need\nput your name Andre yeah here a velocity\nof B with respect to K and what is that\nis that influenced by rotation can you\ndescribe what you mean by the velocity\nof B na physically so as if you were\nstationing sitting in on that frame\nright does a rotation have anything to\ndo with what you see no so this is I\nsometimes to remind myself right here\nthis is omega equals zero and you can\njust set that mega equal to zero what\nyou would see is the it's what this term\nis\ndo we need anything more named Christine",
        "let's deduce it if my my arm here this\nis the first arm and this is that a B\nlink okay now if Omega with respect to\nthis arm this thing weren't moving with\nthere's no rotation rate relative this\nthe thing whole thing would be straight\nright and it's going around like this\nwhat's the rotation rate of the link out\nhere Omega one okay and now this arms\nnot moving but this is rotating relative\nto it at Omega 2 what's the rotation\nrate of the link out here just to make\nit 2 if I put the two together what is\nthe rotation rate of this arm the second\nlink right Omega 1 in certainly in O\nplus Omega 2 it's not with respect to a\nI'm just going to call it with respect",
        "to the are maybe even this notation is\nfailing a little bit but you get what I\nmean it's Omega 1 plus Omega 2 and let's\njust write it as Omega 1 plus Omega 2\nand what direction is it in it's a\nvector so one of the things we have to\npay attention to our unit vectors yeah\nyeah so this has got a capital I hat\nhere and a capital J hat there and\ncoming out of the board okay right\nnow this is certainly a hat capital K\nhat this one knows relative to its the\nrotation rate of this thing here is a\nreference frame what's sticking out this\nway a little k2 right but is it is it\nparallel to capital K always parallel to\ncapital K correct so they're the same\nthing\nif unit vectors in the parallel they",
        "this over here we have a velocity of a\nin\nand we have the velocity of B in a with\nno rotation and we have Omega B and O\nand let's finish that we know what Omega\nis now the whoops is not Omega it's a\nthird term is omega BN o across R b/a so\nnow we've gotten the first bit of this\nlet's finish the problem this is Omega 1\nplus Omega 2 times K hat cross with what\nwe need a length I'll call this l-l-long\nso what is our B with respect to a yes L\nX 2 hat and I'll call that lj2\nthe coordinate is X 2 the unit vector\nwould be I 2 right not a J and I so the\nunit vector is I 2\nokay great now what is K cross I 2\nthank you so we get Omega L Omega 1 plus\nOmega 2 J 2 hat that's that term and we"
"""

# Define the API endpoint
url = "https://api.smmry.com/&SM_API_KEY=DBBAC9ECDD"

# Define the headers
headers = {
    "Expect": "",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Define the data
data = {
    "sm_api_input": text
}

# Send the POST request
response = requests.post(url, headers=headers, data=data)

# Parse the JSON response
return_data = json.loads(response.text)

# Print the return data
print(return_data)
