from database.DB_connect import DBConnect
from model.chromosome import Chromosome
from model.edge import Edge


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllChromosomes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select distinct g.Chromosome as chr
                    from genes g
                    where g.Chromosome != 0"""

        cursor.execute(query)

        for row in cursor:
            res.append(Chromosome(row["chr"]))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select g1.Chromosome as chr1, g2.Chromosome as chr2, sum(i1.Expression_Corr) as peso
                    from genes g1, interactions i1, genes g2
                    where g1.GeneID = i1.GeneID1 
                    and g2.GeneID = i1.GeneID2
                    and g1.Chromosome != g2.Chromosome
                    and g1.Chromosome != 0
                    and g2.Chromosome != 0
                    group by g1.Chromosome, g2.Chromosome"""

        cursor.execute(query)

        for row in cursor:
            res.append(Edge(**row))

        cursor.close()
        conn.close()
        return res