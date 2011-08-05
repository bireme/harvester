from oaipmh.metadata import MetadataReader

qdc_reader = MetadataReader(
        fields={
        'author':                ('textList', 'dcterms:author/text()'),
        'accessioned':           ('textList', 'dcterms:accessioned/text()'),
        'available':             ('textList', 'dcterms:available/text()'),
        'issued':                ('textList', 'dcterms:issued/text()'),
        'bibliographicCitation': ('textList', 'dcterms:issued/text()'),
        'issn':                  ('textList', 'dcterms:issn/text()'),
        'identifier':            ('textList', 'dc:identifier/text()'),
        'description':           ('textList', 'dc:description/text()'),
        'abstract':              ('textList', 'dcterms:abstract/text()'),
        'sponsorship':           ('textList', 'dcterms:sponsorship/text()'),
        'language':              ('textList', 'dc:language/text()'),
        'publisher':             ('textList', 'dc:publisher/text()'),
        'ispartofseries':        ('textList', 'dcterms:ispartofseries/text()'),
        'subject':               ('textList', 'dc:subject/text()'),
        'title':                 ('textList', 'dc:title/text()'),
        'alternative':           ('textList', 'dcterms:alternative/text()'),
        'type':                  ('textList', 'dc:type/text()'),
        'format':                ('textList', 'dc:format/text()'),
        'source':                ('textList', 'dc:source/text()'),
        'relation':              ('textList', 'dc:relation/text()'),
        'coverage':              ('textList', 'dc:coverage/text()'),
        'rights':                ('textList', 'dc:rights/text()')
        },
        namespaces={
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'dc' : 'http://purl.org/dc/elements/1.1/',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'schemaLocation': 'http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2006/01/06/dcterms.xsd http://purl.org/dc/elements/1.1/ http://dublincore.org/schemas/xmls/qdc/2006/01/06/dc.xsd',
        'lang': 'en_US',
        'dcterms': 'http://purl.org/dc/terms/'}
        )