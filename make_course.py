'''
    Program     :   make_course.py
    Author      :   Gregory Stone — gregory@petrasoftresearch.com
    Description :   Will create a set of folders and templates for a class with using a default template for an obsidian
                    notebook. Optionally you can specifiy your own templates to use.
'''

import os
# import requests
import re
import argparse
import utils
from pathlib import Path
import json
import chevron
from enum import Enum
import shutil

class TemplateType(Enum):
    WEEKLY_TEMPL = "templates/Weekly_tmpl.md"
    READING_NOTES_TEMPL = "templates/Book Notes.md"
    WRITTEN_ASSIGNMENTS_TEMPL = "templates/Written Assignment.md"


class CourseDetails :
    def __init__(self, id, shortName, courseTitle, profName, meetTimes, zoom, numWeeks):
        """Full constructor for a course.
        Args:
            id (str): Typically section and number of the class, e.g. HIST1A
            shortName (str): A shorter name for long classes, e.g. History
            fullDesc (str): Official course title, e.g. History of the United States from 1600-1820
            profName (str): Professor's name
            meetTimes (str): A string to describe meeting times, e.g. Mondays & Wednesday 8:30AM PST
        """
        self.meetingTimes = meetTimes
        self.courseId = id
        self.courseTitle = courseTitle
        self.professor = profName
        self.shortName = shortName
        self.meetingCnt = numWeeks
        if not zoom:
            self.zoom = "This course either meets in person or there are no virtual meetings."
        else:
            self.zoom = zoom

    def toJSON(self):
        course = {"meetingTimes" : self.meetingTimes, "courseId" : self.courseId, "courseTitle" : self.courseTitle,
        "professor" : self.professor, "shortName" : self.shortName, "zoomLink" : self.zoom}
        return(course)

"""
Generic function to prompt for a destination directory with proper sanity checks and path expension. It will create
the directory if it doesn't already exist by default.
Args:
    prompt (str): Whatever text you want to prompt the user with.
"""
def prompt_dest_dir(prompt):
    p = None

    while not p:
        # Get the directory to store the file in
        working_dir = input(f"\033[1;35;40m{prompt}\033[1;32;40m")
        # on unix systems users can specify their home dir with alias ~, expand if need be; resolve is in case there are symlinks
        p = Path(working_dir).expanduser().resolve() 
        # Check for existance and write permissions 
        if not os.path.exists(p):
            print("That directory does not exist.")
            mkdir = input("\033[1;35;40mWould you like to to create it [y/n]?\033[1;32;40m")
            if mkdir.lower().startswith('y'):
                try:
                    os.makedirs(p)
                except PermissionError as permEx:
                    print("Sorry, You don't have permsisions in one or more of the directories to create that directory. Try Again.")
                    p = None
                except FileExistsError as fileEx:
                    print("Sorry, the path specified is actually an existing file not directory. Try Again.")
                    p = None
            else:
                p = None
        elif os.path.isfile(p):
            print("Sorry, a file already exists with that directory name. Try again.")
            p = None
    return p


def prompt_course_details():
    id = input("\033[1;35;40mAvoiding the use of colons, slashes, and asterisks, what is the id of the course? \033[1;32;40m")
    done = False
    while not done:
        try:
            weeks = input("\033[1;35;40mHow many weeks for the course? \033[1;32;40m")
            weeks = utils.str_as_number(weeks)
            done = True
        except:
            print("\033[1;31;40mYou must enter a valid integer...Try again.\033[1;32;40m ")
    title = input("\033[1;35;40mWhat is the full title of the course, e.g. History of the United States from 1600-1820? \033[1;32;40m")
    name = input("\033[1;35;40mWhat is a short name for the course, e.g. History, Biology, Bible, etc.? \033[1;32;40m")
    prof = input("\033[1;35;40mWhat is Professor's name (with Dr. if applicable)? \033[1;32;40m")
    times = input("\033[1;35;40mTell us the days and times it meets (room is optional): \033[1;32;40m")
    zoom = input("\033[1;35;40mEnter the zoom link (return if none): \033[1;32;40m")

    # Create the class 
    newCourse = CourseDetails(id, name, title, prof, times, zoom, weeks)
    return (newCourse)

def make_dirs(base, course : CourseDetails):
    # Create the root directory for this course
    rootDir = Path(f"{base}{os.sep}{course.courseId}—{course.shortName}").expanduser().resolve()
    if not Path.exists(rootDir):
        os.mkdir(rootDir)
    
    # Create the completed directory
    os.mkdir(rootDir.joinpath("Completed"))

    # Create the upcoming directory (where all the weeks witll go)
    upcomingDir = rootDir.joinpath("Upcoming")
    os.mkdir(upcomingDir)

    # Create the weekly directories
    for i in range(course.meetingCnt):
        weekDir = upcomingDir.joinpath(f"W{i+1}—{course.courseId}")
        os.mkdir(weekDir)
        
        # Create the weekly markdown file for the course
        weekMarkdownFile = weekDir.joinpath(f"{course.courseId}—Assignments_W{i+1}.md")
        populate_template(TemplateType.WEEKLY_TEMPL, weekMarkdownFile, course)
    

def copy_templates(baseDir):
    templates = Path(baseDir).joinpath(f"Templates{os.sep}").expanduser().resolve()
    if not Path.exists(templates):
        os.mkdir(templates)
        shutil.copyfile(Path(TemplateType.READING_NOTES_TEMPL.value), templates.joinpath(TemplateType.READING_NOTES_TEMPL.value.split('/')[-1]))
        shutil.copyfile(Path(TemplateType.WRITTEN_ASSIGNMENTS_TEMPL.value), templates.joinpath(TemplateType.WRITTEN_ASSIGNMENTS_TEMPL.value.split('/')[-1]))
        

def populate_template(template : TemplateType, file, course: CourseDetails):
    
    # Validate the template exists
    if template == TemplateType.WEEKLY_TEMPL:
        templSrc = Path(TemplateType.WEEKLY_TEMPL.value).expanduser().resolve()
    else: # TemplateType.READING_NOTES_TEMPL until there are more
        templSrc = Path("./templates/templates.reading_notes_tmpls.md").expanduser().resolve()

    if not Path.exists(templSrc):
        print(f"unable to locate the template {template}")
        return

    # Render the template and save the results
    try:
        rendered = None
        with open(templSrc, 'r') as f:
            json_course = course.toJSON()
            rendered = chevron.render(f, json_course)
        with open(file, 'w') as f2:
            f2.write(rendered)
        
    except FileNotFoundError as fileEx:
        print("Course directory does not exist")
        print(fileEx.strerror)
        

######## MAIN

if __name__ == "__main__":
    dest_dir = prompt_dest_dir("What directory would you like to put the generated course in (you can move this later)? ")
    course_info = prompt_course_details()
    make_dirs(dest_dir, course_info)
    copy_templates(dest_dir)
