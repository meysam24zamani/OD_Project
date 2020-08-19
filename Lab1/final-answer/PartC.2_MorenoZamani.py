from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

QUERY = """
CALL algo.betweenness.stream('Paper','isCited',{})
YIELD nodeId, centrality
MATCH (p:Paper) WHERE id(p) = nodeId
RETURN p.title AS paper, centrality
"""

with driver.session() as session:
    result = session.run(QUERY)

for record in result:
    print(record["paper"], record["centrality"])

driver.close()
