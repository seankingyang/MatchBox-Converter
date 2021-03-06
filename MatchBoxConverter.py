# from tksheet import Sheet
import os
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

# from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
import tksheet
#Version: 1.0.4
def grabFileListWithSuffix(folder_path, suffix=None):
    fileList = os.listdir(folder_path)
    if suffix is None or suffix == "":
        return fileList
    fileList = [file for file in fileList if suffix in file]
    return fileList
def grabFilePrefix(fileName, main_name):
    return fileName.replace(main_name,"")


def updateCSV(new_df, org_df):
    org_tech_Name = [tech for tech in org_df["TestName"] if str(tech) != "nan"]
    new_tech_Name = [tech for tech in new_df["TestName"] if str(tech) != "nan"]
    org_tech_idx = sorted([len(org_df.index)] + [org_df.index[org_df["TestName"] == tech].tolist().pop() for tech in
                                                 list(dict.fromkeys(org_tech_Name))])
    new_tech_idx = sorted([len(new_df.index)] + [new_df.index[new_df["TestName"] == tech].tolist().pop() for tech in
                                                 list(dict.fromkeys(new_tech_Name))])
    org_tech_Name_andRange = {org_tech_Name[i]: [org_tech_idx[i], org_tech_idx[i + 1] - 1] for i in
                              range(len(org_tech_Name))}
    new_tech_Name_andRange = {new_tech_Name[i]: [new_tech_idx[i], new_tech_idx[i + 1] - 1] for i in
                              range(len(new_tech_Name))}
    for tech_Name in new_tech_Name_andRange:
        if tech_Name in org_tech_Name_andRange:
            range_idx = org_tech_Name_andRange[tech_Name]
            org_df = org_df.drop([idx for idx in range(range_idx[0], range_idx[1] + 1)])
    return pd.concat([new_df, org_df], axis=0).reset_index(drop=True)

def createCSV(header, path, data):
    df = pd.DataFrame(data, columns=header)
    df.to_csv(path, index=False)



class MatchBoxUI:
    def __init__(self):
        self.sheet = None
        self.now_path = os.path.dirname(__file__)
        self.csv_file_path = None
        # self.csv_file_path = self.now_path+"/Data/MasterPlan.csv"
        self.root = tk.Tk()
        # self.root.iconbitmap('./Icon/P2.ico')
        self.root.iconphoto(True, tk.PhotoImage(file=self.now_path + '/Icon/Icon.png'))
        self.root.title("MatchBox+ MasterPlan Converter UI")
        self.root.geometry("1920x800")

        self.frame = tk.Frame(self.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.root.columnconfigure(0, weight=100)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1000)

        self.style = ttk.Style(self.root)
        self.style.theme_use('alt')
        self.isDark_theme = False

        self.warning_label = ttk.Label(text="Please import the existed CSV file", style="warning.TLabel")
        self.ImportFilepath_label = ttk.Label(text='MasterPlan File Path', style="normal.TLabel")
        self.v = tk.StringVar()
        self.Import_entry = ttk.Entry(textvariable=self.v, width=100, style="normal.TEntry")
        self.Import_entry.state(['disabled'])
        self.Import_Btn = ttk.Button(text='Import CSV file', command=self.import_csv_data, width=15,
                                     style="normal.TButton")
        self.SaveOnly_Btn = ttk.Button(text='Save only ', command=self.save_csv_data, width=15,
                                       style="normal.TButton")
        self.SaveAndConvert_Btn = ttk.Button(text='Save & Convert', command=self.saveAndConvert_csv_data, width=15,
                                             style="normal.TButton")
        # self.SaveAndConvert_Btn.state(['disabled'])
        self.Change_Theme_Btn = ttk.Button(text='Change Theme', command=self.Change_theme, width=15,
                                           style="normal.TButton")
        self.Close_Btn = ttk.Button(text='Close', command=self.root.destroy, width=15, style="close.TButton")
        self.Status_label = ttk.Label(text="Status: Idle", style="warning.TLabel")
        self.revert_BTN = ttk.Button(style="normal.TButton", width=10, command=self.reverter)


        self.ImportFilepath_label.grid(row=1, column=0)
        self.Import_entry.grid(row=2, column=0)
        self.Import_Btn.grid(row=2, column=1)
        self.SaveOnly_Btn.grid(row=3, column=1)
        self.SaveAndConvert_Btn.grid(row=4, column=1)
        self.Change_Theme_Btn.grid(row=5, column=1)
        self.Close_Btn.grid(row=6, column=1)
        self.Status_label.grid(row=6, column=0, sticky="w")
        self.SaveOnly_Btn.state(['disabled'])
        self.SaveAndConvert_Btn.state(['disabled'])
        self.revert_BTN.grid(row=0, column=1,ipady=5, ipadx=5)

        self.Change_theme()

    def Change_theme(self):
        self.isDark_theme = False if self.isDark_theme else True
        self.theme_setting(self.isDark_theme)

    def theme_setting(self, isDark_theme=True):
        # True is dark theme
        if isDark_theme:
            self.root.configure(background='#3d3d3d')
            # theme 'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
            self.style.configure("warning.TLabel", foreground="red", background="#3d3d3d",
                                 font=('Times New Roman', '20'))
            self.style.configure("normal.TLabel", foreground="#f4f4f4", background="#3d3d3d",
                                 font=('Times New Roman', '16'))
            self.style.configure("normal.TEntry", foreground="#3d3d3d", background="#3d3d3d",
                                 font=('Times New Roman', '16'))
            self.style.configure("normal.TButton", foreground="#f4f4f4", background="#606060",
                                 font=('Times New Roman', '16'))
            self.style.configure("close.TButton", foreground="#f4f4f4", background="#606060",
                                 font=('Times New Roman', '16'))
            self.style.map('normal.TButton', background=[('active', 'black')])
            self.style.map('close.TButton', background=[('active', 'red')])
            self.style.map('normal.TEntry', background=[('disabled', 'black')], foreground=[('disabled', '#505050')])
            self.bg_color = '#3d3d3d'
            self.fg_color = '#f4f4f4'
            self.theme = "dark blue"
            self.logo = tk.PhotoImage(file=self.now_path + '/Icon/Icon5050.gif')
        else:
            self.root.configure(background='#f4f4f4')
            # theme 'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
            self.style.configure("warning.TLabel", foreground="red", background="#f4f4f4",
                                 font=('Times New Roman', '20'))
            self.style.configure("normal.TLabel", foreground="#3d3d3d", background="#f4f4f4",
                                 font=('Times New Roman', '16'))
            self.style.configure("normal.TEntry", foreground="#3d3d3d", background="#f4f4f4",
                                 font=('Times New Roman', '16'))
            self.style.configure("normal.TButton", foreground="#3d3d3d", background="#e0e0e0",
                                 font=('Times New Roman', '16'))
            self.style.configure("close.TButton", foreground="#3d3d3d", background="#e0e0e0",
                                 font=('Times New Roman', '16'))
            self.style.map('normal.TButton', background=[('active', '#909090')])
            self.style.map('close.TButton', background=[('active', '#f96060')])
            self.style.map('normal.TEntry', background=[('disabled', '#3d3d3d')], foreground=[('disabled', '#505050')])
            self.bg_color = '#f4f4f4'
            self.fg_color = '#3d3d3d'
            self.theme = "light blue"
            self.logo = tk.PhotoImage(file=self.now_path + '/Icon/Icon5050_rev.gif')
        self.revert_BTN.configure(image=self.logo)
        # ttk.Button(image=self.logo, style="normal.TButton", width=10, command=self.reverter).grid(row=0, column=1,
        #                                                                                           ipady=5, ipadx=5)
        try:
            self.sheet.change_theme(theme=self.theme)
        except:
            self.show_sheet()

    def show_sheet(self):
        if self.csv_file_path is None or self.csv_file_path == "" or not os.path.isfile(
                self.csv_file_path) or ".csv" not in self.csv_file_path:
            self.SaveAndConvert_Btn.state(['disabled'])
            self.SaveOnly_Btn.state(['disabled'])
            self.show_table = [[]]
            try:
                self.sheet.set_sheet_data(self.show_table, reset_col_positions=True, reset_row_positions=True,
                                          redraw=True, verify=False, reset_highlights=True)
                self.sheet.grid_forget()
            except:
                pass
            self.frame.grid_forget()
            self.warning_label.grid(row=0)
            return

        self.warning_label.grid_remove()
        self.df = pd.read_csv(self.csv_file_path)
        self.table_header = [list(self.df.columns.values)]
        self.table_values = [[string if f"{string}" != "nan" else "" for string in row] for row in self.df.values]
        self.show_table = self.table_header + self.table_values
        self.sheet = tksheet.Sheet(self.frame)
        self.sheet.set_sheet_data(self.show_table, reset_col_positions=True, reset_row_positions=True, redraw=True,
                                  verify=False, reset_highlights=True)

        # theme (str) options (themes) are light blue, light green, dark blue and dark green.
        self.sheet.change_theme(theme=self.theme)
        self.sheet.header_font(newfont=("Arial", 12, "bold"))
        self.sheet.font(newfont=("Arial", 12, "bold"), reset_row_positions=True)
        self.sheet.highlight_rows(rows=[0], bg="yellow", fg="black", highlight_index=True, redraw=True)
        if "MasterPlan.csv" in self.csv_file_path:
            self.SaveAndConvert_Btn.state(['!disabled'])
            for i in range(26):
                color = "Red" if i < 13 else "blue"
                self.sheet.highlight_cells(row=0, column=i, cells=[], canvas="table", bg="yellow", fg=color,
                                           redraw=True)
        else:
            self.SaveAndConvert_Btn.state(['disabled'])
        self.sheet.set_all_cell_sizes_to_text(redraw=True)
        self.sheet.enable_bindings()
        self.sheet.edit_bindings(True)
        self.sheet.set_options(enable_edit_cell_auto_resize=True)
        self.frame.grid(row=0, sticky="nsew")
        self.sheet.grid(row=0, sticky="nsew")
        self.SaveOnly_Btn.state(['!disabled'])

    def import_csv_data(self, isNeedImportData=True):
        if isNeedImportData:
            self.setStatus_label()
            self.csv_file_path = tkinter.filedialog.askopenfilename()
        self.v.set(self.csv_file_path)
        if os.path.isfile(self.csv_file_path):
            self.show_sheet()

    def save_csv_data_func(self):
        self.newSheet = self.sheet.get_sheet_data(return_copy=False, get_header=False, get_index=False)
        self.df = pd.DataFrame(self.newSheet[1:], columns=self.newSheet[0])
        self.df.to_csv(self.csv_file_path, index=False)

    def setStatus_label(self, string="Idle"):
        self.Status_label.configure(text="Status: " + string)

    def save_csv_data(self):
        self.setStatus_label()
        self.setStatus_label("Saving...")
        self.save_csv_data_func()
        self.setStatus_label("Saving...Done!")

    def saveAndConvert_csv_data(self):
        self.setStatus_label()
        self.setStatus_label("Saving...")
        self.save_csv_data_func()
        self.setStatus_label("Saving...Converting...")
        self.converter = MatchBoxConverter(self.csv_file_path)
        self.converter.ConvertGroup()
        self.converter.ConvertTech()
        self.setStatus_label("Saving...Converting...Done!")

    def reverter(self):
        main_path = tkinter.filedialog.askopenfilename()
        main_fileName = main_path.split("/")[-1].replace(".csv","")
        if "Main" not in main_fileName:
            return -1
        asserts_folder = main_path.replace(main_path.split("/")[-1], "")
        # print(asserts_folder)
        self.v.set(asserts_folder)
        self.reverter = MatchBoxReverter(asserts_folder, main_fileName)
        self.reverter.process_tech()
        self.reverter.process_group()
        self.csv_file_path = self.reverter.createMasterPlan()
        self.import_csv_data(False)



class MatchBoxConverter:
    def __init__(self, path):
        self.masterplan_path = path
        self.df = pd.read_csv(self.masterplan_path)
        self.main_prefix = grabFilePrefix(str.split(self.masterplan_path, "/")[-1], "MasterPlan.csv")
        self.folder = str.replace(self.masterplan_path, "/" + str.split(self.masterplan_path, "/")[-1], "")
        self.group_header = ["TestName", "Technology", "Disable", "Production", "Audit", "Thread", "Policy", "Loop",
                             "Sample", "SOF", "Condition", "Notes"]
        self.tech_header = ["TestName", "TestActions", "Disable", "Input", "Output", "Timeout", "Retries",
                            "AdditionalParameters", "ExitEarly", "SetPoison", "Commands", "FA", "Condition", "Notes"]
        self.FATech_header = ["TestName", "TestActions", "Disable", "Input", "Output", "Timeout", "Retries",
                              "AdditionalParameters", "Commands", "Condition", "Notes"]

        self.tech_folder = self.folder + "/Tech"
        if not os.path.isdir(self.tech_folder):
            os.mkdir(self.tech_folder)


    def ConvertGroup(self):
        # ===========================================
        # ================== GROUP ==================
        # ===========================================
        if self.main_prefix is not None and self.main_prefix != "":
            group = ["Init", self.main_prefix + "Main", "Teardown"]
        else:
            group = ["Init", "Main", "Teardown"]
        df = self.df.drop(
            columns=["TestActions", "Input", "Output", "Timeout", "Retries", "AdditionalParameters", "ExitEarly",
                     "SetPoison", "Commands", "FA"])

        group_idx = df.index[df["Group"].notnull()].tolist() + [len(df.index)]
        group_idx.sort()
        group_idx_range = []
        for i in range(len(group_idx) - 1):
            group_idx_range.append([group_idx[i], group_idx[i + 1] - 1])

        for i in range(len(group)):
            file = self.folder + "/" + group[i] + ".csv"
            group_key = {}
            idx_range = group_idx_range[i]
            for j in range(idx_range[0], idx_range[1] + 1):
                if str(df["TestName"].iloc[j]) != "nan":
                    for header in self.group_header:
                        if header in group_key:
                            group_key[header] += [df[header].iloc[j]]
                        else:
                            group_key[header] = [df[header].iloc[j]]
            # print(group_key)
            createCSV(self.group_header, file, group_key)

    def ConvertTech(self):
        # ===========================================
        # ================== TECH ===================
        # ===========================================
        df = self.df.drop(columns=["Group", "Production", "Audit", "Thread", "Policy", "Loop", "Sample", "SOF"])

        tech_Technology_testName_idxrange = {}
        tech_Technology = [tech for tech in df["Technology"] if str(tech) != "nan"]
        tech_TestName = [tech for tech in df["TestName"] if str(tech) != "nan"]

        tech_idx = [len(df.index)]
        for tech in list(dict.fromkeys(tech_Technology)):
            tech_idx += df.index[df["Technology"] == tech].tolist()
        tech_idx.sort()

        tech_idx_range = [[tech_idx[i], tech_idx[i + 1] - 1] for i in range(len(tech_idx) - 1)]

        if len(tech_Technology) == len(tech_TestName):
            for i in range(len(tech_Technology)):
                Technology = tech_Technology[i]
                TestName = tech_TestName[i]
                if Technology not in tech_Technology_testName_idxrange:
                    tech_Technology_testName_idxrange[Technology] = {TestName: tech_idx_range[i]}
                else:
                    if TestName not in tech_Technology_testName_idxrange[Technology]:
                        tech_Technology_testName_idxrange[Technology][TestName] = tech_idx_range[i]
        tech_fom = {}
        for Technology in tech_Technology_testName_idxrange:
            if Technology in tech_fom:
                tech_key = tech_fom[Technology]
            else:
                tech_key = {}
            for TestName in tech_Technology_testName_idxrange[Technology]:
                idx_range = tech_Technology_testName_idxrange[Technology][TestName]
                for i in range(idx_range[0] + 1, idx_range[1] + 1):
                    for header in self.tech_header:
                        if header == "TestName":
                            if header in tech_key:
                                tech_key[header] += [df[header].iloc[i - 1]]
                            else:
                                tech_key[header] = [df[header].iloc[i - 1]]
                        else:
                            if header in tech_key:
                                tech_key[header] += [df[header].iloc[i]]
                            else:
                                tech_key[header] = [df[header].iloc[i]]
            tech_fom[Technology] = tech_key

        for tech in tech_fom:
            if tech == "Failure":
                file = self.folder + "/" + tech + ".csv"
                header = self.FATech_header
            else:
                file = self.tech_folder + "/" + tech + ".csv"
                header = self.tech_header
            data = tech_fom[tech]
            if os.path.isfile(file):
                new_df = pd.DataFrame(tech_fom[tech], columns=header)
                org_df = pd.read_csv(file)
                final_df = updateCSV(new_df, org_df)
                data = final_df.values
            # print(file)
            createCSV(header, file, data)





class MatchBoxReverter:
    def __init__(self, Asserts_folder,Main_fileName):
        self.group_df_dic = {}
        self.tech_df_dic = {}
        self.asserts_folder = Asserts_folder
        self.main_fileName = Main_fileName
        self.main_prefix = grabFilePrefix(self.main_fileName,"Main")
        self.tech_folder = self.asserts_folder + "Tech/"
        self.group_header = ["TestName", "Technology", "Disable", "Production", "Audit", "Thread", "Policy", "Loop",
                             "Sample", "SOF", "Condition", "Notes"]
        self.tech_header = ["TestName", "TestActions", "Disable", "Input", "Output", "Timeout", "Retries",
                            "AdditionalParameters", "ExitEarly", "SetPoison", "Commands", "FA", "Condition", "Notes"]
        self.MasterPlan_header = ["Group", "TestName", "Technology", "TestActions", "Disable", "Production", "Audit",
                                  "Thread", "Policy", "Loop", "Sample", "SOF", "Condition", "Input", "Output",
                                  "Timeout", "Retries", "AdditionalParameters", "ExitEarly", "SetPoison", "Commands",
                                  "FA", "Notes"]


    def process_tech(self):
        tech_file_list = [file.replace(".csv", "") for file in grabFileListWithSuffix(self.tech_folder, ".csv")]
        tech_file_list += ["Failure"]
        self.tech_df_dic = {}
        for file in tech_file_list:
            if file == "Failure":
                df = pd.read_csv(self.asserts_folder + file + ".csv")
            else:
                df = pd.read_csv(self.tech_folder + file + ".csv")
            df_header = list(df.columns.values)
            for header in self.MasterPlan_header:
                if header not in df_header:
                    df[header] = np.nan
            df = df[self.MasterPlan_header]
            tech_TestName = [tech for tech in df["TestName"] if str(tech) != "nan"]
            tech_idx = [len(df.index)]
            for tech in list(dict.fromkeys(tech_TestName)):
                tech_idx += df.index[df["TestName"] == tech].tolist()
            tech_idx.sort()
            tech_Name_andRange = {tech_TestName[i]: [tech_idx[i], tech_idx[i + 1] - 1] for i in
                                  range(len(tech_TestName))}
            df["TestName"] = np.nan
            for testName in tech_Name_andRange:
                idx_range = tech_Name_andRange[testName]
                if file not in self.tech_df_dic:
                    self.tech_df_dic[file] = {}
                self.tech_df_dic[file][testName] = df.iloc[idx_range[0]: idx_range[1] + 1]


    def process_group(self):
        # ["Init", "Main", "Teardown"]
        group_file_list = ["Init", self.main_prefix+"Main", "Teardown","Failure"]
        for file in group_file_list:
            if file == "Main":
                file_path = self.asserts_folder + self.main_prefix + file + ".csv"
            else:
                file_path = self.asserts_folder + file + ".csv"
            df = pd.read_csv(file_path)
            df_header = list(df.columns.values)
            if file == "Failure":
                df = df.loc[df['TestName'].notnull()]
                for header in df_header:
                    if header not in self.group_header:
                        df[header] = np.nan
            for header in self.MasterPlan_header:
                if header not in df_header:
                    np.array([file])
                    df[header] = np.nan

            try:
                if "Main" in file:
                    df["Group"].iloc[0] = "Main"
                else:
                    df["Group"].iloc[0] = file
            except:
                pass
            self.group_df_dic[file] = df[self.MasterPlan_header]


    def createMasterPlan(self):
        ## Combine GROUP DF to TEMP MASTER PLAN ##
        temp_master_plan = pd.concat(
            [self.group_df_dic["Init"], self.group_df_dic[self.main_fileName], self.group_df_dic["Teardown"], self.group_df_dic["Failure"] ],
            axis=0).reset_index(drop=True)
        # print(temp_master_plan)
        ## Separate the TEMP MASTER PLAN and Combine the TECH DF ##
        master_plan = pd.DataFrame([], columns=self.MasterPlan_header)
        FA_flag = False
        for i in range(len(temp_master_plan.index)):
            test_Name = temp_master_plan["TestName"].iloc[i]
            tech = temp_master_plan["Technology"].iloc[i]

            if  temp_master_plan["Group"].iloc[i] == "Failure":
                FA_flag = True
            if FA_flag:
                tech = "Failure"
                temp_master_plan["Technology"].iloc[i] = tech
            try:
                master_plan = pd.concat(
                    [master_plan, temp_master_plan.iloc[i:i + 1], self.tech_df_dic[tech][test_Name]],
                    axis=0).reset_index(drop=True)
            except:
                print("test_Name:", test_Name, ";tech: ", tech)
                pass

        master_plan = master_plan[self.MasterPlan_header]
        master_plan.to_csv(self.asserts_folder +self.main_prefix +"MasterPlan.csv", index=False)
        return self.asserts_folder +self.main_prefix +"MasterPlan.csv"


app = MatchBoxUI()
app.root.mainloop()
