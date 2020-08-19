from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))


QUERY = """
MATCH (a:Author)-[:writes]->(p:Paper), (p:Paper)-[r:isCited]->(:Paper)
WITH a.name AS author, p.title AS title, COUNT(r) AS numCitations ORDER BY numCitations DESC
WITH author, collect({title:title, numCitations:numCitations}) AS papers
WITH author, [i IN RANGE(1, SIZE(papers)) | CASE WHEN i > papers[i-1]["numCitations"] THEN papers[i-1]["numCitations"] ELSE i END] AS list
RETURN author, REDUCE(h = 0, x IN list | CASE WHEN h < x THEN x ELSE h END) AS hindex
"""

with driver.session() as session:
    result = session.run(QUERY)

for record in result:
    print(record["author"], record["hindex"])

driver.close()
