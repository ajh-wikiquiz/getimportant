# getimportant
Returns important phrases from the text by rank in descending order.  
Uses spacy and pytextrank.

This is intended to be deployed as a web service.  
Try it out here:  
    - GET https://getimportant.herokuapp.com/phrases?text=%22This%20is%20just%20a%20test.%22  
    - GET https://getimportant.herokuapp.com/phrases/%22This%20is%20just%20a%20test.%22  
    - POST https://getimportant.herokuapp.com/phrases  
    - https://getimportant.herokuapp.com/graphql


### Example POST JSON input
```
{
    "text": "A pet door is found to be convenient by many owners of companion animals, especially dogs and cats, because it lets the pets come and go as they please, reducing the need for pet-owners to let or take the pet outside manually, and curtailing unwanted behaviour such as loud vocalisation to be let outside, scratching on doors or walls, and (especially in the case of dogs) excreting in the house. They also help to ensure that a pet left outdoors can safely get back into the house in the case of inclement weather."
}
```


### Example output
```
{
    "data": {
        "phrases": [
            {
                "text": "inclement weather",
                "rank": 0.145819857298919,
                "count": 1,
                "sentences": [
                    "They also help to ensure that a pet left outdoors can safely get back into the house in the case of inclement weather.\""
                ]
            },
            {
                "text": "many owners",
                "rank": 0.11241158515844514,
                "count": 1,
                "sentences": [
                    "\"A pet door is found to be convenient by many owners of companion animals, especially dogs and cats, because it lets the pets come and go as they please, reducing the need for pet-owners to let or take the pet outside manually, and curtailing unwanted behaviour such as loud vocalisation to be let outside, scratching on doors or walls, and (especially in the case of dogs) excreting in the house."
                ]
            },
            ...
        ]
    },
}
```
