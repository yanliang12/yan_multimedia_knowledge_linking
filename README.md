# Jessica's Knowledge Linking Engine

```bash
docker pull gaoyuanliang/jessica_knowledge_linking:1.0.1

docker run -it \
-m 10g \
-v /Users/liangyu/Downloads/:/Downloads/ \
-p 4643:4643 \
-p 6781:6781 \
-p 9375:9000 \
gaoyuanliang/jessica_knowledge_linking:1.0.1
```

## input 

http://0.0.0.0:9375/

```python

{
"text": "I live in Abu Dhabi but study in Dubai."
}

{
"document_path":[
"/jessica_text.txt",
"/jessica_voice.mp3",
"/jessica_etisalat.jpeg",	
"/jessica_dubai_photo.jpg"]
}
```

## output

http://0.0.0.0:4643/browser/

password: neo4j1

## contact

I am opent for a data scientist/AI engineer job at UAE. Contact me by gaoyuanliang@outlook.com
