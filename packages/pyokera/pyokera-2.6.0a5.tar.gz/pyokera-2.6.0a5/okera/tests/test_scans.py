# Copyright 2017 Okera Inc. All Rights Reserved.
#
# Tests that should run on any configuration. The server auth can be specified
# as an environment variables before running this test.
# pylint: disable=bad-continuation,bad-indentation,global-statement,unused-argument
# pylint: disable=no-self-use
import time
import unittest
import json
import numpy

from okera._thrift_api import TTypeId

from okera.tests import pycerebro_test_common as common
import cerebro_common as cerebro

retry_count = 0

class BasicTest(common.TestBase):
    def test_sparse_data(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            df = planner.scan_as_pandas("rs.sparsedata")
            self.assertEqual(96, len(df), msg=df)
            self.assertEqual(68, df['age'].count(), msg=df)
            self.assertEqual(10.0, df['age'].min(), msg=df)
            self.assertEqual(96.0, df['age'].max(), msg=df)
            self.assertEqual(b'sjc', df['defaultcity'].max(), msg=df)
            self.assertEqual(86, df['description'].count(), msg=df)

    def test_nulls(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            df = planner.scan_as_pandas("select string_col from rs.alltypes_null")
            self.assertEqual(1, len(df), msg=df)
            self.assertTrue(numpy.isnan(df['string_col'][0]), msg=df)

            df = planner.scan_as_pandas(
                "select length(string_col) as c from rs.alltypes_null")
            self.assertEqual(1, len(df), msg=df)
            self.assertTrue(numpy.isnan(df['c'][0]), msg=df)

    def test_timestamp_functions(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json("""
                select date_add('2009-01-01', 10) as c from okera_sample.sample""")
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('2009-01-11 00:00:00.000', str(json[0]['c']), msg=json)
            self.assertEqual('2009-01-11 00:00:00.000', str(json[1]['c']), msg=json)

    def test_duplicate_cols(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json("""
                select record, record from okera_sample.sample""")
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record']),
                             msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record_2']),
                             msg=json)

        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json("""
                select record, record as record_2, record from okera_sample.sample""")
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record']),
                             msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record_2']),
                             msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record_2_2']),
                             msg=json)

    def test_large_decimals(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json("select num from rs.large_decimals2")
            self.assertTrue(len(json) == 6, msg=json)
            self.assertEqual('9012248907891233.020304050670',
                             str(json[0]['num']), msg=json)
            self.assertEqual('2343.999900000000', str(json[1]['num']), msg=json)
            self.assertEqual('900.000000000000', str(json[2]['num']), msg=json)
            self.assertEqual('32.440000000000', str(json[3]['num']), msg=json)
            self.assertEqual('54.230000000000', str(json[4]['num']), msg=json)
            self.assertEqual('4525.340000000000', str(json[5]['num']), msg=json)

        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            df = planner.scan_as_pandas("select num from rs.large_decimals2")
            self.assertTrue(len(df) == 6, msg=df)
            self.assertEqual('9012248907891233.020304050670',
                             str(df['num'][0]), msg=df)
            self.assertEqual('2343.999900000000', str(df['num'][1]), msg=df)
            self.assertEqual('900.000000000000', str(df['num'][2]), msg=df)
            self.assertEqual('32.440000000000', str(df['num'][3]), msg=df)
            self.assertEqual('54.230000000000', str(df['num'][4]), msg=df)
            self.assertEqual('4525.340000000000', str(df['num'][5]), msg=df)

    def test_date(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json("select * from datedb.date_csv")
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('Robert', str(json[0]['name']), msg=json)
            self.assertEqual(100, json[0]['id'], msg=json)
            self.assertEqual('1980-01-01', str(json[0]['dob']), msg=json)
            self.assertEqual('Michelle', str(json[1]['name']), msg=json)
            self.assertEqual(200, json[1]['id'], msg=json)
            self.assertEqual('1991-12-31', str(json[1]['dob']), msg=json)

        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            pd = planner.scan_as_pandas("select * from datedb.date_csv")
            self.assertTrue(len(pd) == 2, msg=pd)
            self.assertEqual(b'Robert', pd['name'][0], msg=pd)
            self.assertEqual(100, pd['id'][0], msg=pd)
            self.assertEqual('1980-01-01', str(pd['dob'][0]), msg=pd)
            self.assertEqual(b'Michelle', pd['name'][1], msg=pd)
            self.assertEqual(200, pd['id'][1], msg=pd)
            self.assertEqual('1991-12-31', str(pd['dob'][1]), msg=pd)

    def test_scan_as_json_max_records(self):
        sql = "select * from okera_sample.sample"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(json) == 1, msg='max_records not respected')
            json = planner.scan_as_json(sql, max_records=100, max_client_process_count=1)
            self.assertTrue(len(json) == 2, msg='max_records not respected')

    def test_scan_as_pandas_max_records(self):
        sql = "select * from okera_sample.sample"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            pd = planner.scan_as_pandas(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 1, msg='max_records not respected')
            pd = planner.scan_as_pandas(sql, max_records=100, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 2, msg='max_records not respected')

    def test_scan_retry(self):
        global retry_count

        sql = "select * from okera_sample.sample"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            # First a sanity check
            pd = planner.scan_as_pandas(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 1, msg='test_scan_retry sanity check failed')

            # Patch scan_as_pandas to throw an IOError 2 times
            retry_count = 0
            def test_hook_retry(func_name, retries, attempt):
                if func_name != "plan":
                    return
                global retry_count
                retry_count = retry_count + 1
                if attempt < 2:
                    raise IOError('Fake Error')

            planner.test_hook_retry = test_hook_retry
            pd = planner.scan_as_pandas(sql, max_records=1, max_client_process_count=1)

            assert(retry_count == 3) # count = 2 failures + 1 success
            self.assertTrue(len(pd.index) == 1, msg='Failed to get data with retries')

    def test_worker_retry(self):
        global retry_count

        ctx = common.get_test_context()
        with common.get_worker(ctx) as worker:
            # First a sanity check
            v = worker.get_protocol_version()
            self.assertEqual('1.0', v)

            # Patch get_protocol_version to throw an IOError 2 times
            retry_count = 0
            def test_hook_retry(func_name, retries, attempt):
                if func_name != "get_protocol_version":
                    return
                global retry_count
                retry_count = retry_count + 1
                if attempt < 2:
                    raise IOError('Fake Error')

            worker.test_hook_retry = test_hook_retry
            v = worker.get_protocol_version()

            assert(retry_count == 3) # count = 2 failures + 1 success
            self.assertEqual('1.0', v)

    def test_overwrite_file(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            planner.execute_ddl("DROP TABLE IF EXISTS rs.dim")
            planner.execute_ddl("""CREATE EXTERNAL TABLE rs.dim
                (country_id INT, country_name STRING, country_code STRING)
                ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
                LOCATION 's3://cerebro-datasets/starschema_demo/country_dim/'
                TBLPROPERTIES ('skip.header.line.count'='1')""")

            # Copy one version of the file into the target location
            cerebro.run_shell_cmd('aws s3 cp ' +\
                's3://cerebro-datasets/country_dim_src/country_DIM.csv ' +\
                's3://cerebro-datasets/starschema_demo/country_dim/country_DIM.csv')
            before = planner.scan_as_json('rs.dim')[0]
            self.assertEqual("France", before['country_name'], msg=str(before))

            # Copy another version. This file has the same length but a different
            # character. S3 maintains time in ms timestamp, so sleep a bit.
            time.sleep(1)

            cerebro.run_shell_cmd('aws s3 cp ' +\
                's3://cerebro-datasets/country_dim_src/country_DIM2.csv ' +\
                's3://cerebro-datasets/starschema_demo/country_dim/country_DIM.csv')
            i = 0
            while i < 10:
                after = planner.scan_as_json('rs.dim')[0]
                if 'france' in after['country_name']:
                    return
                self.assertEqual("France", after['country_name'], msg=str(after))
                time.sleep(.1)
                i = i + 1
            self.fail(msg="Did not updated result in time.")

    def test_scan_as_json_newline_delimiters(self):
        sql1 = '''select
         *
        from
        okera_sample.sample'''
        sql2 = '''select
        *
        from
        okera_sample.sample'''
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json(sql1, max_records=100, max_client_process_count=1)
            self.assertTrue(
                len(json) == 2,
                msg='could parse query with newline and space delimiters')
            json = planner.scan_as_json(sql2, max_records=100, max_client_process_count=1)
            self.assertTrue(
                len(json) == 2,
                msg='could parse query with newline delimiters')

    def test_scan_as_json_using_with_clause(self):
        sql1 = '''WITH male_customers AS
         (SELECT * FROM okera_sample.users WHERE gender = 'M')
         SELECT * FROM male_customers;'''
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json = planner.scan_as_json(sql1, max_records=100, max_client_process_count=1)
            self.assertTrue(
                len(json) == 100,
                msg='could parse query that starts with "with"')

    def test_scan_as_json_serialization(self):
        sql = "select * from rs.alltypes"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            json.loads(json.dumps(planner.scan_as_json(sql)))

    def test_das_6218(self):
        DB = "das_6218"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self._recreate_test_db(conn, DB)
            conn.execute_ddl('''
                CREATE EXTERNAL TABLE %s.alltypes(
                  bool_col BOOLEAN,
                  tinyint_col TINYINT,
                  smallint_col SMALLINT,
                  int_col INT,
                  bigint_col BIGINT,
                  float_col FLOAT,
                  double_col DOUBLE,
                  string_col STRING,
                  varchar_col VARCHAR(10),
                  char_col CHAR(5),
                  timestamp_col TIMESTAMP,
                  decimal_col decimal(24, 10))
                ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
                STORED AS TEXTFILE
                LOCATION 's3://cerebrodata-test/alltypes/'
                ''' % DB)

            # Verify schema from catalog, plan and data are all timestamp
            schema = conn.plan('%s.alltypes' % DB).schema
            self.assertEqual(schema.cols[10].type.type_id, TTypeId.TIMESTAMP_NANOS)
            df = conn.scan_as_pandas('SELECT timestamp_col FROM %s.alltypes' % DB)
            self.assertEqual(str(df.dtypes[0]), 'datetime64[ns, UTC]')
            catalog_schema = conn.list_datasets(DB, name='alltypes')[0].schema
            self.assertEqual(
                catalog_schema.cols[10].type.type_id, TTypeId.TIMESTAMP_NANOS)
            print(df)

            # Create a view that is proper with the explicit cast.
            conn.execute_ddl('''
                CREATE VIEW %s.v1(ts STRING)
                AS
                SELECT cast(timestamp_col AS STRING) FROM %s.alltypes''' % (DB, DB))
            # Verify schema from catalog, plan and data are all strings
            catalog_schema = conn.list_datasets(DB, name='v1')[0].schema
            self.assertEqual(catalog_schema.cols[0].type.type_id, TTypeId.STRING)
            schema = conn.plan('%s.v1' % DB).schema
            self.assertEqual(schema.cols[0].type.type_id, TTypeId.STRING)
            df = conn.scan_as_pandas('%s.v1' % DB)
            self.assertEqual(str(df.dtypes[0]), 'object')
            print(df)

            # We want to carefully construct a view that has mismatched types with
            # the view definition. The view just selects a timestamp columns but we
            # will force the catalog type to be string, instead of timestamp.
            # This forces the planner to produce an implicit cast.
            conn.execute_ddl('''
                CREATE EXTERNAL VIEW %s.v2(ts STRING)
                SKIP_ANALYSIS USING VIEW DATA AS
                "SELECT timestamp_col FROM %s.alltypes"''' % (DB, DB))
            # Verify schema from catalog, plan and data are all strings
            catalog_schema = conn.list_datasets(DB, name='v2')[0].schema
            self.assertEqual(catalog_schema.cols[0].type.type_id, TTypeId.STRING)
            schema = conn.plan('%s.v2' % DB).schema
            self.assertEqual(schema.cols[0].type.type_id, TTypeId.STRING)
            df = conn.scan_as_pandas('%s.v2' % DB)
            self.assertEqual(str(df.dtypes[0]), 'object')
            print(df)

    def test_zd_1633(self):
        DB = "zd_1633"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self._recreate_test_db(conn, DB)
            conn.execute_ddl('''
                CREATE EXTERNAL TABLE %s.t(
                  s STRING)
                STORED AS TEXTFILE
                LOCATION 's3://cerebrodata-test/zd-1627/'
                ''' % DB)
            res = conn.scan_as_json('%s.t' % DB)
            # Default quote, only 1 row
            self.assertEqual(1, len(res))

            # No quote, should be 2 rows now
            conn.execute_ddl("ALTER TABLE %s.t SET SERDEPROPERTIES('quoteChar'='')" % DB)
            res = conn.scan_as_json('%s.t' % DB)
            self.assertEqual(2, len(res))

            # Recreate using table properties
            conn.execute_ddl('DROP TABLE %s.t' % DB)
            conn.execute_ddl('''
                CREATE EXTERNAL TABLE %s.t(
                  s STRING)
                STORED AS TEXTFILE
                LOCATION 's3://cerebrodata-test/zd-1627/'
                TBLPROPERTIES('okera.text-table.default-quote-char'='')
                ''' % DB)
            res = conn.scan_as_json('%s.t' % DB)
            self.assertEqual(2, len(res))

            # Explicit serde properties overrides table properties
            conn.execute_ddl('''
                ALTER TABLE %s.t SET SERDEPROPERTIES('quoteChar'='"')''' % DB)
            res = conn.scan_as_json('%s.t' % DB)
            self.assertEqual(1, len(res))

            # Table with two cols
            conn.execute_ddl('DROP TABLE %s.t' % DB)
            conn.execute_ddl('''
                CREATE EXTERNAL TABLE %s.t(
                  c1 STRING, c2 STRING)
                STORED AS TEXTFILE
                LOCATION 's3://cerebrodata-test/customers/c1/zd1633_2/'
                TBLPROPERTIES('skip.header.line.count'='1')
                ''' % DB)
            conn.execute_ddl(
                "ALTER TABLE %s.t SET SERDEPROPERTIES('field.delim'=',')" % DB)
            res = conn.scan_as_json('%s.t' % DB)
            self.assertEqual(1, len(res))

            # Remove quote handling
            conn.execute_ddl("ALTER TABLE %s.t SET SERDEPROPERTIES('quoteChar'='')" % DB)
            res = conn.scan_as_json('%s.t' % DB)
            self.assertEqual(2, len(res))
            self.assertEqual('"123', res[1]['c2'])

    def test_scan_delta_dummy_metadata(self):
        DB = "delta_dummy_scan_db"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self._recreate_test_db(conn, DB)
            conn.execute_ddl('''
      CREATE EXTERNAL TABLE %s.airline_events_delta (
          col array<string>)
      WITH SERDEPROPERTIES (
          'path'='s3://cerebrodata-test/delta/airlines/airline_events/',
          'serialization.format'='1')
      STORED AS TEXTFILE
      LOCATION 's3://cerebrodata-test/delta/airlines/airline_events/'
      TBLPROPERTIES (
          'totalSize'='66153', 'numRows'='-1', 'rawDataSize'='-1',
          'okera.delta.infer-schema'='true',
          'COLUMN_STATS_ACCURATE'='false',
          'spark.sql.sources.schema.part.0'='{\"type\":\"struct\",\"fields\":[]}',
          'numFiles'='1', 'spark.sql.partitionProvider'='catalog',
          'spark.sql.sources.schema.numParts'='1', 'spark.sql.sources.provider'='delta',
          'spark.sql.create.version'='3.0.1')
                ''' % DB)
            res = conn.scan_as_json('%s.airline_events_delta' % DB)
            self.assertEqual(1326, len(res))

    def test_scan_dummy_spark_metadata(self):
        DB = "spark_dummy_scan_db"
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            self._recreate_test_db(conn, DB)
            conn.execute_ddl('''
CREATE EXTERNAL TABLE %s.fact_segment_events_last (
  col ARRAY<STRING> COMMENT 'from deserializer'
)
PARTITIONED BY (
  year INT,
  month INT,
  day INT)
WITH SERDEPROPERTIES ('path'='s3://yotpo-data-lake/warehouse/segment/full/last', 'serialization.format'='1')
STORED AS PARQUET
LOCATION 's3://yotpo-data-lake/warehouse/segment/full/last'
TBLPROPERTIES (
    'spark.sql.sources.schema.partCol.0'='year',
    'spark.sql.sources.schema.part.9'='rated_text_removed_albums\",\"type\":{\"type\":\"array\",\"elementType\":\"string\",\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_neutral_reviews_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_invited_user_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_facebook_ad_account_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_autoplay_speed_checkbox\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_conversation_duration\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_public\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_message_body\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_questions_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_qn_a\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_page_number\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_has_referrer_first_name_variable\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_review_notifications_star2\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_review_notifications_subscribed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_count_orders\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_cta_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_rich_snippets\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_email_rendering_succeeded\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is5_stars_checked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_rad_prefill_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_email_subject\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_hashtag\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_deleted_user\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_package\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_shoppable_instagram\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_promoted_products_widget\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties__rrs_sent_in_billing_cycle\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_package_monthly_price\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_reminder_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_website_publish_link\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_agent_username\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_phrase\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_yotpo_product_score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"anonymous_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"event_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_page_category\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_app_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_top_negative_sentences\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"product_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"review_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"sentence\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_default_image_used\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_domain\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_pla\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_result_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"proper',
    'spark.sql.sources.schema.partCol.2'='day',
    'spark.sql.sources.schema.partCol.1'='month',
    'spark.sql.sources.schema.part.6'='true,\"metadata\":{}},{\"name\":\"properties_signup_country\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_email_template_version_order\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_admin_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_agent_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_total_products_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_subscribed_to_blog_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_rich_snippets\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sort_by\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_path\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_uploader_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_results_per_page\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_facebook_token\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tag_domain_key\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_map_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_sent_tsr\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_revenue\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_product\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_tab_position_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_ip\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_signup_utmmedium\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_topic_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_cta_location\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldform_sfdccampaign\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_mapcustom_fields_enabled\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_conversation_link\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_pinterest_token_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_primary_color\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_utm_content_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_explicit_review\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_old_package\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_external_order_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_facebook_spend\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_interaction_response\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"fieldId\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"fieldRequired\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"fieldType\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"label\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"value\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_new_main_widget_layout\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_sentiment_filter\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"user_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_device_brand\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_invited_user_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldsubscribedto_email_course\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_show_total_count_checkbox\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_video_title\",\"type\":\"string\",\"nullab',
    'spark.sql.sources.schema.part.5'='to_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_removed_from_albums\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_email_template_content_changed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"event_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_intercom_user_hash\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"page_path\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_online\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_amount_of_words\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_order_amount\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_traits_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_conversion_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_status\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_review_notifications\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"page_title\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_page_path\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_system_notifications\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_error\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_closed_question_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_questions_and_answers_subscribed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_free_text_profanity\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_section\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_signup_employee_count\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_products_shown\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_step\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_configuration_action\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_meeting_time\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_dma_code\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_exception_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sidebar_open\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_insights_api_end_point\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_package_categories\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_pla\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_last_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_state_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_number_reviews\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_product_star_rating\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_from_product\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_post_words\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_email_template_subject_changed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"app_key\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_duration\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_timezone\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_developer_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_start_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_lpg_action_value\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_send_after\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_platform\",\"type\":\"string\",\"nullable\":',
    'spark.sql.create.version'='2.4.5',
    'spark.sql.sources.schema.part.8'='pdated_testimonial_link_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_imported_reviews\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldform_category\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_os_patch\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_using_packages_service\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"_metadata_bundled\",\"type\":{\"type\":\"array\",\"elementType\":\"string\",\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_title\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_social_publish_link\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_store_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_post_title_text_length\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_top_negative_period\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"product_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"review_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"sentence\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"message_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_ctabutton_text_check_box\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_action\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tsr_upload_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_total_errors\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_bottom_overall_conversion_of_searching_users\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"overall_conversion_of_searching_users\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_card_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_invited_user_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_domain_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_admin_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_album_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_category\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_email_template_key\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tag_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_image_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_activation_url\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_send_to_email_address\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_comment_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_lpg_action_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_negative_topics\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"mentions_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"rank\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"sentiment_score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"topic\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_image_ids\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"external_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_has_pos\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_mode',
    'spark.sql.sources.schema.part.7'='le\":true,\"metadata\":{}},{\"name\":\"properties_reviewer_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_app_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_widget_font\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"review_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_moderated_text_selected_albums\",\"type\":{\"type\":\"array\",\"elementType\":\"string\",\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_old_package_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_birthday_selected_points\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_package\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_sent_mas\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_badge\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_location\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_email_campaign_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_tsr\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_charge_price\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_comments\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_team_member_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_newsletter_subscribed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_include_product_photo\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_css_editor\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_promoted_products_title_check_box\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_existing_baseline_version\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_profanity_filter_selection\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_auto_publish_enabled\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_state\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_album_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_message_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_device_model\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_gross_margin\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_map_state\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_expiration_period_in_hours\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_promoted_products_widget\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_pct_reached\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_dedicated_page\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_picture_url\",\"type\":{\"type\":\"array\",\"elementType\":\"string\",\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_user_days_to_renewal\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_pixel_version\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_comments_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_visitors\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_downgrade_reason\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_filter_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_review_submission\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_primary_color_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_reviewer_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_meeting_duration\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_u',
    'spark.sql.sources.schema.part.14'='\"name\":\"properties_cta_is_open\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_subject\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_question_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_source_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_skip_email\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_error_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldutm_campaign_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_company_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"page_url\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_phone\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_sent_tpr\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_signature\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_month\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_summary\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_secondary_color_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_synced_gallery_enabled\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tag_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_orders_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_last_locked_feature\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_medium_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_status_filter_selection\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_phase_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_merchant_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_conversation_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_profanity_notification\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_admin_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_first_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_quick_filter_selection\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_auto_publish_enabled\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_qn_a\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_feed_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_post_frequency_check_box\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_num_of_points\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_admin_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_send_after_amount\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_purchase_selected_points\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_minimum_opinions\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_app_developer_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_top_positive_period\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"product_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"review_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"sentence\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_days_invalid_pinterest_token\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_metro_code\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_browser_family\",\"type\":\"string\",\"nullable',
    'spark.sql.sources.schema.part.15'='\":true,\"metadata\":{}},{\"name\":\"properties_is_has_promoted_products_email\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_products_count\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_order_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_page_title_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_credit_card_last4_digits\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_selecting_reviews\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_object_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_item_sentiment_score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_moderated_text_allow_remove_from_shoppable_instagram\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_user_agent\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_renewal_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_title\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"session_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"year\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"month\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"day\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"year\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"month\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"day\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}}]}',
    'spark.sql.sources.schema.part.12'='lean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_meeting_time_zone\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_automatic_frequency_drop_down\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_emails_attempted\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_orders\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_medium\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_baseline_version\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_first_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_csv_path\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_moderation_link\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_error_message\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_product_tag_missing\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_signature_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_layout\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_background_color_checkbox\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_device_family\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"received_at\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_view\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_feature\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"page_search\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_pending_rrs\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_charge_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_star_rating_color_check_box\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_gclid_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_pull_past_orders_enabled\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_old_instance_version\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_stars_color_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_contepowerreviewsnt\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_checked\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_results_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_positive_opinions_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_post_title_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_attributes_feedback\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_utm_campaign\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_link_expiration_period_in_hours\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_url_for_skipped\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_coupon_notification_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_ctabutton_color\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_end_anonymous_user_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_source_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_title\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_pays_via\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_google_spend\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_star_rating_color\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_classic_editor\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_campaign_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_u',
    'spark.sql.sources.schema.part.13'='pdated_header_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invited_user_store_restricted\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sentences\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_sent_site_reminder\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_created_at\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_content_type_filter_selection\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sub_status_filter_selection\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_min_star_rating\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_positive_reviews_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_watched_pct\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_library_version\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_amount_of_products_in_file\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_only_my_instagram_photos_check_box\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_blog_category\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_upload_button\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_multiple_products_max_emails_amount\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_product_url\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_reviewer_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldutm_medium_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_avg_distinct_queries_in_domain_key_products\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"avg_distinct_queries_in_domain_key\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_spam_filter_checkbox_checked\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_opinions\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_order_currency\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_view_by\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_alignment\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_product_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_library_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_star_rating\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_marketo_form_loaded\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_old_pacakge_monthly_price\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldsubscribedto_shopify_plus_email_course\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_to_product\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_page_title_check_box\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_integration_version\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_personal_info\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_country_code\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_gsr\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_instance_version\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_last_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_max_orders\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_os_minor\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_user_renewal_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{',
    'spark.sql.sources.schema.part.10'='ties_signup_monthly_orders_count\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_total_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_override_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_thirty_day_revenue_cents\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_account_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_email_templates_reset_confirmed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_cross_sell\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_customer_tab_clicked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_term\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_card_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_multi_product\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_os_major\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_positive_topics\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"mentions_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"rank\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"sentiment_score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"topic\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_topics_in_favorites_section_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_social_network\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_order_amount\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties__rrmonthly_limit\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_page_url\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_popup_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_traits_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_autoplay_speed\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_favorite_action\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_widget_visible\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_end_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_utm_term_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_negative_opinions_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_all_reviews\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_page_referrer\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_album_picture_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldform_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_cokuchcake20silicon20molden20silicon20form20tent\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_gallery_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_days_to_renewal\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_product_didnt_arrive_notification\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_users_count_limit_reached\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_gsr\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_agency\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_original_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_post_comments\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_current_app\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sentiment_value\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_link_to_testimonial_page_checkbox\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_package_i',
    'spark.sql.partitionProvider'='catalog',
    'spark.sql.sources.schema.part.11'='d\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_org_key\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_friend_discount\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_review_notifications_star3\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_instance_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_open_text_question_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_os_family\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_group_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_traits_plan\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_pictures_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_publish_everywhere_link\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_referrals_selected\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties__package_extensions\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_number_of_reviews\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_subscription_state\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_website\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldutm_source_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_dest_app\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_invalid_reason\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_multiple_products_review_request_logic\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_credit_card_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_number_of_reviews\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_country_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_longitude\",\"type\":\"float\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_creation_location\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_referral_code\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_emails_sent\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_insights_api_error\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_friend_tab_clicked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldhashtag\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_topics_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_org_admin_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_amount_of_products\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_page_search\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_coupons\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_yotpo_ip\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_negative_reviews_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_errors_file\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_receive_newsletters\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_marketo_form_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_system_notifications_subscribed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_gallery_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_review_notifications_star1\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_chargify_balance\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_email_template_content_save_succeeded\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_industry_average\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_sentiment_notification\",\"type\":\"boo',
    'spark.sql.sources.schema.part.2'='iewer_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_collection_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_media_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_breakdown_by\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_convert_to_site_review\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_title\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_days_in_dunning\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_cta_title\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_org_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sentiment_filter_selection\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_from_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_signup_utmterm\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_twitter_token_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties__locked_feature_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_body\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_order_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties__deleted_users\",\"type\":{\"type\":\"array\",\"elementType\":\"string\",\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_mkto_person_notes\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_content\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_thirty_day_order_volume\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_to_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_browser_major\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_post_author\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_cta_url\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_item_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_media_sub_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_reviews_widget_installed\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_next_charge_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_ctabutton_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_order_id\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_filter_location\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_tpr\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_star_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_last_conversion_order_time\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"event\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tpr_upload_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_failed_reviews\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_fieldreferrer_token\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_term\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_filter_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tag_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_region_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_multiple_products_interval\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_region\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_opinion_sentiment\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_mandatory_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_number_orders\",\"ty',
    'spark.sql.sources.schema.part.1'='perties_admin\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_locked_menu_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_sent_mai\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_account_selected_points\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_map_state\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_coupons\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_import_status\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_integration_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_end_user_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_postal_code\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_comment_body\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_picture_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_verified_file\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_store_domain\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"channel\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"event_sent_to_segment_at\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_media_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_first_invite\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_header_customization_checkbox\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_facebook_token_date\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_link_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_reviewer_first_letter\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_days_invalid_facebook_token\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is2_stars_checked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_days_invalid_twitter_token\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_clicked_update_npsscore\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_neutral_opinions_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_yotpo_product_score_v2\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_cokuchen20silicon20form20tent\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_url_for_verified\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_chargify_revenue\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_interaction_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_email_template_subject_save_succeeded\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sentiment_change\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_widget_font_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_subject\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_invited_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"is_out_of_date_range\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_stars_color\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_role\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_integration_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_first_album\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_campaign_sq\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_product_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_added_to_albums\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_name_on_credit_card\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_rev',
    'spark.sql.sources.schema.part.4'='e\":\"properties_tab_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_latitude\",\"type\":\"float\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_phone\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_total_search_generated_purchases_products\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"total_search_generated_purchases\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_keyword\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_phase\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_ad_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_ad_network\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_submission\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_body_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_reviews_carousel\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_custom_reviews\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_product_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_platform\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_text_size\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_maps\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_recurring_payment_interval\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_top_overall_conversion_of_searching_users\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"overall_conversion_of_searching_users\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_hashtag_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_moderation_action\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_video_host\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_products_app_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_billing_provider\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"original_timestamp\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_download_link\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_total_searches_in_domain_key_products\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"total_searches_in_domain_key\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_referrer\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_url_for_errors\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_cta_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_segment_id_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_moderation_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_twitter_token\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_date_range\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_syndicated_inherit\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_shopify_plan\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_review_product_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_show_navigation_arrows_checkbox\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_social_push\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_cta_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_send_',
    'spark.sql.sources.schema.part.3'='pe\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tag_location\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_item_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_customer_points\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_batch_action\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_platform_plan\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_promoted_products_email\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_email_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_map\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_uninstall_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_report_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_review_notifications_star4\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_reviews_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_campaign_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"page_referrer\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_campaign_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is1_star_checked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_signup_utmsource\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_button_clicked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_send_after_amount\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_user_plan_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_sent_map\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_product_enablement\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sorting_content\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_failure_reason\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"context_page_title\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_enabled_custom_reviews\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_body\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_browser_patch\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_receive_review_notifications_star5\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_email_template_version_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_new_package_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_user_agent_browser_minor\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_ui_version\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_star_rating_filter_selection\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_subject_updated\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_signup_utmcampaign\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_product_with_reviews_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is4_stars_checked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_email_templates_reset_succeeded\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_signup_utmcontent\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_failure_message\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_agent_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_testimonial_link_url\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"nam',
    'spark.sql.sources.schema.numPartCols'='3',
    'spark.sql.sources.schema.part.0'='{\"type\":\"struct\",\"fields\":[{\"name\":\"valid_event_for_session\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"segment_user_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_area_code\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_end_user_email\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_tag_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_old_state\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_topics_in_all_others_section_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_sentiment_score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_media_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_city\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_filter_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_team_member_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"parsed_ip_country_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_install_order_volume\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"event_created_at\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_card_header\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_invalid_pinterest_token\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_phase\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_search_medium\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_reviews_tab\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_error_text\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is_has_star_rating\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_is3_stars_checked\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_old_plarform\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_lead_type_c\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_feature_update_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_signature\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_background_color\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_anonymized_email_count\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"_metadata_unbundled\",\"type\":{\"type\":\"array\",\"elementType\":\"string\",\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"days_from_purchase_changed\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_topics_shown\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_url\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_post_published\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_form_field_lead_source\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_attributes_score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_top_positive_sentences\",\"type\":{\"type\":\"array\",\"elementType\":{\"type\":\"struct\",\"fields\":[{\"name\":\"product_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"review_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"score\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"sentence\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]},\"containsNull\":true},\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_end_user_id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_year\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_moderated_text_is_product_album\",\"type\":\"boolean\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_plan_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_header_text_color\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"properties_updated_reviews_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"pro',
    'spark.sql.sources.schema.numParts'='16',
    'spark.sql.sources.provider'='parquet')''' %  DB)

            # Without flag and schema inference, we get the dummy cols and partition cols
            ds = conn.list_datasets(DB, name='fact_segment_events_last')
            self.assertEqual(5, len(ds[0].schema.cols))

            # Alter to enable schema inference
            conn.execute_ddl('''
                alter table %s.fact_segment_events_last
                set tblproperties('okera.spark-table.infer-schema'='true')''' % DB)
            ds = conn.list_datasets(DB, name='fact_segment_events_last')
            self.assertEqual(733, len(ds[0].schema.cols))

    def test_pandas_index(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as planner:
            # We scan a small table but with a tiny min task size, so that it is
            # guaranteed to generate more than one task. We then verify that our
            # overall row indices are correct.
            df = planner.scan_as_pandas("okera_sample.sample", min_task_size=1)

            indices = []
            for i, row in df.iterrows():
                indices.append(i)

            assert len(indices) == 2
            assert indices[0] == 0
            assert indices[1] == 1

if __name__ == "__main__":
    unittest.main()
