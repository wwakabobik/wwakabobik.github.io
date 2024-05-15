#################
TestRail Reporter
#################
:date: 2024-04-02 10:00
:author: wwakabobik
:tags: qa, python, api, testrail
:slug: testrail_reporter
:category: qa
:status: published
:summary: Reporting results from your automation tests to TestRail is a good idea. Especially for management with KPIs of automation coverage, and some other metrics. Let's automate it and report it to Testrail, Slack, email, etc.
:cover: assets/images/bg/qa.png

TestRail. I get it, this tool isn't the new kid on the block, but it's still rocking the charts as a go-to for manual and—let's face it, more painfully—automated testing. In a perfect world, I would've shared my pro-tips with you sooner, but the real deal is to recognize the need, am I right?

.. image:: /assets/images/articles/qa/testrail_reporter/testrails_0.png
   :alt: TestRail

So, for those code warriors who've battled with TestRail, it's no secret that its convenience as a tracking and automation management tool is, well, up for debate. But as the IT saga goes—you've got this epic test model, a thousand manual tests that you've begun to cover with auto-tests, say with pytest/selenium as your steed. And for some reason, like a manager's whimsy, you need to corral them into "one testing tool". How do you pull that off?

It all hinges on your framework of choice. The quick and dirty fix? Use the `trcli`_ utility from `Gurock`_ and send off those results. There are other paths to victory—tagging or some mapping in your test docstrings with the TestRails field and yanking the API's chain. Bottom line, figure it out. What follows is my saga and my crafted solutions to the challenges faced over five years.

Dispatching Automated Test Results to TestRail
----------------------------------------------
So, after giving `trcli`_ a whirl without much enthusiasm, I've discovered that out of the box, it doesn't quite perform as I had anticipated. I won't bore you with the details of how the API sometimes hangs, spits out results page by page, and other such nuisances... On the flip side, I wasn't keen on using something alien and far removed from the original `Gurock`_ approach. Thus, I decided to craft my own "reporter" with a dash of QA flair and a Pythonic twist.

Here's what we do, we grab and install the package:

.. code-block:: shell

    pip install testrail-api-reporter


All that's needed, just like in the original, is to add the `automation_id` field to the test cases in the TestRail project(s), and then kick off the tests with the junitxml flag, something like this:

.. code-block:: shell

    pytest --junitxml "junit-report.xml" "./tests"

After the tests have run their course, pytest conjures up an xml report with the fruits of the test execution. Now, we need to read it and dispatch it to TestRails:

.. code-block:: python

    url=https://your_tr.testrail.io
    email=your@email.com password=your_password
    project_number=42 test_suite_number=66
    api=TestRailResultsReporter(url=url,
                                email=email,
                                password=password,
                                project_id=project_id,
                                suite_id=test_suite_id,
                                xml_report='junit-report.xml') # And then we simply invoke api.send_results()

As a result, the outcomes will be appended, and a test run akin to: `AT run 2022-09-01T20:25:51` will be created.

.. image:: /assets/images/articles/qa/testrail_reporter/testrails_1.png
   :alt: TestRail test run

Naturally, if there exists a test in TestRail with the `automation_id` field filled out and correctly formatted, like path.to.test_file.test_class.test, then the results will be added for it. Otherwise, the missing tests will be conjured up in the `pytest` folder.

.. image:: /assets/images/articles/qa/testrail_reporter/testrails_2.png
   :alt: New test cases published

In essence, the report can be tailored to your needs by passing parameters to send_results():

- `title` - completely replaces the name of the test run.
- `environment` - the environment, will be tacked on to the end of the run name, like AT run 2022-09-01T20:25:51 on ENV.
- `timestamp` - the time code, will be swapped with the code from the xml report.
- `run_id` - the id of an existing test run; if specified, the results will be added to it, and a new test run will not be created.
- `close_run` - if True, then any test run will be closed, by default True.
- `run_name` - if you don't know the run_id you can find the test run by its name, and then the run_id parameter will be ignored, even if it was specified.
- `delete_old_run` - if a test run with the specified id or name existed before, it will be deleted if True.

Also, it's not necessary to create a separate reporter if you wish to send a report for a different suite, for example, just call api.method_name(), namely:

- `set_project_id(project_id)` - change project id;
- `set_suite_id(suite_id)` - switch suite id;
- `set_xml_filename(xml_filename)` - change the default path to the report;
- `set_at_report_section(section_name)` - change the default folder where the missing tests will be created.


Automated Coverage Report
---------------------------
So, we've figured out how to transfer results to TestRail, but what if we want to gather metrics that aren't available in TestRail, like coverage by automated tests of our test model? About the progress of automation and the like? Our management lives in Confluence, so why not update those beautiful charts right there? Well, there's a solution for that too!

.. code-block:: python

    # Let's create a Confluence Reporter
    confluence_reporter = ConfluenceReporter(username='Liberator',
                                             password='NoWar',
                                             url="https://my.confluence.com",
                                             confluence_page="1234")

    # Now let's create several reports at once!
    confluence_reporter.generate_report(reports=automation_distribution,
                                        cases=area_distribution,
                                        values=priority_distribution,
                                        type_platforms=my_platforms,
                                        automation_platforms=my_automation_platforms)

    # Or each report separately
    confluence_reporter.history_type_chart(type_platforms=my_platforms)  # historical chart of automation coverage by platforms
    confluence_reporter.history_state_chart(automation_platforms=my_automation_platforms)  # historical chart of test coverage by attribute
    confluence_reporter.test_case_area_distribution(cases=area_distribution)  # chart of test distribution by platforms (pie chart)
    confluence_reporter.test_case_priority_distribution(values=priority_distribution)  # chart of test breakdown by priority (pie chart)
    confluence_reporter.automation_state(reports=automation_distribution)  # chart of automated coverage by platforms (bar chart)

.. image:: /assets/images/articles/qa/testrail_reporter/testrails_3.png
   :alt: TestRail summary charts

Okay, maybe some explanations are needed about where all this comes from. Of course, the data is taken from TestRail. You can get the data like this:

.. code-block:: python

    testrails_adapter = ATCoverageReporter(url=tr_url, email=tr_client_email, password=tr_client_password,
                                   project=tr_default_project, priority=4, type_platforms=my_platforms,
                                   automation_platforms=automation_platforms)

    # Now let's get the results for each type
    values = tr_reporter.test_case_by_priority()
    cases = tr_reporter.test_case_by_type()
    reports = tr_reporter.automation_state_report()

Alright, but it's still unclear what "platforms" are? Platforms are sections (TestRail folders), or even their combinations/intersections, from which we take the data. That is, we may have common tests for the functionality of our product, as well as different, specific ones for each of the platforms (for example, mobile/desktop browsers).

.. code-block:: python

    # You need to specify the top section(s) (folder(s) where tests for each of your platforms are stored,
    # the reporter will recursively collect all tests in nested folders.
    # You also need to specify the field name by which automation affiliation will be selected,
    # by default 'internal_name' is used, namely 'type_id'.
    # By default, these are values like "Automated", "Functional", "Other", etc.

    automation_platforms = (
        {'name': 'Desktop Chrome', 'internal_name': 'type_id', 'sections': [4242, 1111]},
        {'name': 'Desktop Firefox', 'internal_name': 'custom_firefox', 'sections': [2424]})
    ```

    # If you don't need to collect automation data, you can use these platforms without specifying a field:
    type_platforms = (
        {'name': 'UI', 'sections': [6969, 8888]},
        {'name': 'API', 'sections': [9696]})

I hope this makes it clearer. But, perhaps you don't use Confluence? Then just draw the charts as images!

.. code-block:: python

    plotly_reporter = PlotlyReporter(type_platforms=type_platforms)
    plotly_reporter.draw_test_case_by_priority(filename='stacked_bar_chart.png', values=values)
    plotly_reporter.draw_test_case_by_area(filename='pie_chart1.png', cases=cases)
    plotly_reporter.draw_automation_state_report(filename="pie_chart2.png", reports=reports)
    plotly_reporter.draw_history_type_chart(filename="line_stacked_chart.png")

    for item in automation_platforms:
        plotly_reporter.draw_history_state_chart(chart_name=item['name'])


Alternative Data Sharing Methods
--------------------------------
Alright, alright, we're not going to manually send images to our management, right? I've got a solution for that too!

For instance, we can send the report via e-mail:

.. code-block:: python

    chart_drawings = ['report_chart.png', 'path/to/more_graphics.png']
    chart_captions = ['Priority distribution', 'AT coverage']
    emailer = EmailSender(email="my_personal@email.com",
                          password="my_secure_password",
                          server_smtp="smtp.email_server.com",
                          server_port=587)
    emailer.send_message(files=chart_drawings,
                         captions=chart_captions,
                         recipients=['buddy@email.com', 'boss@email.com'])


If you're using GMail, you'll need to get an oauth token and use it. Then the EmailSender would be initialized like this:

.. code-block:: python

    emailer = EmailSender(email="my_personal@gmail.com",
                          gmail_token="token.json")

.. image:: /assets/images/articles/qa/testrail_reporter/testrails_4.png
   :alt: Report with summary charts to email (or gmail)

Seems like email is a bit of an anachronism? Well then, let's send the report to Slack! Just don't forget to set up the token!

.. code-block:: python

    slack_sender = SlackSender(hook_url='https://hooks.slack.com/services/{your}/{api}/{key}')
    slack_sender.send_message(files=chart_drawings, captions=chart_captions)


.. image:: /assets/images/articles/qa/testrail_reporter/testrails_5.png
   :alt: Report with summary charts to Slack

Don't Forget the Backup!
------------------------
Hark! As we frolic in the digital meadows of TestRail, a shadow looms – the specter of lost work. What if our results and tests vanish into the ether? Fear not, for I shall unveil a secret incantation to preserve our toils.

.. code-block:: python

    tc_backup = TCBackup(tr_url, tr_email, tr_password, test_rails_suite=3)
    tc_backup.backup()  # This spell conjures a backup.xml file with all our tests
    tc_backup.get_archive_backup(suffix='')  # And this one summons a backup.zip archive of our tests


Now, where to safeguard these precious scrolls? Let us entrust them to the cloud, to the mighty vaults of GoogleDrive!

.. code-block:: python

    # First, forge a Google token by visiting the arcane halls of:
    # https://console.developers.google.com/apis/credentials?pli=1
    # Navigate ye through: Create Credentials => OAuth client ID => TV
    # and limited Input Devices to obtain thy client_id and client_secret

    # Use these relics to initialize the uploader with parameters:
    #  google_id = client_id and google_secret = client_secret
    gdrive = GoogleDriveUploader(google_id=client_id, google_secret=client_secret)

    # Upon the first invocation, you shall be prompted to enter your user_code
    # from the user account and activate the API token.

    # But if you already possess the tokens of access, proceed thusly:
    gdrive = GoogleDriveUploader(google_id=client_id,
                                 google_secret=client_secret,
                                 google_api_refresh_token=refresh_token)

    # Now you may upload any artifact, but by default, we seek to hoist our archived backup with tests, the backup.zip
    gdrive.upload(filename='backup.zip', mime_type='application/zip')

.. image:: /assets/images/articles/qa/testrail_reporter/testrails_6.png
   :alt: Backup with test cases of TestRail has been zipped and saved using Google Drive

Tricks and pitfalls
-------------------

What could possibly go awry? Perchance, in the realm of plotly, you must separately summon orca:

.. code-block:: shell

    npm install -g electron orca

Mark well, Slack, the messenger of the workplace, does not entertain the direct upload of images, but only the links to their abodes. To wield images in Slack, you may swiftly upload them to a sanctuary like `Freeimage.host`_. Forsooth, like so (the utility is included in the package):

.. code-block:: python

    image_uploaded = upload_image(filename=chart_drawings[0], api_token=YOUR_SECRET_TOKEN)

    # Extract the URL of the image
    image_url = image_uploaded['image']

    # Or its thumbnail
    image_thumb = image_uploaded['thumb']

Conclusions
-----------
Thus concludes our quest. Getting rid of manual reporting and manual manipulations with data, statuses significantly free your time on SDET, automation needs and fun. Wouldn't it be easier to use an alias and re-learn a new, better, habit? If you like my article, feel free to `share a coin`_. And, for sure here are links to the `GitHub repo`_ and `pypi package`_.

May your backups be many and your data loss few. Until next time, I bid thee safe coding!


.. _share a coin: https://www.donationalerts.com/r/rocketsciencegeek
.. _GitHub repo: https://github.com/wwakabobik/testrail_api_reporter
.. _pypi package: https://pypi.org/project/testrail-api-reporter/
.. _Freeimage.host: https://freeimage.host/
.. _Gurock: https://www.testrail.com/
.. _trcli: https://github.com/gurock/trcli
