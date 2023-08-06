#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'sql-smith',
        version = '1.0.0',
        description = 'sql-smith is an SQL query builder with zero dependencies and a fluent interface.',
        long_description = '=========\nsql-smith\n=========\n\n**sql-smith** is an SQL query builder with zero dependencies and a fluent interface.\n\n    The sentence above is, beside the name, a copy from the website of the PHP library\n    Latitude_, for the simple reason that this Python module is a port of Latitude.\n\nInstallation\n************\n\n.. code-block:: sh\n\n    $ pip install sql-smith\n\nQuick Start\n***********\n\nQueryFactory is a factory to create a **SELECT**, **INSERT**, **UPDATE** or **DELETE** query.\nUse the fluent interface of the queries to complete the query.\n\n.. code-block:: python\n\n    from sql_smith import QueryFactory\n    from sql_smith.engine import CommonEngine\n    from sql_smith.functions import field\n    \n    factory = QueryFactory(CommonEngine())\n    query = factory \\\n        .select(\'id\', \'username\') \\\n        .from_(\'users\') \\\n        .where(field(\'id\').eq(5)) \\\n        .compile()\n    \n    print(query.sql)  # SELECT "id", "username" FROM "users" WHERE "id" = ?\n    print(query.params)  # (5)\n\nWhen the query is ready, compile it. The return value of compile is a Query class instance\nwith two properties: sql and params. Use these properties to pass the query to a database.\n\n.. code-block:: python\n\n    import sqlite3\n    \n    db = sqlite3.connect(\'test.db\')\n    cur = db.cursor()\n\n    for row in cur.execute(query.sql, query.params):\n        print(row)\n\n.. _Latitude: https://latitude.shadowhand.com/\n',
        long_description_content_type = 'text/x-rst',
        classifiers = [
            'License :: OSI Approved :: MIT License',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Operating System :: OS Independent'
        ],
        keywords = 'sql-smith query builder querybuilder sql mysql sqlite postgres sqlserver database',

        author = 'Franky Braem',
        author_email = 'franky.braem@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT',

        url = 'https://github.com/fbraem/sql-smith',
        project_urls = {},

        scripts = [],
        packages = [
            'sql_smith',
            'sql_smith.builder',
            'sql_smith.capability',
            'sql_smith.engine',
            'sql_smith.interfaces',
            'sql_smith.partial',
            'sql_smith.partial.parameter',
            'sql_smith.query',
            'sql_smith.query.mysql',
            'sql_smith.query.postgres',
            'sql_smith.query.sql_server'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
