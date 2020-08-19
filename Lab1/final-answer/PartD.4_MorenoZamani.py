from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

QUERY = """
MATCH (a:Author)-[:writes]->(p:Paper {top : TRUE})
WITH a.name as author, COUNT(*) as nPaper
RETURN author, (CASE WHEN nPaper = 1 THEN "member" ELSE "guru" END) AS status
"""

with driver.session() as session:
    result = session.run(QUERY)

for record in result:
    print(record["author"], record["status"])

driver.close()
