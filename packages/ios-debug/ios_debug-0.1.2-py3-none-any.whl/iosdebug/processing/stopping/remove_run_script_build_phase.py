from iosdebug.constants import RUN_SCRIPT_PHASE_ID
import re
import os


def remove_run_script_build_phase(path):
    files = os.listdir(path)
    xcodeproj_file_name = [file for file in files if ".xcodeproj" in file][0]
    project_file = path + os.sep + xcodeproj_file_name + os.sep + "project.pbxproj"
    with open(project_file, "r") as file:
        content = file.read()
        content = re.sub(
            ".*" + RUN_SCRIPT_PHASE_ID + " /\* Sync debug mode.+?,\n", "", content
        )
        content = re.sub(RUN_SCRIPT_PHASE_ID + r"[\s\S]+?}(;|,)\n", "", content)

    with open(project_file, "w") as file:
        file.write(content)
