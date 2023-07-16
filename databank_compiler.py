'''
# JSON compiler v0.93 by Lumyni, requires https://www.python.org/
# Meant for C.R's "Databank Project"
# Messes with files, only modify if you know what you are doing!
'''

import os, importlib, sys, locale, ctypes, json
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
from importlib import util
from importlib import machinery

def import_required_modules(modules):
    for (module,link,targetversion) in modules:
        parameters = ""
        try:
            moduleobj = __import__(module)
            globals()[module] = moduleobj
            version = moduleobj.__version__.replace('.','')
            if version < targetversion:
                parameters = "--upgrade"
                print(f"An inferior version of the module '{module}' was found ({version} vs {targetversion}).")
                consent = input("Would you like to continue trying to run the app anyways? NOT RECOMMENDED (Y/n) ")
                if not(consent.upper() == "Y"):
                    print("Operation denied by user.")
                    raise Exception(f"Inferior version ({version} vs {targetversion}).")
                else:
                    print("Oh well. Trying to run the app anyways...")
            elif targetversion != '0' and version > targetversion:
                print(f"WARNING: Current version of '{module}' ({version}) is higher than the one used in this script ({targetversion}).")
        except Exception as reason:
            print(f"Couldn't find the required module '{module}'{link} \nReason: {reason}")
            consent = input(f"Would you like to automatically install it now with 'pip install {module} {parameters}'? (Y/n) ")
            pendingExit = False
            if consent.upper() == "Y":
                print("Operation accepted by user.")
                os.system(f'pip install {module} {parameters}')
                try:
                    moduleobj = __import__(module)
                    globals()[module] = moduleobj
                except:
                    print("\nCouldn't automatically install module, it is likely that this script cannot access pip.")
                    pendingExit = True
            else:
                print("Operation denied by user.")
                pendingExit = True
            if pendingExit == True:
                print(f"Please install {module} before reopening this app.")
                input("(Press enter to quit)\n")
                quit()

def import_path(path):
    module_name = os.path.basename(path).replace('-', '_')
    spec = importlib.util.spec_from_loader(
        module_name,
        importlib.machinery.SourceFileLoader(module_name, path)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    return module

def substring_before(s, delim): return s.partition(delim)[0]
def substring_after(s, delim): return s.partition(delim)[2]

def json_dump(dictionary): return json.dumps(dictionary, indent=None)

def json_export(json_object):
    try:
        with open("databank_scan.json", "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        print(f"ERROR: {e}")
        messagebox.showwarning(title='Warning', message="Something went wrong while trying to export data as JSON.\nCheck the console for details.")

def read_entries(path, debugmode=0):
    data = {"properties":[],"entries":[]}
    try:
        #data['properties'].append({"bankname":os.path.basename(os.path.normpath(path))})
        data['properties'].append({"bankpath":path})
        print("Found path.\n")
    except:
        messagebox.showerror(title='Error', message="The directory provided was not valid.")
        return
    invalid = False
    missing = False
    entrycount = 0

    for subdir, dirs, files in os.walk(path):
        for entry in dirs:
            if entry.endswith("__pycache__"): continue

            id = substring_before(str(entry), "_")
            filename = substring_after(str(entry), "_")

            try: int(id)
            except: print(f"Found invalid entry: {entry}"); continue
            
            if debugmode: print(f"~* ENTRY FOUND *~\nID: {id}\nFilename: {filename}")
            else: print(f"* ENTRY {id} FOUND: {filename}")
            entrycount += 1
            location = os.path.join(subdir, entry)
            statsfile = os.path.join(location, "stats.txt")

            stats = None
            try: stats = import_path(statsfile)
            except:
                data['entries'].append({"id":id,"filename":filename,"path":location})
                try: os.unlink(os.path.join(location, "stats_INVALID.txt"))
                except: pass
                try:
                    os.rename(statsfile, os.path.join(location,"stats_INVALID.txt"))
                    print("The stats file from this entry is invalid!")
                    invalid = True
                except:
                    print("Couldn't find the stats file from this entry.")
                    missing = True
            
            if stats and debugmode:
                if hasattr(stats, 'yo'): print(f"yo: {str(stats.yo)}")
                if hasattr(stats, 'Name'): print(f"Name: {str(stats.Name)}")
                if hasattr(stats, 'Alias'): print(f"Alias: {str(stats.Alias)}")
                if hasattr(stats, 'Rank'): print(f"Rank: {str(stats.Rank)}")
                if hasattr(stats, 'RVE'): print(f"RVE: {str(stats.RVE)}")
                if hasattr(stats, 'Class'): print(f"Class: {str(stats.Class)}")
                if hasattr(stats, 'Height'): print(f"Height: {str(stats.Height)}")
                if hasattr(stats, 'Weight'): print(f"Weight: {str(stats.Weight)}")
                if hasattr(stats, 'Race'): print(f"Race: {str(stats.Race)}")
                if hasattr(stats, 'FirstEncounter'): print(f"FirstEncounter: {str(stats.FirstEncounter)}")
                if hasattr(stats, 'Age'): print(f"Age: {str(stats.Age)}")
                if hasattr(stats, 'Gender'): print(f"Gender: {str(stats.Gender)}")
                if hasattr(stats, 'Spellbook'): print(f"Spellbook: {str(stats.Spellbook)}")
                if hasattr(stats, 'Description'): print(f"Description: {str(stats.Description)}")
                if hasattr(stats, 'ImageName'): print(f"ImageName: {str(stats.ImageName)}")
            if debugmode: print()
            entrydata = {
                "id":id,
                "filename":filename,
                "yo":stats.yo if hasattr(stats, 'yo') else None,
                "Name":stats.Name if hasattr(stats, 'Name') else None,
                "Alias": stats.Alias if hasattr(stats,'Alias') else None,
                "Rank": stats.Rank if hasattr(stats,'Rank') else None,
                "RVE": stats.RVE if hasattr(stats,'RVE') else None,
                "Class": stats.Class if hasattr(stats,'Class') else None,
                "Height": stats.Height if hasattr(stats,'Height') else None,
                "Weight": stats.Weight if hasattr(stats,'Weight') else None,
                "Race": stats.Race if hasattr(stats,'Race') else None,
                "FirstEncounter": stats.FirstEncounter if hasattr(stats,'FirstEncounter') else None,
                "Age": stats.Age if hasattr(stats,'Age') else None,
                "Gender": stats.Gender if hasattr(stats,'Gender') else None,
                "Spellbook": stats.Spellbook if hasattr(stats,'Spellbook') else None,
                "Description": stats.Description if hasattr(stats,'Description') else None,
                "ImageName":stats.ImageName if hasattr(stats, 'ImageName') else None,
                }
            empty_keys = [k for k,v in entrydata.items() if not v]
            for k in empty_keys:
                del entrydata[k]
            data['entries'].append(entrydata)
    
    if missing: messagebox.showwarning(title='Warning', message="At least one entry's stats.txt is missing.")
    if invalid: messagebox.showwarning(title='Warning', message="At least one entry's stats.txt was invalid and renamed to stats_INVALID.txt.")
    if not debugmode: print()
    print(f"Total of entries found: {entrycount}.")
    return data

class UX:
    def __init__(self, win, warn):

        def smartDirPath(entry):
            try: path = filedialog.askdirectory(initialdir=entry.get())
            except: path = filedialog.askdirectory()
                
            if not path == '':
                entry.delete(0,customtkinter.END)
                entry.insert(0,path)

        self.frame_1=customtkinter.CTkFrame(master=win)
        self.frame_1.pack(pady=10, padx=10, expand=True, fill="both")
        self.lbl1=customtkinter.CTkButton(self.frame_1, text='Root directory', fg_color="#424242", hover_color="#696969", command=lambda:smartDirPath(self.t1))
        self.t1=customtkinter.CTkEntry(self.frame_1)
        self.b1=customtkinter.CTkButton(self.frame_1, text='Save & Run', command= lambda: run(self.t1.get(),self.swi1.get()))
        #self.b2=customtkinter.CTkButton(self.frame_1, text='Save', command= lambda: settings_save(self.t1.get()))
        #self.lbl2=customtkinter.CTkLabel(self.frame_1, text="Debug\nlevel", anchor="center")
        #self.slider_1=customtkinter.CTkSlider(self.frame_1, from_=0, to=1, number_of_steps=1)
        self.swi1=customtkinter.CTkSwitch(self.frame_1, text="Verbose")
        
        try: self.t1.insert(0,settings.rootdir)
        except: pass

        self.lbl1.place(x=0, y=0)
        self.t1.place(x=140, y=0)
        self.b1.place(x=140/2, y=0+29)
        #self.b2.place(x=140/2, y=0+29+29)
        #self.lbl2.place(x=5, y=-5+29+29)
        #self.slider_1.place(x=140/3, y=0+29+29)
        self.swi1.place(x=5, y=0+29+29)

        if warn:
            self.w1 = messagebox.showwarning(title='Warning', message="Invalid settings file! Renamed to databank_settings_INVALID.txt.")
            warn = False
            win.focus_force()

def main():
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)

    global settings
    warn = False
    try:
        settings = import_path(os.path.join(os.getcwd(), "databank_settings.txt"))
        print("Found settings file.\n")
    except:
        try: os.unlink(os.path.join(os.getcwd(), "databank_settings_INVALID.txt"))
        except: pass
        try: 
            os.rename(os.path.join(os.getcwd(),"databank_settings.txt"), os.path.join(os.getcwd(),"databank_settings_INVALID.txt"))
            warn = True
        except: print("Settings file not found, running anyway.\n")

    root = customtkinter.CTk()
    GUI = UX(root, warn)
    root.title("DatabankJSON")
    root.geometry('300x100')  
    root.mainloop()

def run(rootdir, debugmode=0):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"\n[{dt_string}] Initiating procedure...")
    #
    data = read_entries(rootdir, debugmode=debugmode)
    json = json_dump(data)
    if not len(data['entries']):
        messagebox.showerror(title='Error', message="The directory provided was not valid.")
    else:
        settings_save(rootdir)
        json_export(json)
        messagebox.showinfo(title='Info', message="Success!")

def settings_save(rootdir):
    try:
        with open("databank_settings.txt", "w") as outfile:
            outfile.write(f"rootdir = {repr(rootdir)}")
    except:
        messagebox.showwarning(title='Warning', message="Not enough permissions to save settings.")

if __name__ == "__main__":
    required_modules = [
        #(NAME, LINK, TARGET_VERSION),
        ('customtkinter', ': https://github.com/TomSchimansky/CustomTkinter/tags', '513')
    ]
    import_required_modules(required_modules)
    sys.dont_write_bytecode = True
    customtkinter.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("dark-blue") # Themes: "blue" (standard), "green", "dark-blue"
    main()
else: #so pycharm shuts up
    import customtkinter
