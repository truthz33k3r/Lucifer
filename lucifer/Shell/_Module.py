import os
import importlib
from lucifer.Errors import checkErrors
import re


def use_module(self, mod_path: list):
    use_cache = True
    if "-R" in mod_path:
        mod_path.remove("-R")
        use_cache = False
    if self.module_obj is not None:
        self.loaded_modules[self.module] = self.module_obj
    ori_path = mod_path.copy()
    file = mod_path.pop(-1)
    path = "modules"
    for directory in mod_path:
        path += "/" + directory
        if os.path.exists(path):
            if os.path.isdir(path):
                continue
            else:
                print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
                return
        else:
            print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
            return

    if os.path.isfile(path + "/" + file):
        self.module = path + "/" + file
        print(f"Using module: {self.module}")
    elif os.path.isfile(path + "/" + file + ".py"):
        self.module = path + "/" + file + ".py"
        print(f"Using module: {self.module}")
    else:
        print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
        return
    isInCache = self.module in self.loaded_modules.keys()
    if isInCache and use_cache:
        print(f"Loading {self.module} from cache, use -R to override this.")
        self.module_obj = self.loaded_modules.get(self.module)
    else:
        if isInCache:
            print(f"{self.module} in cache, ignoring it...")
        print(f"Loading {self.module} from file.")
        to_import = (self.module.replace("/", ".")
                     if ".py" not in self.module else
                     self.module.replace(".py", "").replace("/", ".")).split(".")
        pkg = to_import.pop(-1)
        to_import = ".".join(to_import)
        imported_module = importlib.import_module(to_import + "." + pkg)
        self.module_obj = imported_module.Module(self.luciferManager, ShellRun=True)
        self.loaded_modules[self.module] = self.module_obj
    if self.auto_vars:
        self.set_vars()
    return


def run_module(self, *args, **kwargs):
    try:
        if self.module_obj is not None:
            self.module_obj.run()
        else:
            print("Please Select A Module First!")
    except Exception as e:
        checkErrors(e)


def describe_module(self, *args, **kwargs):
    try:
        if self.module_obj is not None:
            print(self.module_obj.get_description())
            return
        else:
            print("Please Select A Module First!")
            return
    except Exception as e:
        checkErrors(e)


def set_vars(self, *args, **kwargs):
    try:
        if self.module_obj is not None:
            self.vars.update(self.module_obj.set_vars())
            return
        else:
            print("Please Select A Module First!")
            return
    except Exception as e:
        checkErrors(e)


def use(self, com_args: list):
    if len(com_args) > 1:
        if len(com_args) == 2:
            module_path = re.split(r"\\|/|,", com_args[1].rstrip())
        else:
            com_args.pop(0)
            module_path = re.split(r"\\| |/|,", " ".join(com_args).rstrip())
        if module_path:
            while "" in module_path:
                module_path.remove("")
            self.use_module(module_path)
    else:
        print("Please add valid module path")
    return
