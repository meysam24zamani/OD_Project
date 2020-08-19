from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j","admin"))

# remove previous data
with driver.session() as session:
    result = session.run("MATCH (n) DETACH DELETE n")



# Create metadata
with driver.session() as session:
    session.run("CREATE (:MetaAuthor {name: '', nationality: '', age: '', email: ''})")
    session.run("CREATE (:MetaPaper {title: '', ISBN: '', pages: '', DOI: ''})")
    session.run("CREATE (:MetaKeyword {name : ''})")
    session.run("CREATE (:MetaJournal {name : ''})")
    session.run("CREATE (:MetaConference {name : ''})")
    session.run("MATCH (a:MetaAuthor {name : ''}), (p:MetaPaper {title : ''}) CREATE (a)-[:writes]->(p)")
    session.run("MATCH (a:MetaAuthor {name : ''}), (p:MetaPaper {title : ''}) CREATE (a)-[:reviews]->(p)")
    session.run("MATCH (p:MetaPaper {title : ''}) CREATE (p)-[:isCited]->(p)")
    session.run("MATCH (k:MetaKeyword {name : ''}), (p:MetaPaper {title : ''}) CREATE (k)-[:isIn]->(p)")
    session.run("MATCH (c:MetaConference {name : ''}), (p:MetaPaper {title : ''}) CREATE (p)-[:isPresentedIn {edition: '', location: ''}]->(c)")
    session.run("MATCH (j:MetaJournal {name : ''}), (p:MetaPaper {title : ''}) CREATE (p)-[:isPublishedIn {year: '', volume: ''}]->(j)")


# Load Journal-Dataset
with driver.session() as session:
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row CREATE (:Author { name: row.AuthorName, nationality: row.Nationality, age: row.Age, email: row.email})")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row CREATE (:Paper { title: row.ArticleTitle, ISBN: row.ISBN, pages: row.Npages, DOI: row.DOI})")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row CREATE (:Journal { name: row.JournalName})")            
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (a:Author { name : row.AuthorName}), (p:Paper { title: row.ArticleTitle}) CREATE (a)-[:writes]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (a:Author { name : row.AuthorName}), (p:Paper { title: row.ArticleTitle}) CREATE (a)-[:reviews]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (p1:Paper { title : row.ArticleTitle}), (p2:Paper { title : row.ArticleTitle}) CREATE (p1)-[:isCited]->(p2)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (p:Paper { title : row.ArticleTitle}), (j:Journal { name : row.JournalName}) CREATE (p)-[:isPublishedIn{ year: row.YearPublished, volume: row.Volume}]->(j)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row CREATE (k:Keyword {name : row.keyword1})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row CREATE (k:Keyword {name : row.keyword2})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row CREATE (k:Keyword {name : row.keyword3})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row CREATE (k:Keyword {name : row.keyword4})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (k:Keyword {name : row.keyword1}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (k:Keyword {name : row.keyword2}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (k:Keyword {name : row.keyword3}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-journal.csv\' AS row MATCH (k:Keyword {name : row.keyword4}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")    

## Load Conference-Dataset
with driver.session() as session:
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row CREATE (:Author { name: row.AuthorName, nationality: row.Nationality, age: row.Age, email: row.email})")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row CREATE (:Paper { title: row.ArticleTitle, ISBN: row.ISBN, pages: row.Npages, DOI: row.DOI})")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row CREATE (:Conference { name: row.ConferenceName})")          
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (a:Author { name : row.AuthorName}), (p:Paper { title: row.ArticleTitle}) CREATE (a)-[:writes]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (a:Author { name : row.AuthorName}), (p:Paper { title: row.ArticleTitle}) CREATE (a)-[:reviews]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (p1:Paper { title : row.ArticleTitle}), (p2:Paper { title : row.ArticleTitle}) CREATE (p1)-[:isCited]->(p2)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (p:Paper { title : row.ArticleTitle}), (c:Conference { name : row.ConferenceName}) CREATE (p)-[:isPresentedIn{ edition: row.Edition, location: row.Location}]->(c)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row CREATE (k:Keyword {name : row.keyword1})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row CREATE (k:Keyword {name : row.keyword2})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row CREATE (k:Keyword {name : row.keyword3})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row CREATE (k:Keyword {name : row.keyword4})") 
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (k:Keyword {name : row.keyword1}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (k:Keyword {name : row.keyword2}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (k:Keyword {name : row.keyword3}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")
    session.run("LOAD CSV WITH HEADERS FROM \'file:///dataset-conference.csv\' AS row MATCH (k:Keyword {name : row.keyword4}), (p:Paper { title: row.ArticleTitle}) CREATE (k)-[:isIn]->(p)")

driver.close()
