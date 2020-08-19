from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

with driver.session() as session:
    session.run("""MERGE (c:Community {name:"database"})""")
    session.run("""MATCH (k:Keyword {name:"sequence alignment"}), (c:Community {name:"database"}) MERGE (c)-[:definedBy]->(k)""")
    session.run("""MATCH (k:Keyword {name:"Machine Learning"}), (c:Community {name:"database"}) MERGE (c)-[:definedBy]->(k)""")
    session.run("""MATCH (k:Keyword {name:"Service and cloud computing"}), (c:Community {name:"database"}) MERGE (c)-[:definedBy]->(k)""")
    session.run("""MATCH (k:Keyword {name:"Computational Video"}), (c:Community {name:"database"}) MERGE (c)-[:definedBy]->(k)""")
    session.run("""MATCH (k:Keyword {name:"type theory"}), (c:Community {name:"database"}) MERGE (c)-[:definedBy]->(k)""")
    session.run("""MATCH (k:Keyword {name:"Deep learning"}), (c:Community {name:"database"}) MERGE (c)-[:definedBy]->(k)""")
    session.run("""MATCH (k:Keyword {name:"Energy lab"}), (c:Community {name:"database"}) MERGE (c)-[:definedBy]->(k)""")

driver.close()
