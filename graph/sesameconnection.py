__author__ = 'Ed Duarte'
__email__ = "edmiguelduarte@gmail.com"
__copyright__ = "Copyright 2015, Ed Duarte"
__credits__ = ["Ed Duarte"]

__license__ = "Apache License 2.0"
__version__ = "2.0.0"
__maintainer__ = "Ed Duarte"
__status__ = "Prototype"

import urllib
import httplib2


class connection:
    def __init__(self, url):
        self.baseurl = url

    def protocol(self):
        # Fetch the protocol version
        endpoint = '%sprotocol' % self.baseurl
        (response, content) = httplib2.Http().request(endpoint, 'GET')
        print("Response %s" % response.status)
        print(content)

    def repository_list(self):
        # Fetch the repository list
        endpoint = '%srepositories' % self.baseurl
        header = {'accept': 'application/sparql-results+json'}
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)
        return content

    def query_get(self, repository, query):
        # Evaluate a SeRQL-select query on repository
        params = {'query': query}
        header = {'accept': 'application/sparql-results+json'}
        endpoint = '%srepositories/%s?%s' % (self.baseurl,
                                             repository,
                                             urllib.urlencode(params))
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)
        return content

    def query_post(self, repository, query):
        # Evaluate a SPARQL-construct query on repository using a POST request
        params = {'query': query}
        header = {'content-type': 'application/x-www-form-urlencoded',
                  'accept': 'application/rdf+json'}
        endpoint = '%srepositories/%s?%s' % (
            self.baseurl, repository, urllib.urlencode(params))
        (response, content) = httplib2.Http().request(
            endpoint,
            'POST',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)
        return content

    def query_ask(self, repository, query):
        # Evaluate a SPARQL-ask query on repository
        params = {'query': query}
        header = {'accept': 'text/boolean'}
        endpoint = '%srepositories/%s?%s' % (
            self.baseurl, repository, urllib.urlencode(params))
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)
        return content

    def add_repository(self, repository, title):
        # Add the repository
        header = {'content-type': 'application/x-turtle;charset=UTF-8'}
        params = {'context': '<http://WS>'}
        endpoint = '%srepositories/%s/statements?%s' % (
            self.baseurl,
            'SYSTEM',
            urllib.urlencode(params)
        )

        body = """
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
        @prefix rep: <http://www.openrdf.org/config/repository#>.
        @prefix sr: <http://www.openrdf.org/config/repository/sail#>.
        @prefix sail: <http://www.openrdf.org/config/sail#>.

        [] a rep:Repository ;
           rep:repositoryID "%s" ;
           rdfs:label "%s" ;
           rep:repositoryImpl [
              rep:repositoryType "openrdf:SailRepository" ;
              sr:sailImpl [
                 sail:sailType "openrdf:MemoryStore"
              ]
           ].
           """ % (repository, title)

        (response, content) = httplib2.Http().request(
            endpoint,
            'POST',
            body=body,
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def remove_repository(self, repository):
        # Remove the repository
        endpoint = '%srepositories/%s' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(endpoint, 'DELETE')
        print("Response %s" % response.status)
        print(content)

    def statements(self, repository):
        # Fetch all statements from repository
        header = {'accept': 'application/rdf+json'}
        endpoint = '%srepositories/%s/statements' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def get_statements_of_context(self, repository, context):
        # Fetch all statements from a specific context in repository
        header = {'accept': 'application/rdf+json'}
        endpoint = '%srepositories/%s/statements?%s' % (
            self.baseurl, repository, context)
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def remove_all_statements(self, repository):
        # Remove all statements from the repository
        endpoint = '%srepositories/%s/statements' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(endpoint, 'GET')
        print("Response %s" % response.status)
        print(content)

    def add_data(self, repository, data, context):
        # Add data to the repository
        header = {'content-type': 'application/rdf+xml;charset=UTF-8'}
        params = {'context': context}
        endpoint = '%srepositories/%s/statements?%s' % (
            self.baseurl, repository, urllib.urlencode(params))
        (response, content) = httplib2.Http().request(
            endpoint,
            'POST',
            body=data,
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def replace_data(self, repository, data):
        # Add data to the repository, replacing any and all existing data
        header = {'content-type': 'application/rdf+xml;charset=UTF-8'}
        endpoint = '%srepositories/%s/statements' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'PUT',
            body=data,
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def replace_data_of_context(self, repository, data, context):
        # Add data to a specific context in the repository, replacing any data
        # that is currently in this context
        header = {'content-type': 'application/x-turtle;charset=UTF-8'}
        params = {'context': context}
        endpoint = '%srepositories/%s/statements?%s' % (
            self.baseurl, repository, urllib.urlencode(params))
        (response, content) = httplib2.Http().request(
            endpoint,
            'PUT',
            body=data,
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def add_statements_no_context(self, repository, data):
        # Add statements without a context to the repository, ignoring any
        # context information that is encoded in the supplied data
        header = {'content-type': 'application/x-turtle;charset=UTF-8'}
        endpoint = '%srepositories/%s/statements' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'POST',
            body=data,
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def update_described(self, repository, update):
        # Perform update described in a SPARQL 1.1 Update string
        header = {'content-type': 'application/x-www-form-urlencoded'}
        params = {'update': urllib.urlencode(update)}
        endpoint = '%srepositories/%s/statements?%s' % (
            self.baseurl, repository, urllib.urlencode(params))
        (response, content) = httplib2.Http().request(
            endpoint,
            'POST',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def update_described_document(self, repository, data, update):
        # Perform updates described in a transaction document and treat it as
        # a single transaction
        header = {'content-type': 'application/x-rdftransaction'}
        endpoint = '%srepositories/%s/statements' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'POST',
            body=data,
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def context_identifiers(self, repository):
        #  Fetch all context identifiers from repository
        header = {'accept': 'application/sparql-results+json'}
        endpoint = '%srepositories/%s/contexts' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def namespace_info(self, repository):
        # Fetch all namespace declaration info
        header = {'accept': 'application/sparql-results+json'}
        endpoint = '%srepositories/%s/namespaces' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def remove_namespace(self, repository):
        # Remove all namespace declarations from the repository.
        # endpoint = '%srepositories/%s' % (self.baseurl, repository)
        endpoint = '%srepositories/%s/namespaces' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(endpoint, 'DELETE')
        print("Response %s" % response.status)
        print(content)

    def get_namespace(self, repository, prefix):
        # Get the namespace for prefix
        endpoint = '%srepositories/%s/namespaces/%s' % (
            self.baseurl, repository, prefix)
        (response, content) = httplib2.Http().request(endpoint, 'GET')
        print("Response %s" % response.status)
        print(content)

    def set_namespace(self, repository, prefix):
        # Set the namespace for a specific prefix
        header = {'content-type': 'text/plain'}
        endpoint = '%srepositories/%s/namespaces/%s' % (
            self.baseurl, repository, prefix)
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def remove_namespace_prefix(self, repository, prefix):
        # Remove the namespace for a specific prefix
        endpoint = '%srepositories/%s/namespaces/%s' % (
            self.baseurl, repository, prefix)
        (response, content) = httplib2.Http().request(endpoint, 'DELETE')
        print("Response %s" % response.status)
        print(content)

    def size_of_repository(self, repository):
        # Get the size of repository
        endpoint = '%srepositories/%s/size' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(endpoint, 'GET')
        print("Response %s" % response.status)
        print(content)

    def size_of_repository_context(self, repository, context):
        # Fetch the protocol version
        params = {'context': context}
        endpoint = '%srepositories/%s/size?%s' % (
            self.baseurl, repository, urllib.urlencode(params))
        (response, content) = httplib2.Http().request(endpoint, 'GET')
        print("Response %s" % response.status)
        print(content)

    def statements_directly_graph(self, repository):
        # Fetch all statements from a directly referenced named graph
        # in a repository
        header = {'accept': 'application/rdf+json'}
        endpoint = '%srepositories/%s/rdf-graphs/graph1' % (
            self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def statements_indirectly_graph(self, repository, graph):
        # Fetch all statements from an indirectly referenced named graph
        # in a repository
        header = {'accept': 'application/rdf+json'}
        params = {'graph': graph}
        endpoint = '%srepositories/%s/rdf-graphs/service?%s' % (
            self.baseurl, repository, urllib.urlencode(params))
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def statements_default_graph(self, repository):
        # Fetch all statements from the default graph in repository
        header = {'accept': 'application/rdf+json'}
        endpoint = '%srepositories/%s/rdf-graphs/service?default' % (
            self.baseurl, repository)
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def add_statements_referenced_graph(self, repository, data):
        # Add statements to a directly referenced named graph in the repository
        header = {'content-type': 'application/x-turtle;charset=UTF-8'}
        endpoint = '%srepositories/%s/rdf-graphs/graph1' % (
            self.baseurl,
            repository
        )
        (response, content) = httplib2.Http().request(
            endpoint,
            'GET',
            body=data,
            headers=header
        )
        print("Response %s" % response.status)
        print(content)

    def directly_referenced_graph(self, repository):
        # Clear a directly referenced named graph in the "mem-rdf" repository
        endpoint = '%srepositories/%s/namespaces/' % (self.baseurl, repository)
        (response, content) = httplib2.Http().request(endpoint, 'DELETE')
        print("Response %s" % response.status)
        print(content)


if __name__ == '__main__':
    c = connection('http://localhost:8080/openrdf-sesame/')
    repository = 'taxonomy'
    prefix = 'PREFIX %s:<%s>\n' % (
        'taxonomy',
        'http://www.semanticweb.org/ontologies/2013/4/taxonomy.owl#'
    )
    query = query = 'SELECT ?x WHERE{ ?id1 ?x ?id2 . }'
    data = open("/Users/edduarte/data.rdf", "rb").read()
    print("protocol()")
    c.protocol()
    print("repositoryList()")
    c.repository_list()

    # c.add_repository(repository, repository)
    # c.remove_namespace(repository)
    # print "addData(repository, data)"
    # c.add_data(repository, data)

    # print "queryGET(self, repository, query)"
    # c.query_get(repository, query)
    # c.size_of_repository(repository)
    c.statements_default_graph(repository)