from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

QUERY = """
MATCH (p:Paper)-[r:isCited]->(:Paper), (p:Paper)-[t:isPublishedIn]->(j:Journal)
WHERE t.year = "2013" OR t.year = "2014"
WITH p.title AS paper, j.name AS journal, COUNT(r) AS numCitations
RETURN journal, AVG(numCitations) AS ImpactFactor
"""

with driver.session() as session:
    result = session.run(QUERY)

for record in result:
    print(record["journal"], record["ImpactFactor"])

driver.close()
