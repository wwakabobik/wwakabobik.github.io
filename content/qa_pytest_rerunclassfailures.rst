################################
Test classes - how to rerun them
################################
:date: 2024-08-21 13:44
:author: wwakabobik
:tags: qa, python, pytest
:slug: pytest_rerunclassfailures
:category: qa
:status: published
:summary: Dealing with imperfect code and test environments can drive you crazy, especially when you need to properly rerun failed tests while preserving the state of the test environment. How I deal with it using pytest?
:cover: assets/images/bg/qa.png

Hard times call for hard measures. Not every application's architecture and testing environment are ideal. They can be downright bad and inflexible. And to test them, you have to step over a tester's pride and violate the basic principles of software testing.

The problem that doesn't exist
------------------------------

Let's get a crash course on best testing practices.

Firstly, every self-respecting tester should know what a "software testing pyramid" is. Specifically, the number of simple tests, starting from unit tests, should be significantly larger than the subsequent API, then UI, and E2E tests.

.. image:: /assets/images/articles/qa/pytest_rerunclassfailures/pyramid-test-pyramid.jpg
   :alt: Testing pyramid


This is because the cost of developing, executing, and maintaining such tests is lower, they run faster, and usually catch most errors at the earliest stages of development and testing. Meanwhile, the longest tests, which sequentially cover a long sequence of actions and states following business logic - E2E tests usually make up the smallest part of testing. Primarily because all their components have already been (often repeatedly) checked by smaller and simpler tests. Secondly, the truly critical business logic, which E2E tests should be, is usually just a couple of scenarios, which, I believe, with a high degree of probability will make up your smoke set for pre-release testing.

The problem that exists
-----------------------
Well, our world is not perfect. Companies and teams are not perfect, code is not perfect, and honestly, people are not perfect, I would even say, they are a rare kind of crap. And we have to live and work with this.

Suppose you have a test environment with a hundred tests that run in an isolated environment - behind several firewalls (like the one we run tests on, the one where the system is deployed, and the one that launches the tests - our CI server), due to which there is a call to one of the cloud testing platforms. If you have worked with such systems, then you probably know that deploying a virtual machine takes some time, so it doesn't make much sense to break the connection and recreate it for each test. Moreover, even if you use only a few deployed virtual machines, their performance leaves much to be desired. Well, due to the accumulation of internal networks, as well as different regions, this bundle, so to speak, starts to work far from the speed of light.

.. image:: /assets/images/articles/qa/pytest_rerunclassfailures/browserstack.jpg
   :alt: Running test on Browserstack on VMs with video over firewall is pain


Well, running tests becomes slower, but still, no one prevents us from resetting and setting the state for each test inside such a virtual machine. Yes, but... the system is written in such a way that it lacks test handles that can be pulled to set the desired state. Moreover, for UI tests, you can't just go to the desired URL to the desired form, you have to click through several screens. All this takes time, and in the conditions of a test environment, preparing for one test can take 1-2 minutes. This already sounds like a huge problem, especially if we are trying to write tests well, atomically, and the next check is, say, entering a character in a field. A disaster that forces us to either throw out such tests or wait for results for hours.

Here, it seems, it's time to step over our tester's pride and lump several checks into one test. Let's say, now the test will fill in twenty fields and click a button to go to another screen. I think you understand that during input into a field, flipping a checkbox or flipper, something can go wrong - an error can be displayed, for example, text can be lost, and when interacting with another component, the state can change again, and we will surely get not quite a valid result. So, it means we still have to break our check into tests, but at the same time leaving the system state for each of the tests, equal to the previous state. So, we can do this if we reset the context within the session. This is of course good, but then we will raise a virtual machine for a session that combines a sequence of tests every time. Trying to restore atomicity, we will lose performance. Then there is another alternative - to isolate the state by files, and even better - by wrapping tests in test classes. Yes, I forgot to say that I write in python and use pytest, so let's talk about it.

The problem we created
----------------------
So, a good and beautiful atomic test, with which you usually work, looks like this:

.. code-block:: python

    """This module has no class, only test functions"""


    def test_no_class_first():
        """This test always passes"""
        assert True


    def test_no_class_second():
        """This test always fails"""
        assert False


However, for my particular case, we decided to use test classes. They will look something like this:

.. code-block:: python

    class TestBasic:
        """This is a basic test"""

        def test_basic(self):
            """This is basic test 1"""
            assert True

        def test_basic2(self):
            """This is basic test 2"""
            assert False

        def test_basic3(self):
            """This is basic test 3"""
            assert True

Personally, it makes my eyes bleed because I can imagine the problems it will cause me. Although it looks good at first glance. But that's at first glance. If you call the tests as usual:

.. code-block:: bash

    pytest tests


Then the tests will be executed sequentially, and if there was some interdependence in them, it will be preserved.

However, if you try to call the tests in multiple threads (with pytest-xdist), the sequence will be shuffled.

.. code-block:: bash

    pytest tests -n=auto

To avoid this, you need to specify how exactly to group the tests. For this, don't forget to specify the grouping method.

.. code-block:: bash

    pytest test -n=auto --dist loadscope

Now, suppose we have twenty steps, dependent on each other, and we have to go through all of them, even if one of the first tests failed. But there is no point in this anymore, as the state has already been violated. Therefore, we need to somehow implement the "fail fast" logic in this case. For this, we will have to interfere a little with the logic of `pytest` and implement:

.. code-block:: python

    import pytest


    def pytest_runtest_makereport(item, call):
        if "incremental" in item.keywords:
            if call.excinfo is not None:
                parent = item.parent
                parent._previousfailed = item


    def pytest_runtest_setup(item):
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


Now those test classes that need to be failed quickly need to be marked in advance:

.. code-block:: python

    import pytest


    @pytest.mark.incremental
    class TestMarkedFailFast:
        """This test class will fail fast"""

        def test_will_pass(self):
            """This test will pass"""
            assert True

        def test_will_fail(self):
            """This test will fail"""
            assert False

        def test_wont_run(self):
            """This test won’t run"""
            assert True

Another problem we created is the pointlessness of using the `pytest-rerunfailures` plugin. If we decide to use it, the test will be restarted outside the class context with a completely different state than we expected. You can break a bunch of copies on the topic of whether reruns are worth using or not. In the end, we will survive a couple of falls and manually restart before the release. If there are many falls, perhaps something critical has broken, and we will quickly identify the error, and we will have to restart most of the tests anyway. But if you have a lot of tests - thousands, and instability still happens, and time is a pity, if the test, of course, does not regularly unstably fall, then delegate the restart to the machine. But in our case... there are no such options, it turns out?

The problem I solved
--------------------

So, to solve this problem, I wrote the `pytest-rerunclassfailures` plugin.

To install it and start using it, just install it via pip:

.. code-block:: bash

    pip install pytest-rerunclassfailures

To run tests with reruns, just pass the --rerun-class-max parameter with some number of reruns.

.. code-block:: bash

    pytest tests --rerun-class-max=2

Or add it explicitly in `pytest.ini`:

.. code-block:: ini

    [pytest]
    plugins = pytest-rerunclassfailures
    addopts = --rerun-class-max=3


Results of run will look like:

.. image:: /assets/images/articles/qa/pytest_rerunclassfailures/pytest-rerunclassfailures.jpg
   :alt: Output of test run with pytest-rerunclassfailures plugin

You can also set additional parameters, like delay between reruns or logging type:

- `--rerun-class-max` - the number of retries for a failed test class. Default is 0.
- `--rerun-delay` - delay between retries in seconds. Default is 0.5 seconds.
- `--rerun-show-only-last` - show results of only the last retry - there will be no "rerun" in the log, only the last, final run with the final result. Not specified by default.
- `--hide-rerun-details` - remove rerun details (errors and traceback) in the terminal. Not specified by default.

.. code-block:: bash

    PYTHONPATH=. pytest -s tests -p pytest_rerunclassfailures --rerun-class-max=3 --rerun-delay=1 --rerun-show-only-last

The plugin is compatible with `pytest-xdist`, you can use it in multiple threads, but always specify `--dist loadscope`. After an error, the class will be reset to its initial state, however, the next test will fail on restart, as the class state was changed bypassing the constructor inside the function level fixture. However, I hope you don't use this bad practice in your code.

.. code-block:: python

    """Test class with function (fixtures) attributes"""

    from random import choice

    import pytest


    random_attribute_value = choice((42, "abc", None))


    @pytest.fixture(scope="function")
    def function_fixture(request):
        """Fixture to set function attribute"""
        request.cls.attribute = "initial"
        return "initial"


    @pytest.fixture(scope="function")
    def function_fixture_secondary(request):
        """Fixture to set function attribute"""
        request.cls.attribute = "secondary"
        return "secondary"


    class TestFunctionFixturesAttributes:
        """Test class with function params attributes"""

        def test_function_fixtures_attribute_initial(self, function_fixture):  # pylint: disable=W0621
            """Test function fixture attribute at the beginning of the class"""
            assert self.attribute == "initial"
            assert function_fixture == "initial"

        def test_function_fixtures_attribute_recheck(self, function_fixture_secondary):  # pylint: disable=W0621
            """Test function fixture attribute after changing attribute value"""
            assert self.attribute == "secondary"  # type: ignore  # pylint: disable=E0203
            assert function_fixture_secondary == "secondary"
            self.attribute = random_attribute_value  # type: ignore  # pylint: disable=attribute-defined-outside-init
            # attribute is changed, but fixture is not
            assert self.attribute == random_attribute_value
            assert function_fixture_secondary == "secondary"

        def test_function_fixtures_attribute_forced_failure(self):
            """Test function fixture attribute to be forced failure"""
            assert False


A bit of technical details
--------------------------

To be able to intercept and restart test class tests, I interfere with pytest_runtest_protocol and take control if it's a test class:

.. code-block:: python

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_protocol(
        self, item: _pytest.nodes.Item, nextitem: _pytest.nodes.Item
    ) -> bool:

Next, we get the test class, and find its descendants - test functions:

.. code-block:: python

    parent_class = item.getparent(pytest.Class)
    for i in items[items.index(item) + 1 :]:
        if item.cls == i.cls:  # type: ignore
            siblings.append(i)

And then we execute the standard testing protocol for each descendant sequentially:

.. code-block:: python

    for i in range(len(siblings) - 1):
        # Before run, we need to ensure that finalizers are not called (indicated by None in the stack)
        nextitem = siblings[i + 1] if siblings[i + 1] is not None else siblings[0]
        siblings[i].reports = runtestprotocol(siblings[i], nextitem=nextitem, log=False)

And, finally, after determining the test status (how many times we had to restart it and set the result or rerun), we send the results back:

.. code-block:: python

    item.ihook.pytest_runtest_logstart(nodeid=item.nodeid, location=item.location)
    for index, rerun in enumerate(test_class[item.nodeid]):
        self.logger.debug("Reporting node results %s (%s/%s)", item.nodeid, len(test_class[item.nodeid]), index)
        for report in rerun:
            item.ihook.pytest_runtest_logreport(report=report)
    item.ihook.pytest_runtest_logfinish(nodeid=item.nodeid, location=item.location)

If you need to restart the test class, you must definitely do a teardown and recreate the test class in its original form.

.. code-block:: python

    # Drop failed fixtures and cache
    self._remove_cached_results_from_failed_fixtures(item)
    # Clean class setup state stack
    item.session._setupstate.stack = {}  # pylint: disable=protected-access
    self._teardown_test_class(item)  # Teardown the class and emulate recreation of it
    # We can't replace the class because session-scoped fixtures will be lost
    parent_class, siblings = self._recreate_test_class(parent_class, siblings, initial_state)
    item.parent = parent_class  # ensure that we're using updated class

That's all. I hope my plugin will help you a little when you are dealing with bad architectural decisions, bad code, and tests.

Conclusions
-----------

That's all. I hope my plugin will help you a little when you are dealing with bad architectural decisions, bad code, and tests. If you like my article, feel free to `share a coin`_. And, for sure here are links to the `GitHub repo`_ and `pypi package`_.


.. _share a coin: https://www.donationalerts.com/r/rocketsciencegeek
.. _GitHub repo: https://github.com/wwakabobik/pytest-rerunclassfailures
.. _pypi package: https://pypi.org/project/pytest-rerunclassfailures/
