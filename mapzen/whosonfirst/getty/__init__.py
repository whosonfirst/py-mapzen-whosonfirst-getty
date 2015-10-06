# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import requests
import StringIO
import rdflib
import os.path
import logging
import sys

# the crawl stuff can / should probably go in a 'utils' package or really
# a 'getty.geojson' package...
# (20151004/thisisaaronland)

import geojson
import multiprocessing
import signal

def crawl(source, **kwargs):

    validate = kwargs.get('validate', False)
    inflate = kwargs.get('inflate', False)

    for (root, dirs, files) in os.walk(source):

        for f in files:
            path = os.path.join(root, f)
            path = os.path.abspath(path)

            ret = path

            if not path.endswith('geojson'):
                continue

            if validate or inflate:

                try:
                    fh = open(path, 'r')
                    data = geojson.load(fh)

                except Exception, e:
                    logging.error("failed to load %s, because %s" % (path, e))
                    continue

                if not inflate:
                    ret = path
                else:
                    ret = data

            yield ret

def crawl_with_callback(source, callback, **kwargs):

    iter = crawl(source, **kwargs)

    if kwargs.get('multiprocessing', False):

        processes = multiprocessing.cpu_count() * 2
        pool = multiprocessing.Pool(processes=processes)

        def sigint_handler(signum, frame):
            logging.warning("Received interupt handler (in crawl_with_callback scope) so exiting")
            pool.terminate()
            sys.exit()

        signal.signal(signal.SIGINT, sigint_handler)

        batch = []
        batch_size = kwargs.get('multiprocessing_batch_size', 1000)

        for rsp in iter:

            batch.append((callback, rsp))

            if len(batch) >= batch_size:

                pool.map(_callback_wrapper, batch)
                batch = []

        if len(batch):
            pool.map(_callback_wrapper, batch)

    else:

        for rsp in iter:
            callback(rsp)

# Dunno - python seems all sad and whingey if this gets defined in
# the (crawl_with_callback) scope above so whatever...
# (20150902/thisisaaronland)

def _callback_wrapper(args):

    callback, feature = args

    try:
        callback(feature)
    except KeyboardInterrupt:
        logging.warning("Received interupt handler (in callback wrapper scope) so exiting")
    except Exception, e:
        logging.error("Failed to process feature because %s" % e)
        raise Exception, e

# basically everything in this class should be moved in to a properly
# generic 'working-with-geojson' class so I can stop rewriting it over
# and over and over again (20151004/thisisaaronland)

import mapzen.whosonfirst.geojson
import atomicwrites

class exporter:

    def __init__(self, root):

        encoder = mapzen.whosonfirst.geojson.encoder()
        self.encoder = encoder 

        self.root = root

    def feature2abspath(self, feature):

        rel_path = self.feature2relpath(feature)
        return os.path.join(self.root, rel_path)

    def feature2relpath(self, feature):

        if feature.get('id', False):
            return self.id2abspath(feature.get('id'))

        props = feature.get('properties', {})
        id = props.get('tgn:id', 0)

        return self.id2relpath(id)

    def id2abspath(self, id):

        rel_path = self.id2relpath(id)
        return os.path.join(self.root, rel_path)
        
    def id2relpath(self, id):

        path = self.id2path(id)
        fname = self.id2fname(id)
        
        return os.path.join(path, fname)

    def id2path(self, id):

        tmp = str(id)
        parts = []
        
        while len(tmp) > 3:
            parts.append(tmp[0:3])
            tmp = tmp[3:]
            
        if len(tmp):
            parts.append(tmp)

        return "/".join(parts)

    def id2fname(self, id):
        return "%s.geojson" % id

    def export_feature(self, feature):

        abs_path = self.feature2abspath(feature)

        with atomicwrites.atomic_write(abs_path, overwrite=True) as fh:
            self.encoder.encode_feature(feature, fh)

        return abs_path

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

    def prefLabels(self, **kwargs):

        prune = kwargs.get('prune_links', False)

        for s, p, o in self.triples_about_me():

            if p != 'prefLabel':
                continue
                
            if prune and o.startswith('http'):
                continue

            yield o

    def names(self):

        return self.require_p('label')

    def require_p(self, value):

        for s, p, o in self.triples_about_me():

            if p != value:
                continue

            yield o

# as in: http://vocab.getty.edu/aat/term/1000571284-en

class term(record):

    def __init__(self, compound_id):

        if compound_id.startswith('http'):
            compound_id = os.path.basename(compound_id)

        record.__init__(self, "http://vocab.getty.edu/aat/term/", compound_id)

        uid, lang = compound_id.split("-", 1)
        self.uid = uid
        self.lang = lang

    def term(self):
        return self.require_p('term')

    def literal(self):
        return self.require_p('literalForm')

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

    
