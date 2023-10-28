# DasaBot - Discord Cutoffs and College Info Bot

## Table of Contents
- [Required Dependencies](#required-dependencies)
- [Summary](#summary)
- [How to Use the Bot](#how-to-use-the-bot)
- [Project Structure](#project-structure)
- [License](#license)
- [Contributors](#contributors)

### Required Dependencies
The following libraries can also be found in `requirements.txt` by running the following command:  
```shell
pip install -r requirements.txt
```

### Summary

DasaBot is a versatile Discord bot designed to provide information about cutoffs, college lists, and closest airports. It offers these details via Discord slash commands, processes the requests in [mainBot.py](mainBot.py), communicates with [connectRankDB.py](connectRankDB.py) for relevant data, and analyzes user input for any college nicknames (e.g., "nitt" for NIT Trichy). It retrieves data from a Google Sheets database and delivers the results to Discord.

**Note:** This project is a fork of the original [DasaBot](https://github.com/DASA-boys/DASA-Bot), a collaborative effort of several authors.

### How to Use the Bot

**Slash Commands:**
DasaBot features several slash commands that enable you to retrieve specific information. Below are the available commands:

#### Cutoff (branch is optional)
- `/cutoff`: Retrieve cutoffs for a given college, year, round, branch, and category. If no branch is provided, it displays cutoffs for all branches of the college.

![image-001](https://github.com/Haz3-jolt/DasaBot/assets/79502699/6f3f1a64-618f-4217-bd82-a876822c52ea)
![image-003](https://github.com/Haz3-jolt/DasaBot/assets/79502699/4e06797e-81b8-4fdd-8d33-ebe990e88800)
![image-002](https://github.com/Haz3-jolt/DasaBot/assets/79502699/9e864e24-1706-4310-a46a-38176ebb62c4)
![image-004](https://github.com/Haz3-jolt/DasaBot/assets/79502699/a252db12-0408-45cc-9a2c-c3e2c7b9130a)

#### Analyze (branch is optional)
- `/analyze`: Find colleges with closing rank cutoffs closest to the rank entered by the user. If no branch is provided, it displays cutoffs for all branches from colleges within a close range of the given rank.

![image-005](https://github.com/Haz3-jolt/DasaBot/assets/79502699/e1de1d00-95ca-47f4-bd57-065b03e23d23)
![image-006](https://github.com/Haz3-jolt/DasaBot/assets/79502699/b79c07a3-33a1-421c-999a-1598049657df)
![image-007](https://github.com/Haz3-jolt/DasaBot/assets/79502699/4d932f65-4198-4b0c-aa61-e6d918e928de)

#### Airport
- `/airport`: Get information about the closest airport to a requested college, including the airport code and distance from the airport to the college.

![image-008](https://github.com/Haz3-jolt/DasaBot/assets/79502699/3a17837c-40f2-4384-a414-513bf87ec43c)
![image-009](https://github.com/Haz3-jolt/DasaBot/assets/79502699/aea489b4-d00c-4f72-a935-ac3eee4c6acc)

#### Resupd (Mod only, non-slash command)
- `/resupd`: A command for moderators to update results of server members automatically. It updates the result message on the server's results tab and adds users' results based on relevant year and college roles.

![image-010](https://github.com/Haz3-jolt/DasaBot/assets/79502699/d2aa80df-a14c-4eed-88ae-346b2b352652)
![image-011](https://github.com/Haz3-jolt/DasaBot/assets/79502699/690f378d-fde3-42ba-9338-fadf504ad5ba)

### Project Structure

#### [connectRankDB.py](connectRankDB.py)

- This script manages data retrieval from a Google Sheets database.
- It uses the `gspread` library for interaction with Google Sheets, as well as `os` and `pathlib` for file handling.
- The script establishes a data connection to Google Sheets using service account credentials loaded from a JSON file ([db_key.json](DASABot/db_key.json)).
- It opens a specific Google sheet, retrieves worksheets, and stores data in a nested list format for program operations.
- Methods include:
  - `get_sheet`: Searches for the worksheet containing the cutoffs of a specific year and round.
  - `request_college_list`: Returns a list of colleges participating in DASA counseling for a specific year and round.
  - `nick_to_college`: Converts college nicknames to their full names.
  - `request_branch_list`: Returns a list of valid branches under a college based on qualification for CIWG.
  - `get_statistics`: Provides cutoff ranks for a specific branch under a college.
  - `get_statistics_for_all`: Retrieves cutoff ranks for all branches under a specified college using `get_statistics`.
  - `reverse_engine`: Lists colleges with closing rank cutoffs closest to the rank given by the user.
  - `analysis`: Returns colleges filtered by the difference between the user's CRL and a college's Round 3 JEE Closing cutoff.
  - `get_airport_stats`: Provides information about airports closest to colleges.

#### [mainBot.py](mainBot.py)

- This script is the main script for interacting with the Discord API to log in the bot.
- It listens for Discord slash command pings and utilizes the `connectRankDB.py` class `connectDB` to retrieve data from the Google Sheets database.
- All commands for the slash commands are stored in the [dasa.py](cogs/dasa.py) script in the `cogs` folder.
- Additional functionality includes:
  - `reload()`: Reloads cogs.
  - `shut()`: Shuts down the bot.

#### [dasa.py](cogs/dasa.py)

- This script is a command extension file containing commands related to DASA.
- Commands include:
  - `cutoff`: Retrieve cutoffs for a specified college, year, round, branch, and category.
  - `analyze`: Find colleges with closing rank cutoffs closest to a specified rank.
  - `airport`: Get information about the closest airport to a requested college.

#### [dasa_res.py](cogs/dasa_res.py)

- This script is a command extension file for moderator use to manage the results tab on the server.
- `resupd` is a mod-only non-slash command that updates server members' results and adds them to the server's results tab based on relevant year and college roles.

**Note:** The repository assumes the presence of the `gspread` library and a valid service account JSON file with appropriate access to the Google Sheet. Create a `.env` file with environment variables and use the provided [.example_env](.example_env) file as a reference.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Contributors

- [Haz3jolt](https://github.com/Haz3-jolt): Worked on both front-end and back-end, designed algorithms for the airport command, and contributed to the legacy Discord interface. Created the original command system, later replaced by Koshy's update, and assisted in transitioning the codebase to modern slash commands using Discord.py.

- [Koshy](https://github.com/koshyj8): Structured and designed the front-end interface, coded Discord slash commands to retrieve data from the database, and redesigned the bot's output from messages to embeds for a more user-friendly design. Also collaborated on the airport command with Haz3jolt.

- [Cookie](https://github.com/CookieOnCode): Established and converted DASA cutoffs into usable XLS format. Created most of the algorithms in [connectRankDB.py](connectRankDB.py) to extract requested information from the database. Managed the test server and developer account for the bot, including relevant tokens.

- [Amol](https://github.com/AmolOnGitHub): Assisted in mapping DASA ranks with JEE ranks in the database and laid the foundation for [connectrankdb.py](connectRankDB.py) and [mainBot.py](mainBot.py). Worked on an admin-level command, `resupd`, to automatically update the server's results tab. Integrated the dotenv library to secure API and login tokens.
