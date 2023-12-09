'''

'''

import gspread
import os
import pathlib
from dotenv import load_dotenv

# Class to connect to the database

class connectDB:
    '''
    formats:

    WORKSHEETNAMEFORMAT: DASA_YYYY_Rx

    WORKSHEETDATAFORMAT:

    [index, college_name, course_code, course_name, or_jee, cr_jee, or_dasa, cr_dasa, nicknames, ciwg_status]
       0         1             2            3          4       5       6        7         8           9

    where: or stands for opening rank
           cr stands for closing rank

    '''

    # Constants
    DB_KEY_FILENAME = "DASA-Bot\db_key.json"
    RANK_SPREADSHEET_KEY = os.getenv("RANK_SPREADSHEET_KEY")

    def get_sheet(self, year: str, round: str):

        # Try to find a worksheet for respective year and round, raises value error if not found
        sheet_name = f'DASA_{year}_R{round}'
        try:
            sheet_index = self.worksheet_names.index(sheet_name)
        except ValueError:
            raise ValueError("Invalid year / round")
            return

        wksdat = self.worksheet_data[sheet_index]
        return wksdat

    # Function to get airport data sheet
    def get_air_sheet(self):

        sheet_name = f'DASA_AIRPORT'
        try:
            sheet_index = self.worksheet_names.index(sheet_name)
        except ValueError:
            raise ValueError("Invalid year / round")
            return

        wksdat = self.worksheet_data[sheet_index]
        return wksdat[2:]

    def request_college_list_air(self):

        current_sheet = connectDB.get_air_sheet(self)

        college_list = []
        for row in current_sheet:
            if row[1] not in college_list:
                college_list.append(row[1])

        return college_list[2:]

    def nick_to_air(self, college_nick: str):
        current_sheet = connectDB.get_air_sheet(self)
        college_list = connectDB.request_college_list_air(self)
        # If user inputs the full name of a uni ("Indian Institute of Engineering Science and Technology, Shibpur")
        if college_nick.lower() in [col.lower() for col in college_list]:
            return college_nick.lower()

        for row in current_sheet:
            # If user inputs a nickname ("IIEST")
            aliases = [ali.lower() for ali in row[6].split(', ')]
            #print(aliases) [This is for debugging purposes]
            if college_nick.lower() in aliases:
                return row[1]  # Will return the full name of the uni

    def get_airport_stats(self, college_name):
        returnlist = []
        tempdat = connectDB.get_air_sheet(self)
        college_name = connectDB.nick_to_air(self, college_name)
        for element in tempdat:
            if college_name.lower() == element[1].lower():
                returnlist.append(element[1:6])
        finallist = returnlist[0]
        return finallist

    def request_college_list(self, year: str, round: str):

        current_sheet = connectDB.get_sheet(self, year, round)

        college_list = []
        for row in current_sheet:
            if row[1] not in college_list:
                college_list.append(row[1])

        return college_list[2:]


    def nick_to_college(self, year: str, round: str, college_nick: str):
        current_sheet = connectDB.get_sheet(self, year, round)
        college_list = connectDB.request_college_list(self, year, round)

        if college_nick in college_list:
            return college_nick

        for row in current_sheet:
            if college_nick in [n.strip() for n in row[8].split(",")]:
                return row[1]

        raise ValueError("Invalid college name")
        return
    

    def request_branch_list(self, year: str, round: str, college_name: str, ciwg: bool):
        current_sheet = connectDB.get_sheet(self, year, round)

        college_name = connectDB.nick_to_college(
            self, year, round, college_name)
        branch_list = []
        for row in current_sheet:
            if row[1] != college_name:
                continue  
            if not ciwg and row[9] == '1':
                continue  
            if row[2] not in branch_list:
                branch_list.append(row[2])
        return branch_list


    def get_statistics(self, year: str, round: str, college_name: str, branch_code: str, ciwg: bool, check: bool = False):
        current_sheet = connectDB.get_sheet(self, year, round)
        branch_list = connectDB.request_branch_list(
            self, year, round, college_name, ciwg)
        code = branch_code.upper()

        if code not in branch_list:
            raise ValueError("Invalid branch name")
            return

        for row in current_sheet:
            if row[1] != college_name:
                continue
            if row[2] != branch_code:
                continue

            return row[3:8] if not check else row[4:8]


    def get_statistics_for_all(self, year: str, round: str, college_name: str, ciwg: bool):
        current_sheet = connectDB.get_sheet(self, year, round)
        branch_list = connectDB.request_branch_list(
            self, year, round, college_name, ciwg)
        
        for row in current_sheet:
            if row[1] != college_name:
                continue
        ranks = []
        for branch in branch_list:
            st = connectDB.get_statistics(
                self, year, round, college_name, branch, ciwg, check=True)
            ranks.append([branch, st])
        return ranks


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
                branches = [row[2] for row in current_sheet if row[9] == '1' and row[2] not in ['BAR1', 'BAR', 'ARH', 'ARH1', 'ARC', 'ARC1', 'ARC', 'ARC1']]
                cutoffs, college = [int(row[5]) for row in current_sheet if row[9] == '1' and row[2] not in ['BAR1', 'BAR', 'ARH', 'ARH1', 'ARC', 'ARC1']], [
                    row[1] for row in current_sheet if row[9] == '1' and row[2] not in ['BAR1', 'BAR', 'ARH', 'ARH1', 'ARC', 'ARC1']]
            else:
                branches = [row[2] for row in current_sheet if (
                    row[9] == '0' and row[2] not in ['BAR1', 'BAR', 'ARH', 'ARH1', 'ARC', 'ARC1'])]
                cutoffs, college = [int(row[5]) for row in current_sheet if (row[9] == '0' and row[2] not in ['BAR1', 'BAR', 'ARH', 'ARH1', 'ARC', 'ARC1'])], [
                    row[1] for row in current_sheet if (row[9] == '0' and row[2] not in ['BAR1', 'BAR', 'ARH', 'ARH1', 'ARC', 'ARC1'])]

            cutoffscopy = cutoffs.copy()
            indices_to_remove = []
            for cutoff in cutoffscopy:
                if int(rank) - int(cutoff) > 10000:
                    indices_to_remove.append(cutoffs.index(cutoff))
            for index in sorted(indices_to_remove, reverse=True):
                del cutoffs[index]
                del college[index]
                del branches[index]
            sorted_lists = sorted(zip(cutoffs, college, branches))
            scutoff, scollege, sbranches = zip(*sorted_lists)
            return (scutoff), (scollege), (sbranches)
        

    def __init__(self):
        load_dotenv()
        connectDB.RANK_SPREADSHEET_KEY = os.getenv("RANK_SPREADSHEET_KEY")
        self.cwd_path = os.getcwd()
        db_key_path = os.path.abspath(connectDB.DB_KEY_FILENAME)
        # Connects to service account
        gc = gspread.service_account(filename=f'{db_key_path}')

        self.database = gc.open_by_key(connectDB.RANK_SPREADSHEET_KEY)  # Connects to excel sheet

        self.worksheets = self.database.worksheets()  # Gets all the worksheets
        # Gets names of worksheets
        self.worksheet_names = [
            worksheet.title for worksheet in self.worksheets]

        self.worksheet_data = [worksheet.get_all_values()
                               for worksheet in self.worksheets]


obj = connectDB()
# Uncomment next line for terminal testing.
#obj.testing()
