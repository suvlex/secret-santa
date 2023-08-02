# Secret Santa

Secret Santa by Alex Suvertok

License: Open source

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
