#############################
Contributing to this project
#############################

When contributing to this repository, please first discuss the change you wish to make via issue with the owners of this repository before making a change.
Please note we have a code of conduct, please follow it in all your interactions with the project.

***********************
Types of Contributions
***********************

=====================
Pull Request Process
=====================

If you wish to make suggestions to this project's code, please keep this few considerations in mind before pushing your **Pull Requests**:

* Ensure any install or build dependencies are removed before the end of the layer when doing a build.
* Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
* This project code is a work in progress, so there is always room for improvement, but there is no need to impoverish the code base quality; have that in mind when submitting your suggestions and **Pull Requests**.
* Until a better release cycle is implemented,the branch **master** is the most recent, most stable code base.
* Always push your **PR** to *develop* branch, any other will not be considered, and giving the case is easy to do, we guess there will be no difficulties with that.
* Any code submitted should have it's own UnitTest added inside the same code structure the project has right now.
* This projects uses PyTest, Coverage, Flake8 and PyLint for testing and static analysis, install them and use them for your development process.
* Before submitting code to the project, run PyTest on the code base, just type `pytest` to run the UnitTest on the code, is your responsibility to guarantee all the test pass and at least to keep the same coverage level previous to your changes.
* PyTest runs Coverage at the end of the process, and throws a brief report, simpler than the traditional one called with `coverage report -m`, which you also are still able to run if there is need for a more detailed version.
* Before submitting code to the project, run Flake8 and PyLint (which we are still tuning so beware of false alarms there, if you detect them, feel free to fix it through your **PR**), look at the reports and fix those lines where there is need to.
* Try your best to validate your signature on GitHub, that way your commits will be signed and validated by the platform.

============
Report Bugs
============

Report bugs at the issues section of `this project`_.

If you find a bug, try your best to provide the necessary information to replicate the resulting error, the expected result and the actual one, if there is additional information you think will be useful, please add it, please include at least:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

.. _`this project`: https://github.com/vitorfs/bootcamp/issues

===================
Fix Bugs
===================

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.

===================
Implement Features
===================

Look through the GitHub issues for features. Anything tagged with "feature" is open to whoever wants to implement it.

===================
Write Documentation
===================

Bootcamp could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

===================
Submit Feedback
===================

The best way to send feedback is to file an issue at the issues section of `this project`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

.. _`this project`: https://github.com/vitorfs/bootcamp/issues

===================
Issues and support
===================

We will try our best to provide help and orientation with this project implementation, but keep in mind than this is done in our spare time, and that has a lot of implications, please, be patient.
