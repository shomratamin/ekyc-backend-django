# ekyc-backend
For postman API reference look into : https://documenter.getpostman.com/view/5549838/SVSPoSqa?version=latest


For dependency installation run:
```shell
pip install -r requirements.txt
```

For data migration run once:
```shell
python manage.py makemigrations
python manage.py migrate
```
To run the server run:
```shell
python manage.py runserver localhost:3000
```

Ekyc Repository Development Guide
=================================

This part of the documentation was created using/copying (and editing, making changes to) the

[contribution guide of FCC:](https://github.com/FreeCodeCamp/FreeCodeCamp/blob/staging/CONTRIBUTING.md)


### Forking Ekyc development repository

<ol>
 <li>Go to the top level shomratamin/ekyc-backend repository: <strong>https://github.com/shomratamin/ekyc-backend</strong></li>
 <li>Click the "Fork" button in the upper right corner of the interface <a href="https://help.github.com/articles/fork-a-repo">More Details Here</a>
</li>
 <li>After the repo has been forked, you will be taken to your copy of the Ekyc-devops repo at <strong>your_username/Ekyc_Backend</strong></li>
</ol>

### Cloning Your Fork

<ol>
<li>Open a Terminal / Command Line / Bash Shell in your projects directory (i.e.: /yourprojectdirectory/)</li>
<li>Clone your fork of Ekyc_Backend</li>
</ol>

```shell
$ git clone git@github.com:your_username/ekyc_Backend.git
```

(make sure to replace your_username with your GitHub Username)

This will download the entire Ekyc_Backend repo to your projects directory.

#### Setup Your Upstream *

1. Change directory to the new Ekyc_Backend directory (`cd Ekyc_Backend`)
2. Add a remote to the official Ekyc_Backend repo:

```shell
$ git remote add upstream https://github.com/shomratamin/ekyc-backend.git
```

Congratulations, you now have a local copy of the Ekyc_Backend repo!


#### Maintaining Your Fork

Now that you have a copy of your fork, there is work you will need to do to keep it current.

##### **Rebasing from Upstream**

Do this prior to every time you create a branch for a PR:

1. Make sure you are on the `development` branch

  > ```shell
  > $ git status
  > On branch development
  > Your branch is up-to-date with 'origin/development'.
  > ```

  > If your aren't on `development`, resolve outstanding files / commits and checkout the `development` branch

  > ```shell
  > $ git checkout development
  > ```

2. Do A Pull with Rebase Against `development`

  > ```shell
  > $ git pull --rebase upstream development
  > ```

  > This will pull down all of the changes to the official development branch, without making an additional commit in your local repo.

3. (_Optional_) Force push your updated staging branch to your GitHub fork

  > ```shell
  > $ git push origin development --force
  > ```

  > This will overwrite the development branch of your fork.

### Create A Branch

Before you start working, you will need to create a separate branch specific to the issue / feature you're working on. You will push your work to this branch.

#### Naming Your Branch

Name the branch something like `xxx-programmername`  where `xxx` is a short description of the changes or feature you are
attempting to add. For example `fix-email-login-ofemeteng` would be a branch where you fix something specific to email login.

#### Adding Your Branch

To create a branch on your local machine (and switch to this branch):

```shell
$ git checkout -b [name_of_your_new_branch]
```

and to push to GitHub:

```shell
$ git push origin [name_of_your_new_branch]
```

##### If you need more help with branching, take a look at _[this](https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches)_.


### Creating A Pull Request

#### What is a Pull Request?

A pull request (PR) is a method of submitting proposed changes to the talktome
Repo (or any Repo, for that matter). You will make changes to copies of the
files which make up ekc-devops in a personal fork, then apply to have them
accepted by ekyc-devops proper.


#### Important: ALWAYS EDIT ON A BRANCH

**If you take only take away one thing from this document**, it should be this: Never, **EVER** make edits to the `development` branch. **ALWAYS make a new branch BEFORE you edit files**. This is critical, because if your PR is not accepted, your copy of
staging will be forever sullied and the only way to fix it is to delete your
fork and re-fork.

#### Methods

The method of creating a pull request for ekyc-devops:

-   Editing files on a local clone


##### Editing via your Local Fork

This is the recommended method. Read about [How to Setup and Maintain a Local
Instance of Ekyc_Backend](#maintaining-your-fork).

1.  Perform the maintenance step of rebasing `development`.
2.  Ensure you are on the `development` branch using `git status`:

```bash
$ git status
On branch development
Your branch is up-to-date with 'origin/development'.

nothing to commit, working directory clean
```

1.  If you are not on development or your working directory is not clean, resolve any outstanding files/commits and checkout development `git checkout development`

2.  Create a branch off of `development` with git: `git checkout -B
    branch/name-here` **Note:** Branch naming is important. Use a name like
    `short-fix-description-programmername` or `short-feature-description-programmername`.

3.  Edit your file(s) locally with the editor of your choice.

4.  Check your `git status` to see unstaged files.

5.  Review your `git status` first. Add your edited files: `git add path/to/filename.ext`.

6.  Commit your edits: `git commit -m "Brief Description of Commit"`. Do not add the issue number in the commit message.

7.  Push your commits to your GitHub Fork: `git push -u origin branch/name-here`

9.  Go to [Common Steps](#common-steps)


### Common Steps

1.  Once the edits have been committed, you will be prompted to create a pull
    request on your fork's GitHub Page.

2.  By default, all pull requests should be against the ekyc-devops repo, `development` branch.

3.  Submit a pull request from your branch to ekyc-devops `development` branch.

4.  The title (also called the subject) of your PR should be descriptive of your changes and succinctly indicate what is being fixed.

    -   **Do not add the issue number in the PR title or commit message.**

    -   Examples: `Add Test Cases to Chat bot` `Correct typo in function <name>`

5.  In the body of your PR include a more detailed summary of the changes you
    made and why.

    -   If the PR is meant to fix an existing bug/issue, then, at the end of
        your PR's description, append the keyword `closes` and #xxxx (where xxxx is the issue number). Example: `closes #1337`. This tells GitHub to close the existing issue, if the PR is merged.

6.  Indicate if you have tested on a local copy of the site or not.


### How We Review and Merge Pull Requests

Before the pull request we will have a code review session in Slack.


### Next Steps

#### If your PR is accepted

Once your PR is accepted, you may delete the branch you created to submit it.
This keeps your working fork clean.

You can do this with a press of a button on the GitHub PR interface. You can
delete the local copy of the branch with: `git branch -D branch/to-delete-name`

#### If your PR is rejected

Don't despair! You should receive solid feedback from the Issue Moderators as to why it was rejected and what changes are needed.

Many Pull Requests, especially first Pull Requests, require correction or
updating. If you have used the GitHub interface to create your PR, you will need to close your PR, create a new branch, and re-submit.

If you have a local copy of the repo, you can make the requested changes and
amend your commit with: `git commit --amend` This will update your existing
commit. When you push it to your fork you will need to do a force push to
overwrite your old commit: `git push --force`

Be sure to post in the PR conversation that you have made the requested changes.


*******************************


### The project tools:
 - [Rasa](https://rasa.com/)


### Workflow

 - All the code must comply with the [PEP-8](https://www.python.org/dev/peps/pep-0008/)
 - The code must have descriptive [comments](https://www.python.org/dev/peps/pep-0008/#comments)
 - The code must have a step by step description (pseudocode) for the code review session
 - Before the pull request, the code has to pass a code review session
 - If you are having problems with your code let us know in #code-review


#### All the code must comply with the PEP-8 style guide

 - [Auto PEP-8]($ autopep8 --in-place --aggressive --aggressive <filename>) or use a linter

```shell
$ autopep8 --in-place --aggressive --aggressive <filename>
```

#### The code must have  descriptive comments

  Follow the style guide [comments section](https://www.python.org/dev/peps/pep-0008/#comments)

#### The code must have  a step by step  description (pseudocode)

  This pseudocode will be used in the  code review session

#### Before the pull request the code has to pass a code review


  - Post in the slack channel **code-review** a snippet with this format:
    -  Title :"Code review session for ```<branch-name>```"
    -  Body: A multiline comment with the content of the ```logs.txt``` file
    -  Body: A multiline comment with the pseudocode
    -  Body: The code

  - We will set a day for a review session

  - In the code review session you will explain how the code works
  - If the code pass this review you will have to make a **pull request**



#### If you are having problems with your code:
   -  Post in the Slack channel **code-review** a snippet with this format:
   -  Title :"Help with ```<branch-name>```"
   -  Body: A multiline comment with the content of the ```logs.txt``` file
   -  Body: A multiline comment witn the pseudocode
   -  Body: The code  


****************************
* http://stackoverflow.com/questions/7244321/how-do-i-update-a-github-forked-repository
* https://2buntu.com/articles/1459/keeping-your-forked-repo-synced-with-the-upstream-source/
* *  we need test and testers (QA)
