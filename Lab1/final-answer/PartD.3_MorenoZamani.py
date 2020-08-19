from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

QUERY = """
CALL algo.pageRank.stream('MATCH (p:Paper)-[:isPublishedIn]->(:Journal)-[:isPartOf]->(:Community) RETURN id(p) as id',
                          'MATCH (p1:Paper)-[:isCited]->(p2:Paper) RETURN id(p1) as source, id(p2) as target',
                          {iterations:20, dampingFactor:0.85, graph:'cypher'})
YIELD nodeId, score
MATCH (p:Paper) WHERE id(p) = nodeId
WITH p, score ORDER BY score DESC LIMIT 10
SET p.top = TRUE
"""

with driver.session() as session:
    result = session.run(QUERY)

driver.close()
