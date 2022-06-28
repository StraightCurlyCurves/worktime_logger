"""
WORKTIME LOGGER

Author:         Jan Schüssler
Website:        https://www.jan-schuessler.ch

Version:        1.1.0


Copyright (c) 2021 Jan Schüssler

The above copyright notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from datetime import datetime, timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

version = '1.1.0'

empty_df = pd.DataFrame(columns=[
    'project_name',
    'start_date',
    'start_time',
    'stop_date',
    'stop_time',
    'seconds_worked'])

temp_file = 'temp_data.csv'
main_file = 'main_data.csv'
csv_seperation_char = ';'  # ';' when "Regional Format" is set to German, ',' for english. In windows, change it under "Reginal Settings"
date_format = "%d.%m.%Y" # "%d.%m.%Y" for German, "%d/%m/%Y" for English
time_format = "%H:%M:%S"
date_time_format = "%d.%m.%Y %H:%M:%S"

if not os.path.exists(temp_file):
    empty_df.to_csv(temp_file, index=False, sep=csv_seperation_char)

if not os.path.exists(main_file):
    empty_df.to_csv(main_file, index=False, sep=csv_seperation_char)

switch_fg_color = 0
fg_color = '\033[97m'  # Escape sequence for Bright White Foreground color
bg_color = '\033[40m'  # Escape sequence for Black Background color



def main():
    start_timer = 's'
    pause_timer = 'p'
    pause_all_timer = 'pa'

    plot_stats = 'plot'
    show_stats = 'ss'
    show_all_stats = 'ssa'

    change_goal = 'c'
    change_goal_all = 'ca'

    switch = 'v'
    brightness = 'b'
    make_progress_always_fill = 'fill'
    fill = 0
    change_color_scheme = 'cc'

    quit_timer = 'q'

    title_projects = 'projects overview'.upper()
    title_progress = 'current progress monitor'.upper()

    help_text = f"{bcolors.OKCYAN}Type 'help' to list commands.\n\
Type 'v' to switch between '{title_projects}' and '{title_progress}'.{bcolors.ENDC}"
    print_help_info = 1
    show_help_page = 'help'

    def define_help():
        global help_commands, help_parameters
        help_commands = [
            f'{bcolors.OKCYAN}{start_timer}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{pause_timer}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{pause_all_timer}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{plot_stats}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{show_stats}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{show_all_stats}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{change_goal}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{change_goal_all}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{switch}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{brightness}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{make_progress_always_fill}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{change_color_scheme}{bcolors.ENDC}',
            f'{bcolors.OKCYAN}{quit_timer}{bcolors.ENDC}'
        ]
        help_parameters = [
            f'{bcolors.GREY}-#{bcolors.ENDC}',
            f'{bcolors.GREY}-# -h{bcolors.ENDC}',
            f'{bcolors.GREY}-h{bcolors.ENDC}',
            f'{bcolors.GREY}{bcolors.ENDC}',
            f'{bcolors.GREY}-s -i -r{bcolors.ENDC}']
    define_help()

    show_main_page = 1
    show_progress_page = 0

    file = open('projects.txt', 'r')
    cleaned_up = []
    projects = []
    goals = []
    reversed_colors = []
    sections = {}

    found_number_one = 0
    for line in file:
        if line[0] != '%' and len(line) > 1:
            if not found_number_one and line[0] == '#':
                found_number_one = 1
                line = line[1:]
                cleaned_up.insert(0, line)
            else:
                cleaned_up.append(line)

    try:
        for index, line in enumerate(cleaned_up):
            line = line.strip()

            if line[0] == '@':
                line = line[1:]
                sections[index - len(sections)] = line
                continue

            else:
                if line[0] == '#':
                    line = line[1:]
                splitLine = line.split(',')
                projects.append(splitLine[0])

                if len(splitLine) > 2:
                    if isNumber(splitLine[1]):
                        goals.append(float(splitLine[1]))
                    else:
                        goals.append(None)
                    if isNumber(splitLine[2]):
                        reversed_colors.append(int(splitLine[2]))
                    else:
                        reversed_colors.append(None)

                elif len(splitLine) > 1:
                    if isNumber(splitLine[1]):
                        goals.append(float(splitLine[1]))
                    else:
                        goals.append(None)
                    reversed_colors.append(None)

                else:
                    goals.append(None)
                    reversed_colors.append(None)

    except ValueError:
        cls()
        print(
            f'{bcolors.WARNING}Please make sure [reversed color] is set as an integer for every active project{bcolors.ENDC}')
        return
    file.close()

    mgr = []
    for index, project in enumerate(projects):
        goal = goals[index]
        reversed_color = reversed_colors[index]
        if type(goal) != type(None) and type(reversed_color) != type(None):
            mgr.append(timemanager(project, goal, reversed_color))
        elif type(goal) != type(None):
            mgr.append(timemanager(project, goal))
        elif type(reversed_color) != type(None):
            mgr.append(timemanager(project, reversed_color=reversed_color))
        else:
            mgr.append(timemanager(project))

    key = ['']

    tabwidth_index = 4
    progress_title = '|' + 10*' ' + 'Progress' + 10*' ' + '|'

    def quit():
        cls()
        write = 0
        for m in mgr:
            if len(m.time_vec) != 0:
                m.quit()
                write = 1
        print_progress_page(closing=True)
        if write or len(pd.read_csv(temp_file, sep=csv_seperation_char)) != 0:
            write_to_main_csv()

    def print_main_page():
        for index, project in enumerate(projects):
            try:
                section = sections[index]
            except KeyError:                
                pass
            else:
                if index != 0:
                    print()
                print(f'{bcolors.SECTION}{section}{bcolors.ENDC}')

            if mgr[index].working:
                print(f"{'#'+str(index):{tabwidth_index}}{bcolors.ACTIVE}{project}{bcolors.ENDC}")
            else:
                print(f"{'#'+str(index):{tabwidth_index}}{project}")
        print()

    def print_progress_page(closing=False):
        distance_projectname_to_next_tab = 3
        tabwidth_1 = 15
        tabwidth_2 = 10
        for m in mgr:  # find the longest project name wich is active or has worked time today
            m.update_time_worked_today()
            if len(m.project_name)+distance_projectname_to_next_tab > tabwidth_1 and (m.time_worked_today != 0 or m.working):
                tabwidth_1 = len(m.project_name) + distance_projectname_to_next_tab
        underline_length = tabwidth_index+tabwidth_1+3*tabwidth_2+len(progress_title)
        underline = underline_length*'-'
        print(f"\
{f'Projects today':{tabwidth_1+tabwidth_index}}\
{'Worked':{tabwidth_2}}\
{'Goal':{tabwidth_2}}\
{'Left':{tabwidth_2}}\
{progress_title}")
        print(underline)
        for index, m in enumerate(mgr):
            if m.time_worked_today != 0 or m.working:
                if m.time_worked_today > m.goal:
                    time_left = timedelta(0)
                else:
                    time_left = timedelta(seconds=m.goal - m.time_worked_today)
                project_name = m.project_name
                percentage = round(100*m.time_worked_today/(m.goal), 1)
                if m.working:
                    project_name = f"{bcolors.ACTIVE}{project_name}{bcolors.ENDC}"
                    tabwidth_1_c = tabwidth_1 + len(f"{bcolors.ACTIVE}{bcolors.ENDC}")
                print(f"\
{'#'+str(index):{tabwidth_index}}\
{project_name:{tabwidth_1_c if m.working else tabwidth_1}}\
{str(timedelta(seconds = m.time_worked_today)):{tabwidth_2}}\
{str(timedelta(seconds = m.goal)):{tabwidth_2}}\
{str(time_left):{tabwidth_2}}\
{colorize_percentage(percentage, m.working, len(progress_title), closing, m.reversed_color, fill)}")
        print()
        '''print(f"{bcolors.TTIME}{'Total:':{tabwidth_index + tabwidth_1}}{str(timedelta(seconds = total_time))}{bcolors.ENDC}")
        print()'''

    cls()
    cls()  # somehow, for windows cmd it has to be cleared twice to set text colors properly (bright white)
    while key != quit_timer:
        try:
            if show_main_page:
                print(f"{bcolors.TITLE}{title_projects}{bcolors.ENDC}")
                print()
                print_main_page()
                if print_help_info:
                    print(help_text)
                    print()
                key = input().split(' ')
                cls()

            if show_progress_page:
                print(f"{bcolors.TITLE}{title_progress}{bcolors.ENDC}")
                print()
                print_progress_page()
                print(f'{bcolors.OKCYAN}Press Enter to refresh the page.{bcolors.ENDC}')
                print()
                if print_help_info:
                    print(help_text)
                    print()
                key = input().split(' ')
                cls()

            if(key[0] == switch):
                show_main_page = not show_main_page
                show_progress_page = not show_progress_page
                continue

            if (key[0] == show_help_page):
                tab_title_1 = 11
                tab_title_2 = 13
                tab1 = 31
                tab2 = tab1+3
                tab3 = tab1+tab2-41
                print(f"Version: {version}")
                print()
                print(f"{'Commands':{tab_title_1}}{'Parameters':{tab_title_2}}Description\n{95*'-'}\n\
{help_commands[0]:{tab1}}{help_parameters[0]:{tab2}}start timer for project #.\n\
{help_commands[1]:{tab1}}{help_parameters[0]:{tab2}}pause timer for project #.\n\
{help_commands[2]:{tab1}}{help_parameters[3]:{tab2}}pause timer for all projects.\n\
\n\
{help_commands[3]:{tab1}}{help_parameters[0]:{tab2}}plot stats for project #.\n\
{help_commands[4]:{tab1}}{help_parameters[0]:{tab2}}show time logs of the current session for project #.\n\
{help_commands[5]:{tab1}}{help_parameters[3]:{tab2}}show time logs of the current session for all projects.\n\
\n\
{help_commands[6]:{tab1}}{help_parameters[1]:{tab2}}change current goal (in hours) for project #.\n\
{help_commands[7]:{tab1}}{help_parameters[2]:{tab2}}change current goal (in hours) for all projects.\n\
\n\
{help_commands[8]:{tab1}}{help_parameters[3]:{tab2}}switch between {title_projects} and {title_progress}.\n\
{help_commands[9]:{tab1}}{help_parameters[3]:{tab2}}change brightness of white text.\n\
{help_commands[10]:{tab1}}{help_parameters[3]:{tab2}}make the progressbars visible for inactive projects.\n\
\n\
{help_commands[11]:{tab1}}{help_parameters[4]:{tab2}}change color scheme for the progressbars with an optional start value s\n\
\033[{tab3}Cand increment i. See https://en.wikipedia.org/wiki/ANSI_escape_code\n\
\033[{tab3}Cchapter 3.4.1.2 for further information.\n\
\033[{tab3}CParameter r restores original colors.\n\
\n\
{help_commands[12]:{tab1}}{help_parameters[3]:{tab2}}pause all timers and quit application.\n\
\n\
{bcolors.WARNING}Hint:{bcolors.ENDC} For the project #0, the #-Parameter is not needed.\n")
                input('\nPress Enter to continue...')
                cls()
                continue

            if((key[0] == change_goal) or (key[0] == change_goal_all)):
                if (key[0] == change_goal_all):
                    for m in mgr:
                        m.change_goal(float(key[1]))
                    print()
                    continue
                if len(key) > 2:
                    mgr[int(key[1])].change_goal(float(key[2]))
                else:
                    mgr[0].change_goal(float(key[1]))
                print()
                continue

            if(key[0] == start_timer):
                if len(key) > 1:
                    mgr[int(key[1])].start()
                else:
                    mgr[0].start()
                continue

            if(key[0] == pause_timer):
                if len(key) > 1:
                    mgr[int(key[1])].stop()
                else:
                    mgr[0].stop()
                continue

            if(key[0] == plot_stats):
                if len(key) > 1:
                    mgr[int(key[1])].plot_statistics()
                else:
                    mgr[0].plot_statistics()
                continue

            if(key[0] == pause_all_timer):
                for m in mgr:
                    if m.working:
                        m.stop()
                continue

            if(key[0] == show_stats):
                if len(key) > 1:
                    mgr[int(key[1])].show_statistics()
                else:
                    mgr[0].show_statistics()
                continue

            if(key[0] == show_all_stats):
                for m in mgr:
                    if len(m.time_vec) != 0:
                        m.show_statistics()
                continue

            if(key[0] == brightness):
                global fg_color, switch_fg_color
                fg_color = '\033[97m' if switch_fg_color else '\033[37m'
                bcolors.ENDC = f'{fg_color}{bg_color}'
                define_help()
                switch_fg_color = not switch_fg_color
                cls()
                continue

            if(key[0] == make_progress_always_fill):
                fill = not fill
                cls()
                continue

            if(key[0] == change_color_scheme):
                if len(key) > 2:
                    update_color_scheme(int(key[1]), int(key[2]))
                elif len(key) > 1:
                    update_color_scheme(key[1])
                else:
                    update_color_scheme()
                cls()
                continue

            if(key[0] == quit_timer):
                quit()
                break
        except (IndexError, ValueError):
            cls()
            input("Please enter a valid argument. Press enter to continue...")
            cls()
        except KeyboardInterrupt:
            quit()
            break
    return 1


def cls():
    if os.name == 'nt':
        print(f'{fg_color}{bg_color}')
        os.system('cls')
    else:
        print(f'{fg_color}{bg_color}')
        os.system('clear')


class timemanager:
    def __init__(self, project_name='Project Name', goal=2, reversed_color=0):
        self.project_name = project_name
        self.reversed_color = reversed_color
        self.time_worked_today_main = self.get_seconds_worked_today(pd.read_csv(main_file, sep=csv_seperation_char))
        self.time_worked_today = 0  # in seconds
        self.goal = goal*3600  # argument comes in hours, saved in seconds
        self.time_vec = []
        self.working = 0

        self.time_0 = 0
        self.time_E = 0

        self.plot_amount_of_dates = 8  # 8 looks always nice
        self.plot_color = [182/255, 250/255, 130/255]

    def change_goal(self, goal):
        old = self.goal
        self.goal = round(goal*3600, 0)
        print(f"{bcolors.HEADER}Changed goal: {str(round(old/3600, 2))+'h':6}--> \
{str(round(self.goal/3600, 2))+'h':6}for {self.project_name}{bcolors.ENDC}")

    def update_time_worked_today(self):
        time = self.time_worked_today_main + \
            self.get_seconds_worked_today(pd.read_csv(temp_file, sep=csv_seperation_char))
        if self.working:
            delta = datetime.now() - self.time_0
            time += delta.days*24*3600 + delta.seconds
        self.time_worked_today = time

    def get_seconds_worked_today(self, df):
        today = datetime.now().strftime(date_format)
        df = df.loc[(df['project_name'] == self.project_name) & (df['start_date'] == today)]
        df = df.groupby(['start_date']).sum().sort_values('start_date', ascending=True)
        df = df.reset_index()
        if len(df):
            return int(df['seconds_worked'])
        else:
            return 0

    def start(self):
        if not self.working:
            self.update_stats("start")
            self.working = 1
        else:
            print(f"{bcolors.WARNING}you're already working on '{self.project_name}'...{bcolors.ENDC}")
            print()

    def stop(self):
        if self.working:
            self.update_stats("stop")
            self.working = 0
        else:
            print(f"{bcolors.WARNING}you're not working on '{self.project_name}'...{bcolors.ENDC}")
            print()

    def quit(self):
        if self.working:
            self.update_stats("stop")
            self.working = 0
        self.print_stats()
        print()

    def update_stats(self, str):
        time = datetime.now()
        time_str = time.strftime(date_time_format)
        self.time_vec.append(f"{time_str} --> {str}:\t{self.project_name}")
        if str == 'start':
            self.time_0 = time
        if str == 'stop':
            self.time_E = time
            delta = self.time_E-self.time_0
            self.time_worked = delta.days*24*3600 + delta.seconds
            self.write_to_temp_csv()

    def print_stats(self):
        for i in self.time_vec:
            print(f"{bcolors.HEADER}{i}{bcolors.ENDC}")

    def write_to_temp_csv(self):
        df = pd.read_csv(temp_file, sep=csv_seperation_char)
        df = df.append({
            'project_name': self.project_name,
            'start_date': self.time_0.strftime(date_format),
            'start_time': self.time_0.strftime(time_format),
            'stop_date': self.time_E.strftime(date_format),
            'stop_time': self.time_E.strftime(time_format),
            'seconds_worked': self.time_worked
        }, ignore_index=True)
        while True:
            try:
                df.to_csv(temp_file, index=False, sep=csv_seperation_char)
            except PermissionError:
                print(f"{bcolors.WARNING}Could not write to '{temp_file}'. Please close the file and try again.{bcolors.ENDC}")
                input("Press Enter to try again...")
                cls()
            else:
                break

    def plot_statistics(self, limit_in_h=0):
        plt_df = pd.read_csv(main_file, sep=csv_seperation_char)
        plt_df = plt_df.loc[plt_df['project_name'] == self.project_name]
        if len(plt_df) == 0:
            input("No data to plot. Press Enter to continue...")
            cls()
            return
        plt_df = plt_df.groupby(['start_date']).sum().sort_values('start_date', ascending=True)
        plt_df = plt_df.reset_index()

        x = [datetime.strptime(d, date_format).date() for d in plt_df['start_date']]
        y = plt_df['seconds_worked']/3600

        '''threshold_25 = (self.goal/3600)*25/100
        threshold_50 = (self.goal/3600)*50/100
        threshold_75 = (self.goal/3600)*75/100
        threshold_100 = (self.goal/3600)

        mask_0_to_25 = y < threshold_25
        mask_25_to_50 = y>=threshold_25 and y < threshold_50
        mask_50_to_75 = y>=threshold_50 and y < threshold_75
        mask_75_to_100 = y>=threshold_75 and y < threshold_100
        mask_100_plus = y >= threshold_100'''

        days = max(x) - min(x)
        interv = int(days.days/self.plot_amount_of_dates) if days.days > self.plot_amount_of_dates else 1

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interv))
        plt.bar(x, y, color=self.plot_color)
        plt.title(self.project_name)
        plt.ylabel("time [h]")
        if limit_in_h:
            plt.ylim(top=limit_in_h)
        plt.gcf().autofmt_xdate()
        plt.show()

    def show_statistics(self):
        if len(self.time_vec):
            self.print_stats()
            print()


def write_to_main_csv():
    df1 = pd.read_csv(main_file, sep=csv_seperation_char)
    df2 = pd.read_csv(temp_file, sep=csv_seperation_char)
    df1 = df1.append(df2)
    while True:
        try:
            df1.to_csv(main_file, index=False, sep=csv_seperation_char)
        except PermissionError:
            print(f"{bcolors.WARNING}Could not write '{main_file}'. Please close the file and try again.{bcolors.ENDC}")
            input("Press Enter to try again...")
            print(2*'\033[1F\033[2K'+'\033[1F')  # delete input line above
        else:
            print(f"{bcolors.OKGREEN}Wrote the data from '{temp_file}' successfully to '{main_file}'.{bcolors.ENDC}")
            while True:
                try:
                    empty_df.to_csv(temp_file, index=False, sep=csv_seperation_char)
                except PermissionError:
                    print(f"{bcolors.WARNING}Could not clear '{temp_file}'. Please close the file and try again.{bcolors.ENDC}")
                    input("Press Enter to try again...")
                    print(2*'\033[1F\033[2K'+'\033[1F')  # delete input line above
                else:
                    print(f"{bcolors.OKGREEN}Cleared {temp_file}.{bcolors.ENDC}")
                    break
            break
    print()


def colorize_percentage(percentage, working, progressbar_length, closing, reversed_color, fill):
    percentages_color_lookup = [100, 75, 50, 25, 0]

    percentages_color_distribution = percentages_color_lookup
    percentage_for_color = percentage

    if reversed_color:
        percentages_color_distribution = [75, 50, 25, 1, 0]
        if percentage <= 100:
            percentage_for_color = 100-percentage
        else:
            percentage_for_color = 0

    for index, p in enumerate(percentages_color_lookup):
        if percentage_for_color >= percentages_color_distribution[index]:
            if working or closing or fill:
                progress = int(round(progressbar_length*percentage/100, 0))
                '''if progress == 0:
                    progress = 1'''
                p_only = str(percentage) + '%'
                p_text = p_only + ' '*(progressbar_length - len(p_only))
                p_text_in = p_text[:progress]
                p_text_in = f"{bcolors.percentage_colors[f'P{p}_b']}{p_text_in}{bcolors.ENDC}"
                p_text_out = f"{bcolors.percentage_colors[f'P{p}_f']}{p_text[progress:]}{bcolors.ENDC}"
                text = p_text_in + p_text_out
                ansi_length = len(f"{bcolors.percentage_colors[f'P{p}_b']}{bcolors.ENDC}")
                break
            else:
                text = f"{bcolors.percentage_colors[f'P{p}_f']}{percentage}%{bcolors.ENDC}"
                ansi_length = len(f"{bcolors.percentage_colors[f'P{p}_f']}{bcolors.ENDC}")
                break
    return text


class bcolors:
    #TITLE = '\033[38;5;144m'
    TITLE = '\033[38;2;170;185;89m'
    SECTION = '\033[38;5;80m'
    HEADER = '\033[38;5;170m'
    TTIME = '\033[38;5;208m'
    BLACK = '\033[30m'
    WHITE = '\033[38;5;15m'
    GREY = '\033[38;5;245m'
    BRIGHT_BLACK = '\033[90m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[38;5;75m'
    OKGREEN = '\033[38;5;78m'
    WARNING = '\033[38;5;221m'
    FAIL = '\033[38;5;203m'
    ENDC = f'{fg_color}{bg_color}'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ACTIVE = '\033[48;5;80m\033[38;5;0m'

    Progress_RED = 124
    Progress_ORANGE = 166
    Progress_YELLOW_1 = 220
    Progress_YELLOW_2 = 190
    Progress_GREEN = 40

    percentage_colors = {
        'P0_f': f'\033[38;5;{Progress_RED}m',
        'P0_b': f'\033[48;5;{Progress_RED}m\033[38;5;0m',
        'P25_f': f'\033[38;5;{Progress_ORANGE}m',
        'P25_b': f'\033[48;5;{Progress_ORANGE}m\033[38;5;0m',
        'P50_f': f'\033[38;5;{Progress_YELLOW_1}m',
        'P50_b': f'\033[48;5;{Progress_YELLOW_1}m\033[38;5;0m',
        'P75_f': f'\033[38;5;{Progress_YELLOW_2}m',
        'P75_b': f'\033[48;5;{Progress_YELLOW_2}m\033[38;5;0m',
        'P100_f': f'\033[38;5;{Progress_GREEN}m',
        'P100_b': f'\033[48;5;{Progress_GREEN}m\033[38;5;0m'}


def update_color_scheme(start=93, inc=6):
    if start == 'r':
        Progress_RED = 124
        Progress_ORANGE = 166
        Progress_YELLOW_1 = 220
        Progress_YELLOW_2 = 190
        Progress_GREEN = 40
    else:
        start = start
        inc = inc
        Progress_RED = start
        Progress_ORANGE = start + inc
        Progress_YELLOW_1 = start + 2*inc
        Progress_YELLOW_2 = start + 3*inc
        Progress_GREEN = start + 4*inc

    bcolors.percentage_colors = {
        'P0_f': f'\033[38;5;{Progress_RED}m',
        'P0_b': f'\033[48;5;{Progress_RED}m\033[38;5;0m',
        'P25_f': f'\033[38;5;{Progress_ORANGE}m',
        'P25_b': f'\033[48;5;{Progress_ORANGE}m\033[38;5;0m',
        'P50_f': f'\033[38;5;{Progress_YELLOW_1}m',
        'P50_b': f'\033[48;5;{Progress_YELLOW_1}m\033[38;5;0m',
        'P75_f': f'\033[38;5;{Progress_YELLOW_2}m',
        'P75_b': f'\033[48;5;{Progress_YELLOW_2}m\033[38;5;0m',
        'P100_f': f'\033[38;5;{Progress_GREEN}m',
        'P100_b': f'\033[48;5;{Progress_GREEN}m\033[38;5;0m'}


def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        try:
            float(s)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    if main():
        print(f"{bcolors.OKCYAN}Thanks for using the WorkTime Logger! See you soon, hopefully!{bcolors.ENDC}")
        input("Press Enter to proceed closing...")
        print('\033[1F\033[2K')  # delete input line above
        print('\033[0m\033[1F')  # reset console colors to default
