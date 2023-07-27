'''

'''

import gspread
import os
import pathlib
from dotenv import load_dotenv

#Main fuction for backend connectivity to gsheets databse
class connectDB:
    '''
    formats:

    WORKSHEET NAME FORMAT: DASA_YYYY_Rx

    WORKSHEET DATA FORMAT:

    [index, college_name, course_code, course_name, or_jee, cr_jee, or_dasa, cr_dasa, nicknames, ciwg_status]
       0         1             2            3          4       5       6        7         8           9

    where: or stands for opening rank
           cr stands for closing rank

    '''


    # constants, try not to change
    DB_KEY_FILENAME = "db_key.json"
    RANK_SPREADSHEET_KEY = os.getenv("RANK_SPREADSHEET_KEY")


    # function to get sheet data for a specific year and round
    def get_sheet(self, year : str, round : str):

        # try to find a worksheet for respective year and round, raises value error if not found
        sheet_name = f'DASA_{year}_R{round}'
        try:
            sheet_index = self.worksheet_names.index(sheet_name)
        except ValueError:
            raise ValueError("Invalid year / round")
            return

        wksdat = self.worksheet_data[sheet_index]
        return wksdat[2:]

    # function to connect to airplane data sheet
    def get_air_sheet(self):

        # Gets airport data sheet
        sheet_name = f'DASA_AIRPORT'
        try:
            sheet_index = self.worksheet_names.index(sheet_name)
        except ValueError:
            raise ValueError("Invalid year / round")
            return

        wksdat = self.worksheet_data[sheet_index]
        return wksdat[2:]

    #Gets college list in airport db
    def request_college_list_air(self):

        current_sheet = connectDB.get_air_sheet(self)  # stores all colleges for airport database pulling

        college_list = []
        for row in current_sheet:
            if row[1] not in college_list:
                college_list.append(row[1])

        return college_list[2:]

    #fetches colleges from nick names given in alternate names colloum
    def nick_to_air(self, college_nick: str):
        current_sheet = connectDB.get_air_sheet(self)
        college_list = connectDB.request_college_list_air(self)
        # if user inputs the full name of a uni ("Indian Institute of Engineering Science and Technology, Shibpur")
        if college_nick.lower() in [col.lower() for col in college_list]:
            return college_nick.lower()

        for row in current_sheet:
            # if user inputs the short form of a uni ("iiest")
            aliases = [ali.lower() for ali in row[6].split(', ')]
            #print(aliases)
            if college_nick.lower() in aliases:
                return row[1]  # will return the full name of the university

    #Gets the final stats of the airport by fetching exact rows, and correct index thru college name
    def get_airport_stats(self, college_name):
        returnlist = []
        tempdat = connectDB.get_air_sheet(self)
        college_name = connectDB.nick_to_air(self, college_name)
        #print(college_name)
        for element in tempdat:
            #print(element)
            if college_name.lower() == element[1].lower():
                returnlist.append(element[1:6])
        finallist = returnlist[0]
        return finallist

    # function to request a list of colleges for a specific year and round
    def request_college_list(self, year : str, round : str):

        current_sheet = connectDB.get_sheet(self, year, round)  # stores all values for current year and round

        college_list = []
        for row in current_sheet:
            if row[1] not in college_list:
                college_list.append(row[1])

        return college_list[2:]


    # function to convert a college nickname to the original college name
    def nick_to_college(self, year : str, round : str, college_nick : str):
        current_sheet = connectDB.get_sheet(self, year, round)
        college_list = connectDB.request_college_list(self, year, round)

        if college_nick in college_list:
            return college_nick

        for row in current_sheet:
            if college_nick in [n.strip() for n in row[8].split(",")]:
                return row[1]


        raise ValueError("Invalid college name")
        return


    # function to request a list of branches for a specific year, round and college
    def request_branch_list(self, year : str, round : str, college_name : str, ciwg : bool):
        current_sheet = connectDB.get_sheet(self, year, round)

        college_name = connectDB.nick_to_college(self, year, round, college_name)
        branch_list = []
        for row in current_sheet:
            if row[1] != college_name:
                continue## skips any irrelevant college names
            if not ciwg and row[9] == '1':
                continue ## checks for non-ciwg
            if row[2] not in branch_list:
                branch_list.append(row[2])
        return branch_list


    # functions to get rank statistics
    def get_statistics(self, year : str, round : str, college_name : str, branch_code : str, ciwg : bool, check:bool = False):
        current_sheet = connectDB.get_sheet(self, year, round)
        branch_list = connectDB.request_branch_list(self, year, round, college_name, ciwg)
        code = branch_code.upper()

        # checks if branch is valid
        if code not in branch_list:
            raise ValueError("Invalid branch name")
            return

        for row in current_sheet:
            if row[1] != college_name: continue
            if row[2] != branch_code: continue

            return row[3:8] if not check else row[4:8]# [branch name], jee_or, jee_cr, dasa_or, dasa_cr

    #function used to fetch stats for all branches
    def get_statistics_for_all(self, year: str, round: str, college_name: str, ciwg: bool):
        current_sheet = connectDB.get_sheet(self, year, round)
        branch_list = connectDB.request_branch_list(self, year, round, college_name, ciwg)
        # checks if branch is valid
        for row in current_sheet:
            if row[1] != college_name:
                continue
        ranks = []
        for branch in branch_list:
            st = connectDB.get_statistics(self, year, round, college_name, branch, ciwg, check = True)
            ranks.append([branch, st])
        return ranks

    #Outdated version of reverse engine
    #function to return 3 lists of colleges based on user's CRL and cutoff
    def analysis(self, rank: int, ciwg: bool, branch: str = None):
        current_sheet = connectDB.get_sheet(self, "2022", "3")
        highclg = []
        midclg = []
        lowclg = []
        for row in current_sheet:
            val = int(row[5])
            if not ciwg and row[9] == '1':
                continue
            closing_rank = f"{row[1]} {row[2]} Closing rank: {row[5]}"
            if val - rank < 0:
                pass
            elif val - rank < 50000:
                lowclg.append(closing_rank)
            elif val - rank < 100000:
                midclg.append(closing_rank)
            if val - rank > 100000:
                highclg.append(closing_rank)

        if branch:
            lowclg = [clg for clg in lowclg if branch.lower() in clg.lower()]
            midclg = [clg for clg in midclg if branch.lower() in clg.lower()]
            highclg = [clg for clg in highclg if branch.lower() in clg.lower()]

        return lowclg, midclg, highclg


    ## testing function remove comment out when u want to test in terminal and run connectRankDB.py
    '''
    def testing(self):

        userinput= input("Please enter your selection \n1. Retrieve college rankings\n2. Enter JEE Rank to determine college chances\n")
        if userinput == "1":
            while True:
                year = input("Enter year: ")
                round = input("Enter round: ")

                current_sheet = connectDB.get_sheet(self, year, round)
                college_list = connectDB.request_college_list(self, year, round)

                print("\nChoose a college from below: ")
                for college in college_list:
                    print(college)

                breaker = True
                while breaker:
                    breaker = False
                    try:
                        college = input("\n")
                        college = connectDB.nick_to_college(self, year, round, college)
                    except ValueError:
                        print("Invalid college name, re-enter")
                        breaker = True


                ciwg_yn = input("Are you CIWG? (Y/N) ")
                ciwg = ciwg_yn.lower() == 'y'

                branch_list = connectDB.request_branch_list(self, year, round, college, ciwg)

                print(f"\nAvailable branches for {college}: " )
                for branch in branch_list:
                    print(branch)

                branch = input("\n")
                truebranch = branch.upper()
                while truebranch not in branch_list:
                    print("Invalid branch name, re-enter")
                    branch = input()


                stats = connectDB.get_statistics(self, year, round, college, truebranch, ciwg)
                print(f"""
                    \nStatistics for {college}, {truebranch}
                    \nJEE Opening Rank: {stats[0]}
                    \nJEE Closing Rank: {stats[1]}
                    \nDASA Opening Rank: {stats[2]}
                    \nDASA Closing Rank: {stats[3]}
                        """)

        elif userinput == "2":
            rank = int(input("Enter JEE Rank: "))
            ciwg_yn = input("Are you CIWG?(Y/N): ")
            ciwg = ciwg_yn.lower() == 'y'
            branch_yn = input("Which Branch?: ")
            branch = branch_yn.upper()
            lowclg, midclg, highclg = connectDB.analysis(self, rank, ciwg, branch)
            print("\n\nLow chances in: \n\n")
            for row in lowclg:
                print(row)
            print("\n\nMid chances in: \n\n")
            for row in midclg:
                print(row)
            print("\n\nHigh chances in: \n\n")
            for row in highclg:
                print(row)

        elif userinput == "3":

            college_name = input("College: ")
            stats = connectDB.get_airport_stats(self, college_name)
            print("\n\nAIRPORT STATS: \n\n")
            for row in stats:
                print(row)

        else:
            print("Invalid input please try again")
    '''

    #Function for reverse engine
    def reverse_engine(self, rank: str, ciwg: bool, branch: str = None):
         current_sheet = connectDB.get_sheet(self, "2023", "1")
         index = None
         if branch is not None:
             branch = branch.upper()
             if ciwg:
                 branch += "1"
             cutoffs, college = [int(row[5]) for row in current_sheet if branch == row[2]], [
                 row[1] for row in current_sheet if branch == row[2]]

             cutoffscopy = list(cutoffs)
             indices_to_remove = []
             for cutoff in cutoffscopy:
                 if int(rank) - int(cutoff) > 10000:
                     indices_to_remove.append(cutoffs.index(cutoff))
             for index in sorted(indices_to_remove, reverse=True):
                 del cutoffs[index]
                 del college[index]
             sorted_lists = sorted(zip(cutoffs, college))
             scutoffs, scollege = zip(*sorted_lists)
             return scutoffs, scollege
         else:
             if ciwg:
                 branches = [row[2] for row in current_sheet if row[9] == '1']
                 cutoffs, college = [int(row[5]) for row in current_sheet if row[9] == '1'], [
                     row[1] for row in current_sheet if row[9] == '1']
             else:
                 branches = [row[2] for row in current_sheet if row[9] == '0']
                 cutoffs, college = [int(row[5]) for row in current_sheet if row[9] == '0'], [
                     row[1] for row in current_sheet if row[9] == '0']

             cutoffscopy = cutoffs.copy()
             indices_to_remove = []
             for cutoff in cutoffscopy:
                 if int(rank) - int(cutoff) > 10000:
                     indices_to_remove.append(cutoffs.index(cutoff))
             for index in sorted(indices_to_remove, reverse=True):
                 del cutoffs[index]
                 del college[index]
                 del branches[index]

            #sorts all the colleges into one lsit
             sorted_lists = sorted(zip(cutoffs, college, branches))
             scutoff, scollege, sbranches = zip(*sorted_lists)
             return (scutoff), (scollege), (sbranches)

    # initialisation function
    def __init__(self):
        load_dotenv()
        connectDB.RANK_SPREADSHEET_KEY = os.getenv("RANK_SPREADSHEET_KEY")
        self.cwd_path = os.getcwd()

        # connects to DB

        db_key_path = os.path.abspath(connectDB.DB_KEY_FILENAME)  # gets path name of db_key.json
        gc = gspread.service_account(filename = f'{db_key_path}')  # connects to service account

        self.database = gc.open_by_key(connectDB.RANK_SPREADSHEET_KEY) # connects to excel sheet

        self.worksheets = self.database.worksheets() # gets all the worksheets
        self.worksheet_names = [worksheet.title for worksheet in self.worksheets] # gets names of worksheets

        self.worksheet_data = [worksheet.get_all_values() for worksheet in self.worksheets]



obj = connectDB()
#Uncomment next line for testing
#obj.testing()