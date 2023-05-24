# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
SQLAlchemy dialect for seqslab.hive
"""

import re

from seqslab import hive
from pyhive.sqlalchemy_hive import HiveDialect


class SeqsLabHiveDialect(HiveDialect):
    """
    seqslab+hive://<username>:<password>@<host>:<port>/<database>?
    http_path=<job_run_id>&ssl_cert=<none|optional|required>
    """
    name = "seqslab"
    scheme = "https"
    driver = "hive"

    @classmethod
    def dbapi(cls):
        return hive

    def create_connect_args(self, url):
        kwargs = {
            "host": url.host,
            "port": url.port or 443,
            "username": url.username,
            "password": url.password,
            "database": re.sub(r'[^0-9a-zA-Z]', '_', url.database).lower() or "default",
        }

        if url.query is not None and "http_path" in url.query:
            kwargs["http_path"] = url.query["http_path"]

        kwargs.update(url.query)
        return [], kwargs

    def get_table_names(self, connection, schema=None, **kw):
        query = 'SHOW TABLES'
        if schema:
            query += ' IN ' + self.identifier_preparer.quote_identifier(schema)
        return [row[1] for row in connection.execute(query)]
