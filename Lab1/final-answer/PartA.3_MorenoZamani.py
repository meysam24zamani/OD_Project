from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

# Add new property to "reviews" relationship
# add new instances (example)
Q1 = """
MATCH (:Author)-[r:reviews]->(:Paper)
SET r.content = 'DEFAULT'
SET r.decision = 'ACCEPT'
"""

# Creating new node. 
# add new instances (example)
# Creating new relationship. 
Q2 = """CREATE (:Organization {name: "UPC"})"""
Q3 = """
MATCH (a:Author {name : "Symeon Bozapalidis"}), (o:Organization {name : "UPC"})
CREATE (o)-[:affiliates]->(a)
"""

with driver.session() as session:
    session.run(Q1)
    session.run(Q2)
    session.run(Q3)

driver.close()
