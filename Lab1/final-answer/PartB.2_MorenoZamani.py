from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))


QUERY = """
MATCH (p:Paper)-[:isPresentedIn]->(c:Conference), (p:Paper)-[r:isCited]->(:Paper)
WITH p.title AS title, c.name AS conference, COUNT(r) AS numCitations ORDER BY numCitations DESC
RETURN conference, collect({title:title, numCitations:numCitations})[0..3] AS papers
"""

with driver.session() as session:
    result = session.run(QUERY)

for record in result:
    print(record["conference"], record["papers"])

driver.close()
