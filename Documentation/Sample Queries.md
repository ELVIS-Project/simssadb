# Sample Queries

Get me the movements of all the pieces written by P. de la Rue which have both a XML file and an image

## SQL

```SQL
select composer, musicalwork.title, section.title as movement, image.file_name, symbolicmusic.file_name from musicalwork
inner join sectioninwork on musicalwork.id = sectioninwork.work_id
inner join instanceofsection on instanceofsection.section_id = sectioninwork.section_id
inner join symbolicmusic on symbolicmusic.musical_instance_id = instanceofsection.instance_id
inner join image on image.musical_instance_id = instanceofsection.instance_id
inner join section on section.id = sectioninwork.section_id
where symbolicmusic.file_type = '.xml' and composer = 'P. de la Rue'
```

## CYPHER

```java
match (c:Composer {name:'P. de la Rue'})-[:COMPOSED]->(w:MusicalWork)
<-[:PART_OF]-(s:Section)<-[:INSTANCE_OF]-(i:MusicalInstance)
<-[MANIFESTATION_OF]-(f:SymbolicMusic {file_type: '.xml'})
match (i)<-[:MANIFESTS]-(a:Image)
return c,w,s,i,f,a
```
