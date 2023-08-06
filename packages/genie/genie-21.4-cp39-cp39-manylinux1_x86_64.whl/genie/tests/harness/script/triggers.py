from pyats import aetest
from genie.harness.base import Trigger

def prepostprocessor(section):
    pass

def processorwithparam(section, param1):
    pass

def exceptionprocessor(section, exc_type, exc_value, exc_traceback):
    pass

class TriggerShutNoShutBgp(Trigger):
    @aetest.test
    def test1(self):
        pass

class TriggerShutNoShutOspf(Trigger):
    @aetest.test
    def test1(self):
        pass
    @aetest.test
    def test2(self):
        pass

class Bad(object):
    @aetest.test
    def test1(self):
        pass

class Wrong(object):
    pass

class TriggerBgpNoSetupCleanup(Trigger):
    @aetest.test
    def test1(self):
        pass
    @aetest.test
    def test2(self):
        pass

class TriggerOspfWtSetupCleanup(Trigger):
    @aetest.setup
    def test_setup(self):
        pass
    @aetest.test
    def test1(self):
        pass
    @aetest.cleanup
    def test_cleanup(self):
        pass

class TriggerHsrpWtSetup(Trigger):
    @aetest.setup
    def test_setup(self):
        pass
    @aetest.test
    def test1(self):
        pass

class TriggerVlanWtCleanup(Trigger):
    @aetest.test
    def test1(self):
        pass
    @aetest.cleanup
    def test_cleanup(self):
        pass

class TriggerIsisBasic(Trigger):
    pass

class TriggerWtJustSetupCleanup(Trigger):
    @aetest.setup
    def test_setup(self):
        pass
    @aetest.cleanup
    def test_cleanup(self):
        pass

class TriggerMixedOrder(Trigger):
    @aetest.test
    def test1(self):
        pass
    @aetest.test
    def test2(self):
        pass
    @aetest.cleanup
    def test_cleanup(self):
        pass
    @aetest.setup
    def test_setup(self):
        pass

class TriggerNoDecorator(Trigger):
    @aetest.setup
    def test_setup(self):
        pass
    # test without decorator
    def test1(self):
        pass
    @aetest.test
    def test2(self):
        pass
    @aetest.cleanup
    def test_cleanup(self):
        pass

@aetest.loop(uids=['Test1', 'Test2', 'Test3'])
class TriggerAetestLoop(Trigger):
    @aetest.test
    def test(self):
        pass