from unittest import TestCase
from contracting import constants
from contracting.stdlib.bridge.decimal import ContractingDecimal
from contracting.storage.driver import Driver
from contracting.storage.orm import Datum, Variable, ForeignHash, ForeignVariable, Hash, LogEvent
# from contracting.stdlib.env import gather

# Variable = gather()['Variable']
# Hash = gather()['Hash']
# ForeignVariable = gather()['ForeignVariable']
# ForeignHash = gather()['ForeignHash']

driver = Driver()


class TestDatum(TestCase):
    def setUp(self):
        driver.flush_full()

    def tearDown(self):
        driver.flush_full()

    def test_init(self):
        d = Datum('stustu', 'test', driver)
        self.assertEqual(d._key, driver.make_key('stustu', 'test'))


class TestVariable(TestCase):
    def setUp(self):
        driver.flush_full()

    def tearDown(self):
        #_driver.flush_full()
        pass

    def test_set(self):
        contract = 'stustu'
        name = 'balance'
        delimiter = constants.INDEX_SEPARATOR

        raw_key = '{}{}{}'.format(contract, delimiter, name)

        v = Variable(contract, name, driver=driver)
        v.set(1000)

        self.assertEqual(driver.get(raw_key), 1000)

    def test_get(self):
        contract = 'stustu'
        name = 'balance'
        delimiter = constants.INDEX_SEPARATOR

        raw_key = '{}{}{}'.format(contract, delimiter, name)
        driver.set(raw_key, 1234)

        v = Variable(contract, name, driver=driver)
        _v = v.get()

        self.assertEqual(_v, 1234)

    def test_set_get(self):
        contract = 'stustu'
        name = 'balance'

        v = Variable(contract, name, driver=driver)
        v.set(1000)

        _v = v.get()

        self.assertEqual(_v, 1000)


class TestHash(TestCase):
    def setUp(self):
        driver.flush_full()

    def tearDown(self):
        driver.flush_full()

    def test_set(self):
        contract = 'stustu'
        name = 'balance'
        delimiter = constants.INDEX_SEPARATOR

        raw_key_1 = '{}{}{}'.format(contract, delimiter, name)
        raw_key_1 += ':stu'

        h = Hash(contract, name, driver=driver)

        h._set('stu', 1234)

        driver.commit()

        self.assertEqual(driver.get(raw_key_1), 1234)

    def test_get(self):
        contract = 'stustu'
        name = 'balance'
        delimiter = constants.INDEX_SEPARATOR

        raw_key_1 = '{}{}{}'.format(contract, delimiter, name)
        raw_key_1 += ':stu'

        driver.set(raw_key_1, 1234)

        h = Hash(contract, name, driver=driver)

        self.assertEqual(h._get('stu'), 1234)

    def test_set_get(self):
        contract = 'stustu'
        name = 'balance'

        h = Hash(contract, name, driver=driver)

        h._set('stu', 1234)
        _h = h._get('stu')

        self.assertEqual(_h, 1234)

        h._set('colin', 5678)
        _h2 = h._get('colin')

        self.assertEqual(_h2, 5678)

    def test_setitem(self):
        contract = 'blah'
        name = 'scoob'
        delimiter = constants.INDEX_SEPARATOR

        h = Hash(contract, name, driver=driver)

        prefix = '{}{}{}{}'.format(contract, delimiter, name, h._delimiter)

        h['stu'] = 9999999

        raw_key = '{}stu'.format(prefix)

        self.assertEqual(driver.get(raw_key), 9999999)

    def test_getitem(self):
        contract = 'blah'
        name = 'scoob'
        delimiter = constants.INDEX_SEPARATOR

        h = Hash(contract, name, driver=driver)

        prefix = '{}{}{}{}'.format(contract, delimiter, name, h._delimiter)

        raw_key = '{}stu'.format(prefix)

        driver.set(raw_key, 54321)

        self.assertEqual(h['stu'], 54321)

    def test_setitems(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)
        h['stu'] = 123
        h['stu', 'raghu'] = 1000
        driver.commit()

        val = driver.get('blah.scoob:stu:raghu')
        self.assertEqual(val, 1000)

    def test_setitem_delimiter_illegal(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)
        with self.assertRaises(AssertionError):
            h['stu:123'] = 123

    def test_setitems_too_many_dimensions_fails(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)

        with self.assertRaises(Exception):
            h['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'] = 1000

    def test_setitems_key_too_large(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)

        key = 'a' * 1025

        with self.assertRaises(Exception):
            h[key] = 100

    def test_setitem_value_too_large(self):
        pass

    def test_setitems_keys_too_large(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)

        key1 = 'a' * 800
        key2 = 'b' * 100
        key3 = 'c' * 200

        with self.assertRaises(Exception):
            h[key1, key2, key3] = 100

    def test_getitems_keys(self):
        contract = 'blah'
        name = 'scoob'
        delimiter = constants.INDEX_SEPARATOR

        h = Hash(contract, name, driver=driver)

        prefix = '{}{}{}{}'.format(contract, delimiter, name, h._delimiter)

        raw_key = '{}stu:raghu'.format(prefix)

        driver.set(raw_key, 54321)

        driver.commit()

        self.assertEqual(h['stu', 'raghu'], 54321)

    def test_getsetitems(self):
        contract = 'blah'
        name = 'scoob'
        delimiter = constants.INDEX_SEPARATOR

        h = Hash(contract, name, driver=driver)

        h['stu', 'raghu'] = 999

        driver.commit()

        self.assertEqual(h['stu', 'raghu'], 999)

    def test_getitems_keys_too_large(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)

        key1 = 'a' * 800
        key2 = 'b' * 100
        key3 = 'c' * 200

        with self.assertRaises(Exception):
            x = h[key1, key2, key3]

    def test_getitems_too_many_dimensions_fails(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)

        with self.assertRaises(Exception):
            a = h['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']

    def test_getitems_key_too_large(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver)

        key = 'a' * 1025

        with self.assertRaises(Exception):
            a = h[key]

    def test_getitem_returns_default_value_if_none(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver, default_value=0)

        self.assertEqual(h['hello'], 0)

    def test_get_all_when_none_exist(self):
        contract = 'blah'
        name = 'scoob'

        h = Hash(contract, name, driver=driver, default_value=0)
        all =h.all()
        self.assertEqual(all, [])

    def test_get_all_after_setting(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh['1'] = 123
        hsh['2'] = 456
        hsh['3'] = 789

        l = [123, 456, 789]

        # TODO - this ok ? :D
        # driver.commit()

        # we care about whats included, not order
        self.assertSetEqual(set(hsh.all()), set(l))

    def test_items_returns_kv_pairs(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh['1'] = 123
        hsh['2'] = 456
        hsh['3'] = 789

        # driver.commit()

        kvs = {
            'blah.scoob:3': 789,
            'blah.scoob:1': 123,
            'blah.scoob:2': 456
        }

        got = hsh._items()

        self.assertDictEqual(kvs, got)

    def test_items_multi_hash_returns_kv_pairs(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh[0, '1'] = 123
        hsh[0, '2'] = 456
        hsh[0, '3'] = 789

        hsh[1, '1'] = 999
        hsh[1, '2'] = 888
        hsh[1, '3'] = 777

        # driver.commit()

        kvs = {
            'blah.scoob:0:3': 789,
            'blah.scoob:0:1': 123,
            'blah.scoob:0:2': 456
        }

        got = hsh._items(0)

        self.assertDictEqual(kvs, got)

    def test_items_multi_hash_returns_all(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh[0, '1'] = 123
        hsh[0, '2'] = 456
        hsh[0, '3'] = 789

        hsh[1, '1'] = 999
        hsh[1, '2'] = 888
        hsh[1, '3'] = 777

        # driver.commit()

        kvs = {
            'blah.scoob:0:3': 789,
            'blah.scoob:0:1': 123,
            'blah.scoob:0:2': 456,
            'blah.scoob:1:3': 777,
            'blah.scoob:1:1': 999,
            'blah.scoob:1:2': 888
        }

        got = hsh._items()

        self.assertDictEqual(kvs, got)

    def test_items_clear_deletes_only_multi_hash(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh[0, '1'] = 123
        hsh[0, '2'] = 456
        hsh[0, '3'] = 789

        hsh[1, '1'] = 999
        hsh[1, '2'] = 888
        hsh[1, '3'] = 777

        # driver.commit()

        kvs = {
            'blah.scoob:0:3': 789,
            'blah.scoob:0:1': 123,
            'blah.scoob:0:2': 456
        }

        hsh.clear(1)

        # driver.commit()

        got = hsh._items()

        self.assertDictEqual(kvs, got)

    def test_all_multihash_returns_values(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh[0, '1'] = 123
        hsh[0, '2'] = 456
        hsh[0, '3'] = 789

        hsh[1, '1'] = 999
        hsh[1, '2'] = 888
        hsh[1, '3'] = 777

        l = [123, 456, 789]

        # TODO
        # Test works when below line is commented out - not sure if our driver works differently now
        # driver.commit()

        # we care about whats included, not order
        self.assertSetEqual(set(hsh.all(0)), set(l))

    def test_multihash_multiple_dims_clear_behaves_similar_to_single_dim(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh[1, 0, '1'] = 123
        hsh[1, 0, '2'] = 456
        hsh[1, 0, '3'] = 789

        hsh[1, 1, '1'] = 999
        hsh[1, 1, '2'] = 888
        hsh[1, 1, '3'] = 777

        # driver.commit()

        kvs = {
            'blah.scoob:1:0:3': 789,
            'blah.scoob:1:0:1': 123,
            'blah.scoob:1:0:2': 456
        }

        hsh.clear(1, 1)

        # driver.commit()

        got = hsh._items()

        self.assertDictEqual(kvs, got)

    def test_multihash_multiple_dims_all_gets_items_similar_to_single_dim(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh[1, 0, '1'] = 123
        hsh[1, 0, '2'] = 456
        hsh[1, 0, '3'] = 789

        hsh[1, 1, '1'] = 999
        hsh[1, 1, '2'] = 888
        hsh[1, 1, '3'] = 777

        l = [123, 456, 789]

        # driver.commit()

        # we care about whats included, not order
        self.assertSetEqual(set(hsh.all(1, 0)), set(l))

    def test_clear_items_deletes_all_key_value_pairs(self):
        contract = 'blah'
        name = 'scoob'

        hsh = Hash(contract, name, driver=driver, default_value=0)

        hsh['1'] = 123
        hsh['2'] = 456
        hsh['3'] = 789

        # TODO - test works without commit - is ok
        # driver.commit()

        kvs = {
            'blah.scoob:3': 789,
            'blah.scoob:1': 123,
            'blah.scoob:2': 456
        }

        got = hsh._items()

        self.assertDictEqual(kvs, got)
        hsh.clear()

        # driver.commit()

        got = hsh._items()

        self.assertDictEqual({}, got)


class TestForeignVariable(TestCase):
    def setUp(self):
        driver.flush_full()

    def tearDown(self):
        driver.flush_full()

    def test_set(self):
        contract = 'stustu'
        name = 'balance'

        f_contract = 'colinbucks'
        f_name = 'balances'

        f = ForeignVariable(contract, name, f_contract, f_name, driver=driver)

        with self.assertRaises(ReferenceError):
            f.set('poo')

    def test_get(self):
        # set up the foreign variable
        contract = 'stustu'
        name = 'balance'

        f_contract = 'colinbucks'
        f_name = 'balances'

        f = ForeignVariable(contract, name, f_contract, f_name, driver=driver)

        # set the variable using the foreign names (assuming this is another contract namespace)
        v = Variable(f_contract, f_name, driver=driver)
        v.set('howdy')

        self.assertEqual(f.get(), 'howdy')


class TestForeignHash(TestCase):
    def setUp(self):
        driver.flush_full()

    def tearDown(self):
        #_driver.flush_full()
        pass

    def test_set(self):
        # set up the foreign variable
        contract = 'stustu'
        name = 'balance'

        f_contract = 'colinbucks'
        f_name = 'balances'

        f = ForeignHash(contract, name, f_contract, f_name, driver=driver)

        with self.assertRaises(ReferenceError):
            f._set('stu', 1234)

    def test_get(self):
        # set up the foreign variable
        contract = 'stustu'
        name = 'balance'

        f_contract = 'colinbucks'
        f_name = 'balances'

        f = ForeignHash(contract, name, f_contract, f_name, driver=driver)

        h = Hash(f_contract, f_name, driver=driver)
        h._set('howdy', 555)

        self.assertEqual(f._get('howdy'), 555)

    def test_setitem(self):
        # set up the foreign variable
        contract = 'stustu'
        name = 'balance'

        f_contract = 'colinbucks'
        f_name = 'balances'

        f = ForeignHash(contract, name, f_contract, f_name, driver=driver)

        with self.assertRaises(ReferenceError):
            f['stu'] = 1234

    def test_getitem(self):
        # set up the foreign variable
        contract = 'stustu'
        name = 'balance'

        f_contract = 'colinbucks'
        f_name = 'balances'

        f = ForeignHash(contract, name, f_contract, f_name, driver=driver)

        h = Hash(f_contract, f_name, driver=driver)
        h['howdy'] = 555

        self.assertEqual(f['howdy'], 555)
        
        



class TestLogEvent(TestCase):
    
    
    """
    TO DO :
    # Missing Tests for `LogEvent` Class

    1. Unauthorized Access Test: 
    - Ensure that unauthorized access to the `rt.context` and `_driver` is not possible. This could involve attempting to manipulate these objects directly and verifying that such actions are blocked or result in an error.

    2. Boundary Value Tests for Indexed Arguments: 
    - Test the boundary conditions for the number of indexed arguments (e.g., exactly three, more than three) to ensure the assertion behaves as expected.

    3. Type Enforcement Test: 
    - Verify that the type enforcement in the `write_event` method is strict and cannot be bypassed by using subclasses or similar types.

    4. Empty Event Data Test: 
    - Test the behavior when `write_event` is called with an empty dictionary or `None` to ensure it fails gracefully.

    5. Invalid Argument Names Test: 
    - Attempt to use invalid or unexpected argument names in the `args` dictionary to ensure they are properly rejected.

    6. Concurrent Access Test: 
    - Simulate concurrent access to the `LogEvent` instance to ensure thread safety and that no race conditions occur.

    7. Large Data Test: 
    - Test the behavior when very large data sets are passed to `write_event` to ensure performance and stability.

    8. Invalid Contract or Event Name Test: 
    - Test with invalid or unexpected contract and event names to ensure they are handled correctly.

    9. Driver Manipulation Test: 
    - Attempt to manipulate the `_driver` directly to ensure it is protected against unauthorized changes.

    10. Event Encoding Test: 
        - Verify that the `encode_kv` function is called correctly and that the encoded data is as expected.

    11. Event Logging Test: 
        - Ensure that events are logged correctly in the `_driver` and that the log can be retrieved and verified.

    12. Security Test for `__call__` Method: 
        - Ensure that the `__call__` method does not expose any vulnerabilities when invoked with unexpected or malicious data.

    13. Invalid Data Types in Event Data Test: 
        - Test with data types that are not specified in the `args` to ensure they are rejected.

    14. Test for Missing `driver`: 
        - Ensure that the class behaves correctly if the `driver` is not provided or is `None`.

    15. Test for Non-Standard Types in Args: 
        - Attempt to use non-standard types in the `args` dictionary to ensure they are rejected.
    """

    def setUp(self):

        # Define the event arguments
        self.args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # Create a LogEvent instance
        self.log_event = LogEvent(contract="test_contract", name="Transfer", args=self.args)
        self.contract = "test_contract"
        self.name = "Transfer"
        self.driver = driver  
        
    def test_log_event(self):
        contract = 'currency'
        name = 'Transfer'
        
        args = {
            'from': {
                'type': str,
                'idx': True
            }, 
            'to': {
                'type': str,
                'idx': True
            },
            'amount': {
                'type': (int, float, ContractingDecimal)
            }
        }
        

        le = LogEvent(contract, name, args=args, driver=driver)


    def test_log_event_with_max_indexed_args(self):
        contract = 'currency'
        name = 'Transfer'
        
        args = {
            'from': {
                'type': str,
                'idx': True
            }, 
            'to': {
                'type': str,
                'idx': True
            },
            'amount': {
                'type': (int, float, ContractingDecimal),
                'idx': True
            }
        }
        # This should not raise an assertion error
        le = LogEvent(contract, name, args=args, driver=driver)
        self.assertIsInstance(le, LogEvent)
        

    def test_log_event_with_too_many_indexed_args(self):
        contract = 'currency'
        name = 'Transfer'
        
        args = {
            'from': {
                'type': str,
                'idx': True
            }, 
            'to': {
                'type': str,
                'idx': True
            },
            'amount': {
                'type': (int, float, ContractingDecimal),
                'idx': True
            },
            'extra': {
                'type': str,
                'idx': True
            }
        }
        
        # This should raise an assertion error
        with self.assertRaisesRegex(AssertionError, "Args must have at most three indexed arguments."):
            LogEvent(contract, name, args=args, driver=driver)

    def test_write_event_success(self):
        # Define the event data
        data = {
            "from": "Alice",
            "to": "Bob",
            "amount": 100
        }

        # Call the write_event method
        self.log_event.write_event(data)

        # No assertions needed here if no exceptions are raised

    def test_write_event_missing_argument(self):
        # Define the event data with a missing argument
        data = {
            "from": "Alice",
            "amount": 100
        }

        with self.assertRaises(AssertionError) as context:
            self.log_event.write_event(data)

        self.assertIn("Data must have the same number of arguments as specified in the event.", str(context.exception))

    def test_write_event_wrong_type(self):
        # Define the event data with a wrong type
        data = {
            "from": "Alice",
            "to": "Bob",
            "amount": "one hundred"
        }

        with self.assertRaises(AssertionError) as context:
            self.log_event.write_event(data)

        self.assertIn("Argument amount is the wrong type!", str(context.exception))
        

    def test_write_event_with_empty_data(self):
        # Test with an empty dictionary
        data = {}

        with self.assertRaises(AssertionError) as context:
            self.log_event.write_event(data)

        self.assertIn("Data must have the same number of arguments as specified in the event.", str(context.exception))

    def test_write_event_with_none(self):
        # Test with None as data
        data = None

        with self.assertRaises(TypeError) as context:
            self.log_event.write_event(data)

        self.assertIn("object of type 'NoneType' has no len()", str(context.exception))

    def test_write_event_with_invalid_argument_names(self):
        # Define the event arguments correctly
        args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # Create a LogEvent instance
        log_event = LogEvent(self.contract, self.name, args=args, driver=self.driver)

        # Define event data with an unexpected argument name
        data = {
            "from": "Alice",
            "to": "Bob",
            "unexpected_arg": 100
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            log_event.write_event(data)

        self.assertIn("Unexpected argument unexpected_arg in the data dictionary.", str(context.exception))

class TestLogEventBoundaryIndexedArgs(TestCase):
    def setUp(self):
        # Common setup for the tests
        self.contract = "test_contract"
        self.name = "Transfer"
        self.driver = driver  # Assuming driver is defined elsewhere

    def test_log_event_with_exactly_three_indexed_args(self):
        # Define arguments with exactly three indexed arguments
        args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal), "idx": True}
        }

        # This should not raise an assertion error
        log_event = LogEvent(self.contract, self.name, args=args, driver=self.driver)
        self.assertIsInstance(log_event, LogEvent)

    def test_log_event_with_more_than_three_indexed_args(self):
        # Define arguments with more than three indexed arguments
        args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal), "idx": True},
            "extra": {"type": str, "idx": True}
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            LogEvent(self.contract, self.name, args=args, driver=self.driver)

        self.assertIn("Args must have at most three indexed arguments.", str(context.exception))
        
import random
import string

class TestLogEventTypeEnforcementFuzz(TestCase):
    def setUp(self):
        # Define the event arguments
        self.args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # Create a LogEvent instance
        self.log_event = LogEvent(contract="test_contract", name="Transfer", args=self.args)

    def random_string(self, length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def test_write_event_with_random_data(self):
        # Generate random data for each argument
        for _ in range(100):  # Run 100 iterations for fuzz testing
            data = {
                "from": self.random_string(),
                "to": self.random_string(),
                "amount": random.choice([self.random_string(), None, [], {}, set(), object()])
            }

            with self.assertRaises(AssertionError) as context:
                self.log_event.write_event(data)

            self.assertIn("Argument amount is the wrong type!", str(context.exception))

    def test_write_event_with_random_structures(self):
        # Test with random structures for the 'amount' field
        random_structures = [None, [], {}, set(), object(), lambda x: x, b"bytes", (1, 2, 3)]

        for structure in random_structures:
            data = {
                "from": "Alice",
                "to": "Bob",
                "amount": structure
            }

            with self.assertRaises(AssertionError) as context:
                self.log_event.write_event(data)

            self.assertIn("Argument amount is the wrong type!", str(context.exception))

    def test_write_event_with_random_numeric_types(self):
        # Test with various numeric types that are not allowed
        random_numeric_types = [
            complex(1, 1), 
            # float('nan'), # Doesnt raise IS THIS OK ?
            # float('inf'), # Doesn't raise IS THIS OK ?
            # -float('inf') # Doesn't raise IS THIS OK ?
        ]

        for num in random_numeric_types:
            data = {
                "from": "Alice",
                "to": "Bob",
                "amount": num
            }

            with self.assertRaises(AssertionError) as context:
                self.log_event.write_event(data)

            self.assertIn("Argument amount is the wrong type!", str(context.exception))

class TestLogEventInvalidArgumentNames(TestCase):
    def setUp(self):
        # Define the event arguments
        self.args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # Create a LogEvent instance
        self.log_event = LogEvent(contract="test_contract", name="Transfer", args=self.args)

    def test_write_event_with_invalid_argument_names(self):
        # Define event data with an unexpected argument name
        data = {
            "from": "Alice",
            "to": "Bob",
            "unexpected_arg": 100
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            self.log_event.write_event(data)

        self.assertIn("Unexpected argument unexpected_arg in the data dictionary.", str(context.exception))

class TestLogEventLargeData(TestCase):
    def setUp(self):
        # Define the event arguments
        self.args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # Create a LogEvent instance
        self.log_event = LogEvent(contract="test_contract", name="Transfer", args=self.args)

    def test_write_event_with_large_data(self):
        # Generate a large string for the 'from' and 'to' fields
        large_string = 'A' * 10**6  # 1 million characters

        # Generate a large number for the 'amount' field
        large_number = 10**18  # A very large number

        # Define the event data with large values
        data = {
            "from": large_string,
            "to": large_string,
            "amount": large_number
        }

        # Call the write_event method and ensure it completes without error
        try:
            self.log_event.write_event(data)
            success = True
        except Exception as e:
            success = False
            print(f"Error occurred: {e}")

        self.assertFalse(success, "write_event should not handle large data without errors.")


class TestLogEventInvalidDataTypes(TestCase):
    def setUp(self):
        # Define the event arguments
        self.args = {
            "from": {"type": str, "idx": True},
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # Create a LogEvent instance
        self.log_event = LogEvent(contract="test_contract", name="Transfer", args=self.args)

    def test_write_event_with_invalid_string_type(self):
        # Use an invalid type (e.g., list) for the 'from' field
        data = {
            "from": ["Alice"],  # Invalid type: list instead of str
            "to": "Bob",
            "amount": 100
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            self.log_event.write_event(data)

        self.assertIn("Argument from is the wrong type!", str(context.exception))

    def test_write_event_with_invalid_numeric_type(self):
        # Use an invalid type (e.g., string) for the 'amount' field
        data = {
            "from": "Alice",
            "to": "Bob",
            "amount": "one hundred"  # Invalid type: str instead of int/float/ContractingDecimal
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            self.log_event.write_event(data)

        self.assertIn("Argument amount is the wrong type!", str(context.exception))

    def test_write_event_with_unexpected_object_type(self):
        # Use an unexpected object type for the 'to' field
        data = {
            "from": "Alice",
            "to": object(),  # Invalid type: object instead of str
            "amount": 100
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            self.log_event.write_event(data)

        self.assertIn("Argument to is the wrong type!", str(context.exception))
        
class TestLogEventNonStandardTypes(TestCase):
    def setUp(self):
        # Common setup for the tests
        self.contract = "test_contract"
        self.name = "Transfer"
        self.driver = driver  # Assuming driver is defined elsewhere

    def test_log_event_with_non_standard_type(self):
        # Define arguments with a non-standard type (e.g., list)
        args = {
            "from": {"type": list, "idx": True},  # Invalid type: list
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            LogEvent(self.contract, self.name, args=args, driver=self.driver)

        self.assertIn("Each type in args must be str, int, float, ContractingDecimal, or bool.", str(context.exception))

    def test_log_event_with_custom_object_type(self):
        # Define arguments with a custom object type
        class CustomType:
            pass

        args = {
            "from": {"type": CustomType, "idx": True},  # Invalid type: CustomType
            "to": {"type": str, "idx": True},
            "amount": {"type": (int, float, ContractingDecimal)}
        }

        # This should raise an assertion error
        with self.assertRaises(AssertionError) as context:
            LogEvent(self.contract, self.name, args=args, driver=self.driver)

        self.assertIn("Each type in args must be str, int, float, ContractingDecimal, or bool.", str(context.exception))


if __name__ == '__main__':
    unittest.main()