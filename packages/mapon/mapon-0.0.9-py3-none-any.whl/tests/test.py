import os
import sys
import unittest
import sqlite3
import pandas as pd

TESTPATH = os.path.dirname(os.path.realpath(__file__))
PYPATH = os.path.join(TESTPATH, '..', '..')
sys.path.append(PYPATH)

import mapon as mo
from mapon.util import add, where, isnum


# customers.csv
# CustomerID,CustomerName,ContactName,Address,City,PostalCode,Country
# 1,Alfreds Futterkiste,Maria Anders,Obere Str. 57,Berlin,12209,Germany
# 2,Ana Trujillo Emparedados y helados,Ana Trujillo,Avda. de la Constitución 2222,México D.F.,5021,Mexico
# 3,Antonio Moreno Taquería,Antonio Moreno,Mataderos 2312,México D.F.,5023,Mexico
# 4,Around the Horn,Thomas Hardy,120 Hanover Sq.,London,WA1 1DP,UK
# 5,Berglunds snabbköp,Christina Berglund,Berguvsvägen 8,Luleå,S-958 22,Sweden


# orders.csv
# orderid,customerid,employeeid,orderdate,shipperid
# 10248,90,5,1996-07-04,3
# 10249,81,6,1996-07-05,1
# 10250,34,4,1996-07-08,2
# 10251,84,3,1996-07-08,1


def remdb():
    if os.path.isfile('test.db'):
        os.remove('test.db')


def initialize():
    remdb()
    #
    mo.mapon._JOBS = {}
    mo.run()


class TestLoading(unittest.TestCase):
    def setUp(self):
        initialize()
        # make empty table

    def test_dbfilename_created_as_script_name(self):
        # mo.run in setUp created empty test.db
        name, _ = os.path.splitext(os.path.basename(__file__))
        self.assertIn(name + '.db', os.listdir())

    def test_loading_ordinary_csv(self):
        mo.register(orders=mo.load('orders.csv'))
        mo.run()
        self.assertEqual(len(list(mo.get('orders'))), mo.mapon._line_count('orders.csv', 'utf-8', '\n'))

    # TODO: some of the other options like encoding must be tested
    def test_loading_ordinary_tsv(self):
        mo.register(markit=mo.load('markit.tsv'))
        mo.run()
        self.assertEqual(len(list(mo.get('markit'))), mo.mapon._line_count('markit.tsv', 'utf-8', '\n'))

    def test_loading_semicolon_separated_file(self):
        mo.register(orders1=mo.load('orders1.txt', delimiter=";"))
        mo.run()
        self.assertEqual(len(list(mo.get('orders1'))), mo.mapon._line_count('orders1.txt', 'utf-8', '\n'))
        with open('orders1.txt') as f:
            cols = list(mo.get('orders1')[0])
            self.assertEqual(f.readline()[:-1].split(";"), cols)

    def test_loading_excel_files(self):
        mo.register(
            ff=mo.load('ff.xls'),
            ff1=mo.load('ff.xlsx'),
            na_sample=mo.load('na_sample.xlsx'),
        )
        mo.run()

        self.assertEqual(mo.get('ff'), mo.get('ff1'))
        na_sample = mo.get('na_sample')
        self.assertEqual(list(na_sample[0]), ['col1', 'col2'])
        self.assertEqual(len(na_sample), 2)

    def test_loading_sas_file(self):
        mo.register(
            ff5=mo.load('ff5_ew_mine.sas7bdat'),
        )
        mo.run()
        ff5 = mo.get('ff5', df=True)
        self.assertEqual(len(ff5), 253)

    def test_loading_stata_file(self):
        mo.register(
            crime=mo.load('crime.dta'),
        )
        mo.run()
        self.assertEqual(len(mo.get('crime', df=True)), 2725)

    def test_loading_seq(self):
        def add3(r):
            r['b'] = r['a'] + 3
            return r

        mo.register(
            seq_loading_sample=mo.load(({'a': i} for i in range(10)), fn=add3)
        )
        mo.run()

        seq_loading_sample = mo.get('seq_loading_sample')
        self.assertEqual(list(seq_loading_sample[0]), ['a', 'b'])

    def tearDown(self):
        if os.path.isfile('test.db'):
            os.remove('test.db')


class TestNone(unittest.TestCase):
    def setUp(self):
        initialize()
        mo.register(
            vendors=mo.load('tysql_Vendors.csv'),
        )
        mo.run()

    def test_none(self):
        def input_none(r):
            if not r['vend_state']:
                r['vend_state'] = None
            return r

        # inserting string 'None' doesn't actually make it None
        def input_none1(r):
            if not r['vend_state']:
                r['vend_state'] = 'None'
            return r

        mo.register(
            vendors1=mo.apply(input_none, 'vendors'),
            vendors2=mo.apply(input_none1, 'vendors'),
        )
        mo.run()

        self.assertEqual(len([r for r in mo.get('vendors') if r['vend_state'] == '  ']), 1)
        self.assertEqual(len([r for r in mo.get('vendors') if r['vend_state'] == '']), 1)
        # '' is falsy but '  ' is not
        self.assertEqual(len([r for r in mo.get('vendors1') if r['vend_state'] is None]), 1)
        self.assertEqual(len([r for r in mo.get('vendors2') if r['vend_state'] is None]), 0)

    def tearDown(self):
        if os.path.isfile('test.db'):
            os.remove('test.db')


class TestApply(unittest.TestCase):
    def setUp(self):
        initialize()
        mo.register(
            orders=mo.load('orders.csv'),
            customers=mo.load('customers.csv'),
        )
        mo.run()

    def test_thunk(self):
        def count():
            customers = mo.get('customers')
            def _f(r):
                r['num'] = len(customers)
                return r
            return _f

        mo.register(
            orders1 = mo.apply(count, 'orders'),
            orders2 = mo.apply(count, 'orders', parallel=True),
        )
        mo.run()

        orders1 = mo.get('orders1')
        orders2 = mo.get('orders2')
        self.assertEqual([r['num'] for r in orders1], [91] * len(orders1))
        self.assertEqual(orders1, orders2)

    def test_append_yyyy_yyyymm_columns(self):
        def add_yyyy_yyyymm(r):
            if r['orderdate'] > '1996-xx-xx':
                r['yyyy'] = r['orderdate'][:4]
                r['yyyymm'] = r['orderdate'][:7]
                yield r

        mo.register(
            orders1=mo.apply(add_yyyy_yyyymm, 'orders'),
        )
        mo.run()

        orders = mo.get('orders')
        orders1 = mo.get('orders1')
        self.assertEqual(len(orders[0]) + 2, len(orders1[0]))
        self.assertEqual(sum(1 for _ in orders1), 44)

    def test_group_by(self):
        def bigmarket(a):
            def fn(rs):
                if len(rs) > a:
                    yield from rs
            return fn

        def bigmarket1(a):
            def fn(rs):
                if len(rs) > a:
                    return rs
                else:
                    return []
            return fn

        mo.register(
            # you can either pass a function that returns
            # a dictionary (row) or  a list of dictionaries
            # or pass a generator that yields dictionaries
            customers1=mo.apply(bigmarket(5), 'customers', by='Country'),
            customers2=mo.apply(bigmarket1(5), 'customers', by='Country')
        )
        mo.run()
        self.assertEqual(list(mo.get('customers1')), list(mo.get('customers2')))

    def test_group_n(self):
        mo.register(
            orders1=mo.apply(lambda rs: {'a': len(rs)}, 'orders', by=10)
        )
        mo.run()
        self.assertEqual(len(mo.get('orders')), sum(r['a'] for r in mo.get('orders1')))

    # all of them at once
    def test_group_star(self):
        mo.register(
            orders1=mo.apply(lambda rs: rs, 'orders', by=' * '),
        )
        mo.run()
        self.assertEqual(mo.get('orders'), mo.get('orders1'))

    def test_group_invalid(self):
        mo.register(
            orders1=mo.apply(lambda rs: {'a': 10}, 'orders', by=10.0),
        )
        _, undone = mo.run()
        self.assertEqual([x['output'] for x in undone], ['orders1'])

    def test_insert_empty_rows(self):
        def filter10(r):
            if r['shipperid'] == 10:
                yield r

        mo.register(
            orders1=mo.apply(filter10, 'orders')
        )
        mo.run()
        with self.assertRaises(mo.mapon.NoSuchTableFound):
            list(mo.get('orders1'))

    def test_return_none(self):
        def foo(r):
            if r['shipperid'] == 1:
                return r

        mo.register(
            orders1=mo.apply(foo, 'orders'),
        )
        mo.run()
        self.assertEqual(len(list(mo.get('orders1'))), 54)

    def test_get(self):
        # dataframe
        orders_df = mo.get('orders', df=True)
        # list of dicts
        orders_ld = mo.get('orders')
        self.assertEqual(orders_df.shape[0], len(orders_ld))
        self.assertEqual(orders_df.shape[1], len(orders_ld[0]))

    def test_join(self):
        mo.register(
            torders = mo.load('tysql_Orders.csv'),
            torder_items = mo.load('tysql_OrderItems.csv'),
            torders1 = mo.apply(add(cust_id1=lambda r: str(r['cust_id'])[-1]), 'torders'),
            torders2 = mo.join(
                ['torders1', "*", 'order_num, cust_id1'],
                ['torder_items', 'order_num as order_num1, order_item, prod_id, quantity', ['order_num ', (">", 'order_item')]]
            ),
            torders3 = mo.apply(where(lambda r: isnum(r['order_num1'])), 'torders2')

        )
        mo.run()
        self.assertEqual(len(mo.get('torders2')), 11)
        self.assertEqual(len(mo.get('torders3')), 9)

    def tearDown(self):
        remdb()


class TestApplyErrornousInsertion(unittest.TestCase):
    def setUp(self):
        initialize()
        mo.register(
            orders=mo.load(file='orders.csv'),
        )
        mo.run()

    def test_insert_differently_named_rows(self):
        def errornous1(rs):
            r = rs[0]
            yield r
            del r['customerid']
            r['x'] = 10
            yield r

        mo.register(orders1=mo.apply(errornous1, 'orders', by='*'))
        mo.run()
        # orders1 is not created
        with self.assertRaises(mo.mapon.NoSuchTableFound):
            list(mo.get('orders1'))

    def test_insert_1col_deleted(self):
        def errornous1(rs):
            r = rs[0]
            yield r
            del r['customerid']
            yield r

        mo.register(orders1=mo.apply(errornous1, 'orders', by='*'))
        mo.run()
        # orders1 is not created
        with self.assertRaises(mo.mapon.NoSuchTableFound):
            list(mo.get('orders1'))

    def test_insert_1col_added(self):
        def errornous1(rs):
            r = rs[0]
            yield r
            # added 'xxx' col is ignored
            r['xxx'] = 10
            yield r

        mo.register(orders1=mo.apply(errornous1, 'orders', by='*'))
        mo.run()
        x1, x2 = list(mo.get('orders1'))
        self.assertEqual(x1, x2)

    def tearDown(self):
        remdb()


class TestGraph(unittest.TestCase):
    def setUp(self):
        initialize()

    def test_graph_dot_gv_file(self):
        def add_yyyy(r):
            r['yyyy'] = r['orderdate'][0:4]
            return r

        def count(rs):
            rs[0]['n'] = len(rs)
            yield rs[0]

        mo.register(
            orders=mo.load('orders.csv', fn=add_yyyy),
            customers=mo.load('customers.csv'),
            # append customer's nationality
            orders1=mo.join(
                ['orders', '*', 'customerid'],
                ['customers', 'Country', 'customerid'],
            ),
            # yearly number of orders by country
            orders2=mo.apply(count, 'orders1', by='yyyy, Country'),
        )
        saved_jobs = mo.mapon._JOBS
        mo.run()
        with open('test.gv') as f:
            graph = f.read()
            for j in saved_jobs:
                self.assertTrue(j in graph)

        with mo.mapon._connect('test.db') as c:
            c.drop('customers')

        mo.mapon._JOBS = saved_jobs
        # rerun
        jobs_to_do, jobs_undone = mo.run()
        self.assertEqual(set(j['output'] for j in jobs_to_do),
                         set(['customers', 'orders1', 'orders2']))
        self.assertEqual(jobs_undone, [])

    def tearDown(self):
        remdb()


# Test Join
class TestIntegratedProcess(unittest.TestCase):
    def setUp(self):
        initialize()

    def test_semiannual_and_quartery_orders_average_by_month(self):
        def sumup(rs):
            r = rs[0]
            r['norders'] = len(rs)
            return r

        def cnt(rs):
            for i, r in enumerate(rs):
                r['cnt'] = i
                yield r

        def orders_avg_nmonth(r):
            r['nmonth'] = 3
            try:
                r['avg'] = round((r['norders'] + r['norders1'] + r['norders2']) / 3, 1)
            except:
                r['avg'] = ''
            yield r

            r['nmonth'] = 6
            try:
                r['avg'] = round((r['norders'] + r['norders1'] + r['norders2'] +  \
                                  r['norders3'] + r['norders4'] + r['norders5']) / 6, 1)
            except:
                r['avg'] = ''
            yield r

        mo.register(
            orders=mo.load('orders.csv'),
            # add month
            orders1=mo.apply(add(yyyymm=lambda r: r['orderdate'][:7]), 'orders'),
            # count the number of orders by month
            orders2=mo.apply(fn=sumup, data='orders1', by='yyyymm'),
            orders3=mo.apply(fn=cnt, data='orders2', by='*'),
            # want to compute past 6 months
            orders4=mo.join(
                ['orders3', '*', 'cnt'],
                ['orders3', 'norders as norders1', 'cnt + 1'],
                ['orders3', 'norders as norders2', 'cnt + 2'],
                ['orders3', 'norders as norders3', 'cnt + 3'],
                ['orders3', 'norders as norders4', 'cnt + 4'],
                ['orders3', 'norders as norders5', 'cnt + 5']
            ),

            orders_avg_nmonth=mo.apply(fn=orders_avg_nmonth, data='orders4'),
        )

        mo.run()

        # with mo1._connect('test.db') as c:
        xs = []
        for r in mo.get('orders_avg_nmonth'):
            if isinstance(r['avg'], float) or isinstance(r['avg'], int):
                xs.append(xs)
        self.assertEqual(len(xs), 9)

    def tearDown(self):
        remdb()


class Testconcat(unittest.TestCase):
    def setUp(self):
        initialize()

    def test_simple_union(self):
        mo.register(
            orders = mo.load('orders.csv'),
            orders1=mo.apply(lambda r: r, 'orders'),
            orders2=mo.concat('orders, orders1'),
            # the following is also fine
            # orders2=mo.append(['orders', 'orders1'])
        )
        mo.run()

        self.assertEqual(len(list(mo.get('orders'))) * 2, len(list(mo.get('orders2'))))

    def tearDown(self):
        remdb()


class Testmzip(unittest.TestCase):
    def setUp(self):
        initialize()
        mo.register(
            order_items = mo.load('tysql_OrderItems.csv'),
            products = mo.load('tysql_Products.csv'),
        )
        mo.run()

    def test_mzip1(self):
        def itemsfn():
            allproducts = mo.get('products')
            def _f(items, products):
                if items:
                    for item in items:
                        r = {'order_num': item['order_num']}
                        r['n']  = len(allproducts)
                        r['prod_desc'] = ''
                        if products:
                            r['prod_desc'] = products[0]['prod_desc']
                        yield r
                else:
                    yield {'order_num': '', 'n': len(allproducts), 'prod_desc': 'Empty'}

            return _f

        mo.register(
            items1 = mo.mzip(itemsfn, [('order_items', 'prod_id'), ('products', 'prod_id')]),
            items2 = mo.mzip(itemsfn, [('order_items', 'prod_id'), ('products', 'prod_id')], stop_short=True)
        )
        mo.run()

        self.assertEqual(len(mo.get('items1')), len(mo.get('items2')) + 2)

    def tearDown(self):
        remdb()


class TestParallel(unittest.TestCase):
    def setUp(self):
        initialize()

    def test_simple_parallel_work_group(self):
        def add_yyyy(r):
            r['yyyymm'] = r['orderdate'][:7]
            r['yyyy'] = r['orderdate'][:4]
            yield r

        # You can make it slow using expressions like "time.sleep(1)"
        # And see what happens in '_temp' folder
        def count(rs):
            rs[0]['n'] = len(rs)
            yield rs[0]

        def count1(rs):
            rs1 = [r for r in rs if r['yyyy'] == 1997]
            if rs1:
                rs1[0]['n'] = len(rs1)
                yield rs1[0]

        mo.register(
            orders=mo.load('orders.csv', fn=add_yyyy),
            # you can enforce single-core-proc by passing parallel "False"
            orders1=mo.apply(count, 'orders', by='yyyymm, shipperid'),
            orders1s=mo.apply(count, 'orders', by='yyyymm, shipperid', parallel=True),
            # part of workers do not have work to do, sort of a corner case
            orders2=mo.apply(count1, 'orders', by='yyyymm, shipperid'),
            orders2s=mo.apply(count1, 'orders', by='yyyymm, shipperid', parallel=True),
            # one column should work as well
            orders3=mo.apply(count, 'orders', by='yyyymm'),
            orders3s=mo.apply(count, 'orders', by='yyyymm', parallel=True),
        )

        mo.run()
        self.assertEqual(list(mo.get('orders1')), list(mo.get('orders1s')))
        self.assertEqual(list(mo.get('orders2')), list(mo.get('orders2s')))
        self.assertEqual(list(mo.get('orders3')), list(mo.get('orders3s')))

    def test_simple_parallel_work_non_group(self):
        def first_name(r):
            r['first_name'] = r['CustomerName'].split()[0]
            yield r

        def first_name1(r):
            if isinstance(r['PostalCode'], int):
                r['first_name'] = r['CustomerName'].split()[0]
                yield r

        mo.register(
            customers=mo.load('customers.csv'),
            customers1=mo.apply(first_name, 'customers'),
            customers1s=mo.apply(first_name, 'customers', parallel=4),

            customers2=mo.apply(first_name1, 'customers'),
            customers2s=mo.apply(first_name1, 'customers', parallel=3),

        )
        mo.run()

        self.assertEqual(list(mo.get('customers1')), list(mo.get('customers1s')))
        self.assertEqual(list(mo.get('customers2')), list(mo.get('customers2s')))

    def test_parallel_apply_with_get(self):
        def orders1():
            d = {}
            for r in mo.get('customers'):
                d[r['CustomerID']] = r['CustomerName']
            def _f(r):
                r['customer_name'] = d.get(r['customerid'], '')
                return r
            return _f

        mo.register(
            customers=mo.load('customers.csv'),
            orders=mo.load('orders.csv'),
            orders1=mo.apply(orders1, 'orders'),
            orders2=mo.apply(orders1, 'orders', parallel=True),
        )

        mo.run()

        names1 = [r['customer_name'] for r in mo.get('orders1') if r['customer_name']]
        names2 = [r['customer_name'] for r in mo.get('orders2') if r['customer_name']]
        self.assertEqual(len(names1), len(mo.get('orders')))
        self.assertEqual(names1, names2)

    def tearDown(self):
        remdb()


class TestLogMsg(unittest.TestCase):
    def test_mute_log_messages(self):
        remdb()
        mo.register(
            orders=mo.load('orders.csv'),
            orders1=mo.apply(lambda r: r, 'orders'),
        )
        self.assertEqual(mo.mapon._CONFIG['msg'], True)
        # you can pass keyword args for configuration
        mo.run(msg=False)
        self.assertEqual(mo.mapon._CONFIG['msg'], True)
        remdb()


class TestRun(unittest.TestCase):
    def test_refresh(self):
        mo.register(
            orders=mo.load('orders.csv'),
            products=mo.load('products.csv'),
        )
        mo.run()

        mo.mapon._JOBS = {}
        mo.register(
            orders=mo.load('products.csv')
        )
        mo.run(refresh='orders')
        self.assertEqual(len(mo.get('orders')), len(mo.get('products')))

    def test_export(self):
        initialize()
        if os.path.exists('orders_sample.csv'):
            os.remove('orders_sample.csv')

        mo.register(
            orders_sample=mo.load('orders.csv'),
        )
        mo.run(export='orders_sample')

        mo.register(
            foo=mo.load('orders_sample.csv'),
        )
        mo.run()

        self.assertEqual(mo.get('orders_sample'), mo.get('foo'))

        if os.path.exists('orders_sample.csv'):
            os.remove('orders_sample.csv')

    # You can export as xlsx, it has advantages when you are dealing with unicode files
    # and also you may find csv insecure sometimes
    def test_export_xlsx(self):
        initialize()
        if os.path.exists('orders_sample.xlsx'):
            os.remove('orders_sample.xlsx')

        mo.register(
            orders_sample=mo.load('orders.csv'),
        )
        mo.run(export='orders_sample.xlsx')
        mo.register(
            foo=mo.load('orders_sample.xlsx'),
        )
        mo.run()

        self.assertEqual(mo.get('orders_sample'), mo.get('foo'))
        if os.path.exists('orders_sample.xlsx'):
            os.remove('orders_sample.xlsx')

# read & write not tested

class TestException(unittest.TestCase):
    pass


# utils
# def nlines_file(name):
#     with open(name) as f:
#         return len(f.readlines())


if __name__ == "__main__":
    unittest.main()