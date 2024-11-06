######################
Adding Tests to Vercel
######################
:date: 2024-11-06 20:28
:author: wwakabobik
:tags: qa, vercel, ci, github actions, devops
:slug: adding_tests_to_vercel
:category: qa
:status: published
:summary: Adding automated tests to your Vercel project can be quick and efficient. Here's a two-path guide to integrating tests using GitHub Actions or Vercel's Checks.
:cover: assets/images/bg/qa.png

.. pull-quote::
    This is my original article (published May 2023), translated from a `Habrahabr`_. I decided to remove all old articles from it and store it only in my personal blog because I don't like moral position of Habr audience.

Good day to all developers, engineers, and automators who stumbled upon this guide. If your project is running on `Vercel`_ and you've dabbled in automation, then this quick guide is right up your alley.

The story is short and sweet, much like most things in `Vercel`_ – adding your automated tests is straightforward and quick. And yes, there are two ways to go about it.

Using GitHub Actions
--------------------

Original reference `here`_ if you want to go into the weeds. This method is ideal if you already have a solid foundation of automated tests or if you’re using `Selenium`_, `Cypress`_, or similar frameworks (but not `Mocha`_, `Puppeteer`_, or `Playwright`_ – we’re talking the heavier hitters here). All is powered by `GitHub Actions`_. All you need is to add or update a file in your project’s directory: **.github/workflows/e2e.yml** (name it whatever suits your fancy, as long as it aligns with the tests you’re running).:

.. code-block:: yaml

    name: E2E Tests

    on:
      deployment_status:

    jobs:
      e2e-tests:
        runs-on: ubuntu-latest
        if: github.event.deployment_status.state == 'success'
        steps:
          - name: Checkout
            uses: actions/checkout@v2

          - name: Setup Node.js
            uses: actions/setup-node@v2
            with:
              node-version: 18

          - name: Install pnpm
            run: curl -fsSL https://get.pnpm.io/install.sh | env PNPM_VERSION=9.12.3 sh - | node - add --global pnpm

          - name: Install dependencies
            run: pnpm install

          - name: Run E2E tests
            run: |
              if [ "${{ env.VERCEL_ENV }}" != "production" ]; then
                my_param="qa"
              else
                my_param=""
              fi
              npx cypress run --config-file "cypress.config.ts" --config specPattern="cypress/e2e" baseUrl=${{ github.event.deployment_status.target_url }} --env nice_param=$my_param allure=true --spec "cypress/e2e/base.cy.js,cypress/e2e/meta.cy.js"
            continue-on-error: true
            id: e2e_tests

          - name: Generate Allure report
            if: always()
            run: pnpm run allure:generate allure-results

          - name: Archive Allure report
            run: zip -r allure-report.zip allure-report

          - name: Upload Allure report
            uses: actions/upload-artifact@v2
            with:
              name: allure-report
              path: allure-report.zip

          - name: Check test status (finally)
            if: ${{ steps.e2e_tests.outcome == 'failure' }}
            run: exit 1

You could replace `Cypress`_ with anything else you’re using – `pytest`_/`Selenium`_, for instance – and set up the environment with something like `tox`_. Or, if you’re feeling adventurous, go ahead and trigger a third-party service or webhook. Here are a few things to note:

.. code-block:: yaml

    if: github.event.deployment_status.state == 'success'

* Tests will only run if the deployment is successful (courtesy of a webhook trigger).
* You’ll likely want to customize tests or parameters based on the environment being deployed. In this example, if the deployment isn't for production, we add the "my_param" parameter, which will be picked up by the tests. The `Vercel`_ environment itself is available through the **env.VERCEL_ENV** variable.

.. code-block:: yaml

    if [ "${{ env.VERCEL_ENV }}" != "production" ]; then
      my_param=""
    else
      my_param="qa"
    fi

The base URL (base_url) for testing lives in a variable as well:

.. code-block:: yaml

    ${{ github.event.deployment_status.target_url }}

You can also add different tests or reports to various steps, such as using `Allure-reports`_ for test results. Upon completion, you’ll see the results in GitHub Actions (unless, of course, you’re calling in a heavy-duty service like `Jenkins`_ or some cloud testing platform).

.. image:: /assets/images/articles/qa/adding_tests_to_vercel/01_vercel_ga.png
   :alt: GitHub actions

A detailed log will show up here:

.. image:: /assets/images/articles/qa/adding_tests_to_vercel/02_vercel_log.png
   :alt: GitHub actions log


Report will be stored in **Actions -> Run -> Summary -> Artifacts**:

.. image:: /assets/images/articles/qa/adding_tests_to_vercel/03_vercel_allure.png
   :alt: Allure report

Using Checks
------------

Alternatively, you can run checks directly within the Vercel deployment workflow via the **Checks** action. Write your own plugin (`Integration`_) to check your deployment with the `Checks API`_, or use an existing one like `Checkly`_:

.. image:: /assets/images/articles/qa/adding_tests_to_vercel/04_vercel_checkly.png
   :alt: Checkly

`Checkly`_ operates with `Playwright`_ tests, offering a base level of checks out of the box, which you can expand upon with your own tests:

.. image:: /assets/images/articles/qa/adding_tests_to_vercel/05_vercel_playwright.png
   :alt: Playwright tests on Checkly

During deployment, these tests will run as a separate step, with results generated accordingly:

.. image:: /assets/images/articles/qa/adding_tests_to_vercel/06_vercel_results.png
   :alt: Checkly testing results

In Conclusion
-------------

As you can see, adding tests to Vercel projects is simple and fast.

That’s all, folks. If this guide has been a useful addition to your automation toolkit, feel free to like the post, drop a comment, or, if you’re feeling particularly generous, `throw a coin`_ my way.

.. _throw a coin: https://www.donationalerts.com/r/rocketsciencegeek
.. _Vercel: https://vercel.com/
.. _Selenium: https://www.selenium.dev/
.. _Cypress: https://www.cypress.io/
.. _Mocha: https://mochajs.org/
.. _Puppeteer: https://pptr.dev/
.. _Playwright: https://playwright.dev/
.. _here: https://vercel.com/guides/how-can-i-run-end-to-end-tests-after-my-vercel-preview-deployment
.. _pytest: https://docs.pytest.org/en/stable/
.. _tox: https://tox.wiki/en/latest/
.. _Allure-reports: https://docs.qameta.io/allure/
.. _Jenkins: https://www.jenkins.io/
.. _Integration: https://vercel.com/docs/integrations/create-integration
.. _Checks API: https://vercel.com/docs/integrations/checks-overview
.. _Checkly: https://www.checklyhq.com/
.. _GitHub Actions: https://github.com/features/actions
.. _Habrahabr: https://habr.com/en/users/wwakabobik/