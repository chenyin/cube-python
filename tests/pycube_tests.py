from nose.tools import *
from os.path import dirname, abspath, join
import sys
#PWD = dirname(abspath(__file__))
#sys.path.append(dirname(dirname(PWD)))

from cube import pycube
import datetime

collector = None
evaluator = None

def setup():
    print "SETUP!"
    global collector, evaluator
    collector = pycube.Collector("localhost", 1080)
    evaluator = pycube.Evaluator("localhost", 1081)

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"
    demos = evaluator.event("demo", stop=datetime.datetime.now().isoformat())
    n_demos = len(demos)

    data = {'status':200}
    ce = pycube.CubeEvent("demo", data, datetime.datetime.now().isoformat())

    status = collector.send(ce)
    assert status
    
    demos = evaluator.event("demo", stop=datetime.datetime.now().isoformat())
    assert len(demos) == n_demos + 1

    stats = evaluator.metric("sum(demo.eq(status,200))", stop=datetime.datetime.now().isoformat(), step = pycube.CUBE_DAY, limit = 10)
    assert len(stats) == 11
