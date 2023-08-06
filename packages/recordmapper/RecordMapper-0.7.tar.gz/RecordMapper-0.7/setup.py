# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['RecordMapper',
 'RecordMapper.appliers',
 'RecordMapper.avro',
 'RecordMapper.builders',
 'RecordMapper.common',
 'RecordMapper.csv',
 'RecordMapper.xml']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=4.5.4,<4.6.0',
 'dateparser>=1.0.0,<1.1.0',
 'defusedxml>=0.7.1,<0.8.0',
 'fastavro>=1.4,<1.5',
 'nose>=1.3.7,<1.4.0']

setup_kwargs = {
    'name': 'recordmapper',
    'version': '0.7',
    'description': 'Transform records using an Avro schema and custom map functions.',
    'long_description': '# RecordMapper\n\nRead, transform and write records using an Avro schema and custom map functions.\n\n\n## Installing the project\n\nTo install the project, run the following command from the root directory:\n\n```bash\n$pip install .\n```\n\nIt is highly recommended to use a virtual environment when installing the project \ndependencies in order to avoid version conflicts.\n\n\n## Updating PyPI version\n\n    poetry publish --build\n \n \n## RecordMapper elements\n \n### Appliers\n\nAppliers are the elements that materialise the records transformations. They apply \nsequentially specific transformations to each record and/or its schema. \n\nThere are four appliers defined by now:\n\n- The selector applier, which will modify the base schema if there exist nested schemas to consider.\n- The rename applier, which will develop a renaming process using the aliases included in the schema.\n- The transform applier which will apply the record transformations given the transforming functions.\n- The clean applier, which will filter the output fields to keep only the ones given in the output schema.\n\nAn Applier is a class that implements the *apply* method, which receives a single \nrecord and its schema and returns their transformed version after the transforming\nprocess. They are located in the appliers directory.\n\n\n### Readers\n\nTo apply the records transformations, the Record Mapper must be able to read the file that\ncontains the data in order to extract them. The Record Mapper supports reading files from \ndifferent formats, including csv, xml and avro.\n\nThe reading process is done by the *Reader* objects. A Reader class implements methods to \nread different kind of files. The Reader class is extended by sub-classes, each of them \nspecialized in reading an specific format. For example, to read an XML file we can use the\nXMLReader class. To extract data from a CSV file, we will be using the CSVReader class.\n\nA Reader sub-class implements the *read_records_from_input* method, which will return the\ncontent of the file record by record. Each specific Reader sub-class is located in the \ndirectory of its own format, sharing space with the correspondent Writer sub-class.\n\n\n### Writers\n\nAfter applying the records transformations, the Record Mapper must be able to write the\nresultant transformed records in a file. It supports writing files for different formats, \nincluding csv and avro. \n\nImportant! The Record Mapper can return different files as output, one for each format, \nbut at least it is mandatory to write the avro file. Thus, avro file is always returned.\n\nThe writing process is done by the *Writer* objects. A Writer class implements methods to \nwrite to different formats. The Writer class is extended by sub-classes, each of them \nspecialized in writing an specific format. For example, to write a CSV file we can use the\nCSVWriter class while we will be using the AvroWriter to write an Avro file.\n\nA Writer sub-class implements the *write_records_to_output* method, which will write a given\niterable of records in an output file. Each specific Writer sub-class is located in the \ndirectory of its own format, sharing space with the correspondent Reader sub-class. The \nmethod accepts other output options as parameters. These output options include:\n- Flattening nested schemas when writing csv files.\n- Merging schemas when writing avro files.\n',
    'author': 'uDARealEstate Data Engineering Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/urbandataanalytics/RecordMapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
