from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))


QUERY = """
MATCH (a:Author)-[:writes]->(:Paper)-[r:isPresentedIn]->(c:Conference)
WITH c.name AS conference, a.name AS author, COUNT(DISTINCT r.edition) AS numEditions
WHERE numEditions >= 4
RETURN conference, collect(author) AS community
"""

with driver.session() as session:
    result = session.run(QUERY)

for record in result:
    print(record["conference"], record["community"])

driver.close()
