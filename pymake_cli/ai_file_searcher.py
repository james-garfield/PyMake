import os


C_FILE_ENDINGS = [".cpp", ".c", ".cp", ".c++", ".cc", ".h", ".hh", ".hp", ".hpp", ".h++"]


class AiFileSearch:
    """
    Search within your CPP project to generate a list of header and cpp files.
    """
    def __init__(self, entry_point:str):
        # entry_point: where the program starts
        self.entry_point = entry_point
        # All project files with C_FILE_ENDINGS
        self.project_files = set()
        # The CPP files.
        self.cpp_files = set()
        # The header file locations
        self.header_locations = set()
        # Get all the files in the project.
        self.get_all_files_in_project()

    def get_header_locations(self):
        hl = list(self.header_locations)
        hl.reverse()
        return ["/".join(x.replace("\\", "/").split("/")[:-1]) for x in hl]
    
    def get_cpp_files(self):
        cl = list(self.cpp_files)
        cl.reverse()
        return [x.replace("\\", "/") for x in cl]

    def get_all_files_in_project(self):
        # get the directories in our current location
        cwd = os.getcwd()
        for root, dirs, files in os.walk(cwd):
            for file in files:
                # if any file has a C ending, add it to the list.
                for ending in C_FILE_ENDINGS:
                    if file.endswith(ending):
                        self.project_files.add(os.path.join(root, file))
                        break

    def is_valid_include_line(self, include_line: str):
        # in order for a line to be considered a valid include line for parsing it must start with #include and contain a '"'
        return include_line.startswith("#include") and '"' in include_line

    def get_path_to_file(self, file_name):
        # Get the path to a file. <-- ! IT MUST BE CONTAINED WITHIN PROJECT FILES
        for file in self.project_files:
            if file.endswith(file_name):
                return file
        return None
    
    def get_relevant_cpp_file(self, hpp_file : str):
        ending = hpp_file.split(".")[-1]
        for possible_endings in C_FILE_ENDINGS[:4]:
            possible_path = self.get_path_to_file(hpp_file.replace(f".{ending}", possible_endings))
            if possible_path:
                return possible_path
        return None

    def get_inlcude_files_needed_for(self, file_path : str):
        # open and read file
        file = open(file_path, "r")
        lines = file.readlines()
        includes_found = set()

        # check for any line that starts with "#include"
        for line in lines:
            if self.is_valid_include_line(line):
                include_file = self.get_path_to_file(line.split('"')[1])
                if include_file:
                    includes_found.add(include_file)

        file.close()

        if len(includes_found) > 0:
            for include in includes_found:
                # check if already exists
                if include in self.header_locations:
                    continue
                self.header_locations.add(include)
                # check for relevant cpp files
                relevant_cpp_file = self.get_relevant_cpp_file(include)
                if relevant_cpp_file:
                    self.cpp_files.add(relevant_cpp_file)
                    self.get_inlcude_files_needed_for(relevant_cpp_file)
                self.get_inlcude_files_needed_for(include)

    def ai_generate(self):
        # start at entry point
        self.get_inlcude_files_needed_for(self.entry_point)


if __name__ == "__main__":
    ai_file_search = AiFileSearch("example/src/main.cpp")
    ai_file_search.ai_generate()
    print(ai_file_search.get_header_locations())
    print(ai_file_search.cpp_files)
    print(ai_file_search.project_files)