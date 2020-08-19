from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

QUERY = """
MATCH (p:Paper)-[:isPublishedIn]->(j:Journal)
WITH j, p, EXISTS((:Community {name:"database"})-[:definedBy]->(:Keyword)-[:isIn]->(p:Paper)) AS inCommunity
WITH j, SUM(CASE WHEN inCommunity THEN 1 ELSE 0 END) AS numPapersCommunity, COUNT(*) AS numPapers
WHERE numPapersCommunity/numPapers >= 0.9
MATCH (c:Community {name:"database"}) MERGE (j)-[:isPartOf]->(c)
"""

with driver.session() as session:
    session.run(QUERY)

driver.close()
