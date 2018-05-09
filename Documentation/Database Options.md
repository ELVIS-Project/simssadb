# Database Options

## PostgreSQL

* Relational database
* [Link](https://www.postgresql.org)

### Pros

* Mature and established technology
* We already use it for ELVIS 1.0
* Works well with Django
  * [PostgreSQL and Django](https://docs.djangoproject.com/en/2.0/ref/databases/)
* SQL is nearly universal
  * Many in the project are familiar with it
* Simple queries are easy to write and fast
* Free and Open Source
* Enforces model integrity
* ACID support

### Cons

* Rigid data schema
  * Not as easy to change the schema for entities
* Certain relationships are harder to model
* Searches that are deep (i.e. many joins) are a harder to do, both in terms of writing and in terms of speed (but I don't think speed is a focus for us right now)

## Neo4J

* Graph database
* [Link](https://neo4j.com)

### Pros

* Flexible
  * Does not impose any structure on the data
  * Easier to model sparse data
* Relationship focused
  * Queries that would be done with a ``JOIN`` in a relational database are easy to right and may run faster
    * But I don't think performance is our focus right now
* ACID support
* Powerful query language, CYPHER
* Looks to me to be a more natural fit for a Linked Data approach

### Cons

* Technology not as mature
* New to project members
* Bad for aggregations (but are we going to do lots of aggregations?)
* Not good for versioning (implications for provenance?)

## MongoDB

References

[What are the Benefits of Graph Databases in Data Warehousing?](https://sonra.io/2017/06/12/benefits-graph-databases-data-warehousing/)
[Graph Databases: Their Power and Limitations](https://link.springer.com/content/pdf/10.1007%2F978-3-319-24369-6_5.pdf)