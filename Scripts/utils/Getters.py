from Scripts.config import *

def get_detected_paths(detected=None, paths=None):
        
        detected_paths = []
        def find_dict_key(item):
            for key, value in PROGRAMS_PATH_NAMES.items():
                if value == item:
                    return key
            return None

        for item in detected:
            program_key = find_dict_key(item)
            header = f"Program: {item} - Folders: {detected_folders[item]} - Profiles: {detected_profiles[item]}\n--------------------------------------------------\n"
            detected_paths.append(header)

            for path in paths:
                if not program_key:
                    continue

                parts = os.path.normpath(path).split(os.sep)
                if program_key in parts:
                    flag = True
                    if program_key == "Code":
                        for detect in detected:
                            if detect != program_key and detect in parts:
                                flag = False
                    
                    if flag: detected_paths.append(path + "\n")

            detected_paths.append("\n\n")
        
        return detected_paths