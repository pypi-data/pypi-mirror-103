# Copyright 2021 Okera Inc. All Rights Reserved.
#
# Some scenario tests for steward delegation
#
# pylint: disable=broad-except
# pylint: disable=global-statement
# pylint: disable=no-self-use
# pylint: disable=too-many-lines
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-locals
# pylint: disable=bad-continuation
# pylint: disable=broad-except

from okera import context
from okera.tests import pycerebro_test_common as common

from okera import _thrift_api

ATTR = "perf_test.attr1"
DB = "python_perf_test_db"
TBL1 = "tbl1"
TBL2 = "tbl2"
ROLE = "python_perf_test_role"
TEST_USER = "pythonperfuser"

def _create_wide_view(db, tbl, multiple, source_db, source_tbl):
    cols = []
    for idx in range(multiple):
        cols.extend([
            "uid AS uid%04d" % (idx),
            "dob AS dob%04d" % (idx),
            "gender AS gender%04d" % (idx),
            "ccn AS ccn%04d" % (idx),
        ])
    stmt = "CREATE VIEW %s.%s AS SELECT %s FROM %s.%s" % (
        db, tbl, ', '.join(cols), source_db, source_tbl)

    return stmt

class PerfTest(common.TestBase):
    def test_wide_table_with_attributes(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            print()
            ddls = [
                "DROP ATTRIBUTE IF EXISTS %s" % (ATTR),
                "CREATE ATTRIBUTE %s" % (ATTR),

                "DROP DATABASE IF EXISTS %s CASCADE" % (DB),
                "CREATE DATABASE %s" % (DB),

                """CREATE TABLE {db}.users (
                  uid STRING ATTRIBUTE {attr},
                  dob STRING ATTRIBUTE {attr},
                  gender STRING ATTRIBUTE {attr},
                  ccn STRING ATTRIBUTE {attr}
                )""".format(db=DB, attr=ATTR),

                _create_wide_view(DB, TBL1, 100, DB, 'users'),

                "DROP ROLE IF EXISTS %s" % (ROLE),
                "CREATE ROLE %s WITH GROUPS %s" % (ROLE, TEST_USER),
                "GRANT SELECT ON DATABASE %s HAVING ATTRIBUTE IN (%s) TO ROLE %s" % (DB, ATTR, ROLE),
            ]

            for ddl in ddls:
                conn.execute_ddl(ddl)

            """
            ---------------------------- admin --------------------------
            Iterations 100
            Mean 68.4731936454773 ms
            50%: 67.74592399597168 ms
            90%: 70.44172286987305 ms
            95%: 73.26173782348633 ms
            99%: 100.9974479675293 ms
            99.5%: 100.9974479675293 ms
            99.9%: 100.9974479675293 ms
            """
            def list(tbl):
                def get():
                    datasets = conn.list_datasets(DB, name=tbl)
                    assert len(datasets) == 1
                return get

            common.measure_latency(100, list(TBL1))

            """
            ---------------------------- test user --------------------------
            Iterations 100
            Mean 484.99685287475586 ms
            50%: 477.36072540283203 ms
            90%: 510.06484031677246 ms
            95%: 526.5743732452393 ms
            99%: 825.0184059143066 ms
            99.5%: 825.0184059143066 ms
            99.9%: 825.0184059143066 ms
            """
            ctx.enable_token_auth(token_str=TEST_USER)
            common.measure_latency(100, list(TBL1))