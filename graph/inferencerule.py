
class InferenceRule:

    def getqueries(self):
        return None

    def maketriples(self,binding):
        return self._maketriples(*binding)