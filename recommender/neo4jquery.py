from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import pandas as pd

class OntologyRecomendations:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def __init__(self, uri):
        self.driver = GraphDatabase.driver(uri)

    def close(self):
        self.driver.close()

    def get_recomendations(self, movieId):
        with self.driver.session() as session:
            recomendations = session.read_transaction(self._return_recomendations, movieId)
            return recomendations

    @staticmethod
    def _return_recomendations(tx, movieId):
        query = """MATCH (m:Movie {{id: {movie} }})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(idMovies:Movie)
                        WHERE EXISTS {{ MATCH (m)-[:STARRING]->( :Actor)<-[:STARRING]-(idMovies:Movie)}}
                        RETURN idMovies, g""".format(movie=movieId)
        result = tx.run(query)
        return [row for row in result]




if __name__ == "__main__":
    id_list = [3619, 1453, 3619, 1021]
    greeter = OntologyRecomendations("bolt://localhost:7687", "neo4j", "12345")
    greeter.get_recomendations(3619)
    greeter.close()





