# Secret Santa

Secret Santa by Alex Suvertok

License: Not open source

## Installation

### Local

#### Backend Installation
```
mkvirtualenv santa
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

#### Setting basic data (RT team and its members)
```
sh utility/loaddata_all_fixtures.sh
```

#### Instructions for work

* Check the availability of the list of members - /admin/core/member/
  * If they are not there, check the presence of the team - /admin/core/team/
    * If the team does not exist, then create it
  * Add members to the team - /admin/core/member/
* Create a celebration - /admin/core/celebration/
* Run "Let the celebration begin!" action on selected celebrations
* Check the build on the tab "Secret santas" - /admin/core/secretsanta/
* Expect letters to the specified e-mails. To resend the letter, use action "Receive a follow-up letter with the recipient of the gift" - /admin/core/secretsanta/

##### FOR Apple silicon crystal
```
1. Install iTherm2
2. Go to Finder > Applications and find your Terminal (this can also be other terminal app, like iTerm in my case)
3. Right-Click the App and Duplicate it and rename it "Terminal i386"
4. Right-Click "Terminal i386" > Get Info > Enable Open using Rosetta
5. Click to Open the Terminal, type arch to verify it says i386 now.
6. Right-Click the Terminal i386 in your Dock and click "Keep in Dock" for future use.
```

#### Run email test server
```
docker run -d -p 1025:1025 -p 1080:1080 --name mailcatcher schickling/mailcatcher
```

## General recommendations

### Git

* Branch names: use [git flow](https://danielkummer.github.io/git-flow-cheatsheet/) or implement its approach (up to a few words in branch name, for example `feature/remove-old-users`)
* Commit names:
  * Should start with #_(issue number)_, where `issue number` is the number of the related issue on GitHub.
  * Commit text should start with a capital letter
  * Commit text should contain a short description of implemented changes
  * (optional) should end with the name of the related module (if it is possible to define)
  * For example:
    * #34 Add new fields to the user model [Auth]
    * #53 Change the structural relations of public modules [General]
    * #192 Set up basic styles for profile-related components [Profile] 

### Github

#### Issue Labels

Consider using correct labels for every issue and keep them up-to-date.

Priority labels:
* `priority: low` - delayed and not necessary task that might be done in future
* `priority: medium` - default tasks for not critical features and changes
* `priority: high` - tasks that have necessary features or might block work on other features
* `priority: hotfix` - the highest priority features or bugs

Progress labels:
* `status: in-progress` - currently working on the issue
* `status: ready-for-review` - issue-related code supposed to be reviewed by other developer(s)
* `status: ready-for-test` - related functional suppose to be tested
* `status: ready-for-release` - issue-related code might be deployed on the production
* `status: released` - issue related code is deployed on the production
* `status: done` - issue is resolved, deployed, and tested on the production


