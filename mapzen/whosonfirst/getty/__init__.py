# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import requests
import StringIO
import rdflib
import os.path
import logging
import sys

# some of this could be moved in to a generic mapzen.whosonfirst.rdfmoonlanguage base class
# (20150903/thisisaaronland)

class nt:

    def __init__ (self, **kwargs):

        if kwargs.get('file', False):

            self.fh = open(kwargs['file'], 'r')

        elif kwargs.get('url', False):

            io = StringIO.StringIO()

            rsp = requests.get(kwargs['url'])
            io.write(rsp.text)
            io.seek(0)

            self.fh = io

        else:

            raise Exception, "Nothing to parse!"

        self.simplify_predicates = kwargs.get('simplify_predicates', True)

    def parse(self):

        self.fh.seek(0)

        for ln in self.fh:

            ln = ln.strip()

            graph = rdflib.Graph()
            graph.parse(data=ln, format='nt')

            for stmt in graph:
                yield self.prepare_statement(stmt)

    def predicates(self):

        predicates = {}
        line = 0

        for s,p,o in self._parse():

            if predicates.get(p, False):
                predicates[p] += 1
            else:
                predicates[p] = 1

            line += 1
            logging.debug("%s %s predicates" % (line, len(predicates.keys())))
            
        return predicates

    def prepare_statement(self, stmt):

        s, p, o = map(unicode, stmt)

        if self.simplify_predicates:

            p = os.path.basename(p)
            
            if "#" in p:
                ignore, p = p.split("#")

        return (s, p, o)

# please add some smarts to periodically purge
# this so that it doesn't eat its host computer
# (20150903/thisisaaronland)

class cache:

    def __init__(self):
        self.cache = {}

    def cache_get(self, k):
        return self.cache.get(k, None)
        
    def cache_set(self, k, v):
        self.cache[k] = v

    def cache_unset(self, k):
        if self.cache.get(k, None):
            del(self.cache[k])

class record(cache):

    def __init__(self, root, id):

        cache.__init__(self)

        self.root = root
        self.id = id

    def uri(self):
        uri = self.root + str(self.id)
        return uri

    def url(self):
        url = self.uri() + ".nt"
        return url

    def triples(self):
        
        body = self.fetch()

        for spo in body.parse():
            # print spo
            yield spo
            
    def triples_about_me(self):

        for s, p, o in self.triples():

            if s == self.uri():
                yield (s, p, o)

    def dump(self):
        for spo in self.triples():
            print spo

    def fetch(self):

        url = self.url()
        cache = self.cache_get(url)

        if cache:
            return cache

        rsp = nt(url=url)
        
        self.cache_set(url, rsp)
        return rsp

    def names(self):
        
        for s, p, o in self.triples_about_me():

            if p != 'label':
                continue

            yield o

# please to me MOAR BETTER about vocabulary URL definitions
# and lookups and trailing slashes (20150903/thisisaaronland)

class aat(record):

    def __init__(self, id):

        record.__init__(self, "http://vocab.getty.edu/aat/", id)

class tgn(record):
    
    def __init__(self, id):

        record.__init__(self, "http://vocab.getty.edu/tgn/", id)

    def note(self):

        note_uri = None
        note = None

        for s, p, o in self.triples_about_me():

            if p != 'scopeNote':
                continue

            root = os.path.dirname(o)

            if root != 'http://vocab.getty.edu/tgn/scopeNote':
                continue

            note_uri = o
            break

        if not note_uri:
            return None

        for s, p, o in self.triples():

            if s != note_uri:
                continue

            if p != 'value':
                continue

            note = o
            break

        return note

    def ancestors(self):

        for s, p, o in self.triples_about_me():

            if p != 'broaderTransitive':
                continue

            root = os.path.dirname(o) + "/"

            if root != "http://vocab.getty.edu/tgn/" :
                continue
                
            id = os.path.basename(o)

            ancestor = tgn(id)
            yield ancestor
            
    def placetypes(self):

        for s, p, o in self.triples():

            if s == self.uri() and p == 'placeType':
                
                root = os.path.dirname(o) + "/"

                if root != "http://vocab.getty.edu/aat/" :
                    continue

                id = os.path.basename(o)
                a = aat(id)

                for n in a.names():
                    yield n

if __name__ == '__main__':

    id = 7007826

    p = tgn(id)

    print list(p.names())
    print p.note()

    sys.exit()

    print list(p.names())
    print list(p.placetypes())

    print ""

    for a in p.ancestors():

        n = a.names()
        t = a.placetypes()

        n = n.next()
        t = list(t)

        print "%s, %s" % (n, t)

    
