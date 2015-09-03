# py-mapzen-whosonfirst-getty

Python tools for working with Getty controlled vocabularies (and Who's On First data)

## IMPORTANT

This library is provided as-is, right now. It lacks proper
documentation which will probably make it hard for you to use unless
you are willing to poke and around and investigate things on your
own.

## Usage

### Example

```
import mapzen.whosonfirst.getty

id = 7013051
place = mapzen.whosonfirst.getty.tgn(id)

print list(place.names())
print list(place.placetypes())

print ""

for a in p.ancestors():

    n = a.names()
    t = a.placetypes()

    n = n.next()
    t = list(t)

    print "%s, %s" % (n, t)
```

Which should yield something like this:

```
[u'Montr\xe9al', u'Montreal', u'Fort Ville Marie', u'Hochelaga']
[u'inhabited places', u'inhabited place', u'nederzetting', u'populated places', u'settlements (inhabited places)', u'settlement (inhabited place)', u'human settlements', u'places, inhabited', u'bewoonde gebieden', u'asentamientos (asentamiento y paisajes)', u'asentamiento (asentamiento y paisajes)', u'cities', u'city', u'communities, urban', u'stad', u'urban communities', u'\u57ce\u5e02', u'\u5e02', u'\u90fd\u5e02', u'ch\xe9ng sh\xec', u'ciudad', u'cheng shi', u"ch'eng shih", u'steden', u'St\xe4dte (Siedlungen)', u'Stadt (Siedlung)', u'ciudades', u'commercial centers (inhabited places)', u'commercial center (inhabited place)', u'centers, commercial (inhabited places)', u'commercial centres (inhabited places)', u'commercial centre (inhabited place)', u'educational centers (buildings)', u'educational center (building)', u'centers, educational (buildings)', u'educational centres (buildings)', u'educational centre (building)', u'\u6559\u80b2\u4e2d\u5fc3 (\u5efa\u7bc9\u7269)', u'\u6587\u6559\u4e2d\u5fc3', u'ji\xe0o y\xf9 zh\u014dng x\u012bn', u'jiao yu zhong xin', u'chiao y\xfc chung hsin', u'onderwijscentra (opleidingscentra)', u'Bildungszentren', u'Bildungszentrum', u'cultural centers (buildings)', u'cultural center (building)', u'building, cultural (building)', u'buildings, cultural (buildings)', u'centers, cultural (buildings)', u'cultural buildings (buildings)', u'w\xe9n hu\xe0 zh\u014dng x\u012bn', u'cultural centres (buildings)', u'wen hua zhong xin', u'cultural centre (building)', u'wen hua chung hsin', u'centres, cultural (buildings)', u'\u6587\u5316\u4e2d\u5fc3 (\u5efa\u7bc9\u7269)', u'culturele centra', u'cultureel centrum', u'centros culturales (buildings)', u'centro cultural (building)', u'financial centers', u'financial center', u'financial centres', u'financial centre', u'centers, financial', u'centres, financial', u'transportation centers (inhabited places)', u'transportation center (inhabited places)', u'center, transportation (inhabited places)', u'transportation centres (inhabited places)', u'transportation centre (inhabited places)', u'industrial centers (inhabited places)', u'industrial center (inhabited place)', u'centers, industrial (inhabited places)', u'industrial centres', u'industrial centre', u'centres, industrial', u'ports (settlements)', u'port (settlement)', u'port cities', u'havengebieden', u'havengebied', u'puertos', u'puerto']

Canadian, [u'primary political entities', u'primary political entity', u'primary political units', u'political entities, primary', u'nations', u'nation', u'countries (nations)', u'nation states', u'states (nations)', u'states, nation', u'\u570b\u5bb6', u'gu\xf3 ji\u0101', u'guo jia', u'naci\xf3n', u'kuo chia', u'naties', u'natie', u'naciones', u'independent sovereign nations', u'independent sovereign nation']
North and Central America, [u'continents', u'continent', u'continent', u'continental masses', u'\u5927\u9678', u'\u6d32', u'\u5927\u6d32', u'd\xe0 l\xf9', u'da lu', u'ta lu', u'continenten', u'Kontinente', u'Kontinent', u'Erdteil', u'Erdteile', u'continentes', u'continente']
Québec, [u'first level subdivisions (political entities)', u'first level subdivision (political entity)', u'provinces', u'province', u'provincies', u'provincie', u'provincias', u'provincia']
Montréal, Île de, [u'islands (landforms)', u'island (landform)', u'isles', u'eilanden', u'eiland', u'islas', u'isla']
```

## See also

* https://github.com/whosonfirst/whosonfirst-data/

