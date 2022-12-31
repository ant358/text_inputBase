[![Makefile CI process for Github](https://github.com/ant358/text_inputBase/actions/workflows/devops-github.yml/badge.svg)](https://github.com/ant358/text_inputBase/actions/workflows/devops-github.yml)

# Input Database for Text NLP projects  

Source data for the Text NLP projects, derived from wikipedia artciles.  
Held in a simple sqlite database.   
There is a single table with the article page id, title and text.  
The text is the raw text of the article.  
  
The database is desiged to run in a docker container. And to supply text data via an API.  

The data is filled by the selection of random english language wikipedia articles.  
The total number of articles can be controlled via a post request to the API.  

Other containers can request the data via the API.