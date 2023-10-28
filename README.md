### Required Dependencies:
The following libraries can also be found in `requirements.txt` by running the following command:  
`pip install -r requirements.txt`  

---

# Summary

This is a discord bot which fetches the cutoffs, college lists based on rank and closest airports via discord slash commands, parses them in mainBot.py, then asks for the relavent data from connectRankDB.py and then analyses the request for any nicknames used (ex: nitt for nit Trichy), It then fetches it from a Google sheets database and finally outputs to discord.

NOTE: This is a fork of the original [DasaBot](https://github.com/DASA-boys/DASA-Bot) which was created with equal collabaration with all of my co-authors without which this project will not have been possible. 

## Here are the slash commands:
![image-000](https://github.com/Haz3-jolt/DasaBot/assets/79502699/9d88fd7e-1434-402f-9c19-1e5dbe055e2a)


## Here is what each slash command looks for and what the output would look like:

### cutoff (branch is optional): 
![image-001](https://github.com/Haz3-jolt/DasaBot/assets/79502699/6f3f1a64-618f-4217-bd82-a876822c52ea)
![image-003](https://github.com/Haz3-jolt/DasaBot/assets/79502699/4e06797e-81b8-4fdd-8d33-ebe990e88800)
![image-002](https://github.com/Haz3-jolt/DasaBot/assets/79502699/9e864e24-1706-4310-a46a-38176ebb62c4)
![image-004](https://github.com/Haz3-jolt/DasaBot/assets/79502699/a252db12-0408-45cc-9a2c-c3e2c7b9130a)


### analyse (branch is optional): 
![image-005](https://github.com/Haz3-jolt/DasaBot/assets/79502699/e1de1d00-95ca-47f4-bd57-065b03e23d23)
![image-006](https://github.com/Haz3-jolt/DasaBot/assets/79502699/b79c07a3-33a1-421c-999a-1598049657df)
![image-007](https://github.com/Haz3-jolt/DasaBot/assets/79502699/4d932f65-4198-4b0c-aa61-e6d918e928de)


### airport:
![image-008](https://github.com/Haz3-jolt/DasaBot/assets/79502699/3a17837c-40f2-4384-a414-513bf87ec43c)
![image-009](https://github.com/Haz3-jolt/DasaBot/assets/79502699/aea489b4-d00c-4f72-a935-ac3eee4c6acc)


### resupd (Mod only non slash command to update results of members of server):
![image-010](https://github.com/Haz3-jolt/DasaBot/assets/79502699/d2aa80df-a14c-4eed-88ae-346b2b352652)
![image-011](https://github.com/Haz3-jolt/DasaBot/assets/79502699/690f378d-fde3-42ba-9338-fadf504ad5ba)


---

## How does the project work?:

### connectRankDB.py

1. The script imports the necessary libraries, `gspread` for interacting with Google Sheets, as well as `os` and `pathlib` for getting filepaths etc.
2. The script establishes a data connection to Google Sheets using the `service_account` method from `gspread`. It loads the service account credentials from a JSON file named `"DASABot/db_key.json"`.
4. It then opens a specific google sheet using its key, and then gets all the worksheets present and adds it to an object variable called `worksheets`
5. The script retrieves all the values from the worksheet using the `get_all_values` method and stores them in the `worksheet_data` variable in the form of a nested list. Since the data is static, the program operates based on list indexes.

Upon this, there are multiple methods to execute specific functions:

- `get_sheet` searches the worksheet containing the cutoffs of a specific year and round
- `request_college_list` returns a list of colleges participating in DASA counselling in a specific year and round
- `nick_to_college` converts any college nickname to its full name and returns it
- `request_branch_list` returns a list of valid branches under a college depending on whether the student qualifies for ciwg or not
- `get_statistics` returns a list of the cutoff ranks for a specific branch under a college
- `get_statistics_for_all` returns a list of cutoff ranks for all branches under a specified college (using `get_statistics`)
- `reverse_engine` returns a list of colleges which has a closing rank cutoff closest to the rank given by the user  
- `analysis` returns three lists each containing the names of colleges filtered out by the difference between the user's CRL and college's Round 3 JEE Closing cutoff
- `get_airport_stats` returns the info for each airport closest to a college using similar methods to get_statistics.

### mainBot.py
1. This script is the main script which interacts with the Discord API for logging into the bot.
2. The Bot then listens for discord slash command pings, and then calls the connectRankDB.py class connectDB to use its methods to retrieve data from the gsheets Database.
3. All of the commands for the slash commands are stored in the dasa.py cript in the cogs folder.
4. It has the commands that help in reloading cogs `def reload()` as well as shut the bot `def shut()`.

### dasa.py
1. This script is an command extension file containing the commands relating to DASA.
- `cutoff` - This command retrieves the cutoffs for a given college taken from a given year, round, branch and category. If branch is not given, cutoffs for all the branches from the given college will be displayed.  
- `analyze` - This command returns the colleges whose closing rank cutoffs are closest to the rank inputed by the user. If branch is not givem, cutoffs for all the branches from all the colleges within a close range(i.e. 10000 higher than the given rank) of the given rank is returned.
- `airport` - This command returens the closest airport to a requested college, the airport code, and distance from airport to the college.

### dasa_res.py
1. This script is an command extension file for mod use to admin the results tab in the server.
- `resupd` - This is a Mod only non slash command to update results of members of server which automatically updates the result message on the results tab on the DASA server, and adds the users results by searching for if they have a relevant year role and college role. This also has a method under the DASAResults class which checks if the user has permission to use the command. 

  

NOTE: The repo assumes the presence of the `gspread` library and a valid service account JSON file with the appropriate access to the Google Sheet.

NOTE: Create a .env file with your environment variables in the example_.env file included and create a valid service account JSON file called db_key.json file with your required info in the example_db_key.json file included. If your forking this repo be sure to create a .gitignore to not leak your API tokens, and login info.

---

## Contributors:

- [Haz3jolt](https://github.com/Haz3-jolt): Worked in both front end and back end, designed algorithms for airport command and designed part of the legacy discord interface. Created the original commands system which was later replaced by Koshy's update. Helped transition the codebase from legacy discord commands to modern slash commands.
- [Koshy](https://github.com/koshyj8): Structured and designed front-end interface and coded discord slash commands to pull data from database, also changed the bot's output from messages to embeds with more fluid design. Also helped work on the airport command with Haz3jolt. 
- [Cookie](https://github.com/CookieOnCode): Established and converted DASA cutoffs to usable data in XLS format. Created nearly all the algorithms in connectRankDB.py to fetch the correct data to return requested information. Maintained the test server and managed the developer account for the bot and all relevant tokens. 
- [Amol](https://github.com/AmolOnGitHub): Assisted in mapping of DASA ranks with JEE ranks within database and laid foundation for connectrankdb.py and mainBot.py , Also worked on a admin level command which auto updates the servers results tab called resupd. Integrated the dotenv lib to maintain the secrecy of the API and login tokens.

