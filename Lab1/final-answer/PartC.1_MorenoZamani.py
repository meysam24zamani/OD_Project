from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

QUERY = """
MATCH (p:Paper {title:'Minimum Feedback Vertex Sets in Cocomparability Graphs and Convex Bipartite Graphs.'})
CALL algo.shortestPath.deltaStepping.stream(p,"cost",1,{nodeQuery:'Paper', relationshipQuery:'isCited', defaultValue:1.0, direction:'OUTGOING'})
YIELD nodeId, distance
MATCH (n:Paper) WHERE id(n) = nodeId AND distance < 100
RETURN n.title AS paper, distance
"""

with driver.session() as session:
    result = session.run(QUERY)

for record in result:
    print(record["paper"], record["distance"])

driver.close()
