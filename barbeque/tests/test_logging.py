from barbeque.logging import get_logger, logged


def test_func():
    pass


class TestClass(object):
    def test(self):
        pass


class TestGetLogger:
    def test_function(self):
        logger = get_logger(test_func)
        assert logger.name == 'barbeque.tests.test_logging.test_func'

    def test_class(self):
        logger = get_logger(TestClass)
        assert logger.name == 'barbeque.tests.test_logging.TestClass'

    def test_method_unbound(self):
        logger = get_logger(TestClass.test)
        assert logger.name == 'barbeque.tests.test_logging.TestClass.test'

    def test_method_bound(self):
        logger = get_logger(TestClass().test)
        assert logger.name == 'barbeque.tests.test_logging.TestClass.test'

    def test_string(self):
        logger = get_logger('test123')
        assert logger.name == 'test123'

    def test_fallback(self):
        logger = get_logger(None)
        assert logger.name == 'root'


class TestLoggedDecorator:

    def test_simple(self):
        @logged
        class Dummy:
            def foo(self):
                pass

        obj = Dummy()
        assert obj.logger
        assert obj.logger.name == 'barbeque.tests.test_logging.Dummy'
