## API

ver 0.2

### create new tweet

POST URL_BASE/create.json

**Parameters**

 - Text: Text of this tweet
 - Image: The Userimage of this Tweet
 - Name: The Username of this Tweet

**Response**

	{
		id: $id,
		url: URL_BASE/$id,
		full_text: $full_text,
		text: $text,
	}

**Note**
	
 - $id: the unique id of the piece of text
 - $url: url to get full text
 -$full_text: full text
 -$text: the striped text. The length of it shouldn't longer than 140 - len($url)

### get full tweet

GET URL_BASE/tweets/:id.json

**Parameters**

 None

**Response**

	{
		id: $id,
		url: URL_BASE/$id,
		full_text: $full_text
	}

