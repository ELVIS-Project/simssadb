# Database Options

## PostgreSQL

* Relational database
* [Link](https://www.postgresql.org)
* Queried using SQL or an Object Relational Mapping (ORM) layer in Python/Django

### Pros

* Free and Open Source
* Mature and established technology
* We already use it for ELVIS 1.0
* Works well with Django
* SQL is nearly universal
  * Many in the project are familiar with it
* Simple queries are easy to write and fast
* Easier to enforce model integrity
* ACID support

### Cons

* Rigid data schema
  * Not as easy to change the schema for entities or to add new relationships
* Certain relationships are harder to model
* Searches that are deep (i.e. many joins) are a harder to do, both in terms of writing and in terms of speed (but I don't think speed is a focus for us right now)

## Neo4J

* Graph database
* [Link](https://neo4j.com)
* Queried using Cypher or an Object Graph Mapper (OGM) layer in Python/Django

### Pros

* Flexible
  * Does not impose any structure on the data
  * Easier to model sparse data
* Relationship focused
  * Queries that would be done with a ``JOIN`` in a relational database are easy to write
* ACID support
* Powerful query language, CYPHER
* Looks to me to be a more natural fit for a Linked Data approach
* Easy to create interesting and intuitive data visualizations

### Cons

* Technology not as mature
* New to project members
* Bad for aggregations (but are we going to do lots of aggregations?)
* Not good for versioning (implications for provenance?)
* Enterprise license is paid

## Sample Queries

Get me the movements of all the pieces written by P. de la Rue which have both a XML file and an image

### SQL

```SQL
select composer, musicalwork.title, section.title as movement, image.file_name, symbolicmusic.file_name from musicalwork

inner join sectioninwork on musicalwork.id = sectioninwork.work_id
inner join instanceofsection on instanceofsection.section_id = sectioninwork.section_id
inner join symbolicmusic on symbolicmusic.musical_instance_id = instanceofsection.instance_id
inner join image on image.musical_instance_id = instanceofsection.instance_id
inner join section on section.id = sectioninwork.section_id

where symbolicmusic.file_type = '.xml' and composer = 'P. de la Rue'
```

## Cypher

```java
match (composer:Composer {name:'P. de la Rue'})
  -[:COMPOSED]->(work:MusicalWork)
  <-[:PART_OF]-(section:Section)<-[:INSTANCE_OF]-(instance:MusicalInstance)
  <-[MANIFESTS]-(symb:SymbolicMusic {file_type: '.xml'})

match (instance)<-[:MANIFESTS]-(image:Image)
return composer, work, section, instance, symb, image
```

## Other Graph Databases

* AgensGraph
  * This one is very interesting
  * Multi-model supporting both graph and relational models as well as storing attributes as JSON
  * Can be queried using both Cypher and SQL
* ArangoDB (multi-model)

[What are the Benefits of Graph Databases in Data Warehousing?](https://sonra.io/2017/06/12/benefits-graph-databases-data-warehousing/)
[Graph Databases: Their Power and Limitations](https://link.springer.com/content/pdf/10.1007%2F978-3-319-24369-6_5.pdf)