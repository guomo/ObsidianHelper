/**
 * Javascript functions for scraping course and student specific data forom Canvas Pages.
 * These need to be run from the debugger of the browser in the console.
 */
// Getting the course short title from course landing page

/**
 * Run from home page of a course.
 */
function getCanvCourseID(){
    canvCourseId = _.last(document.URL.split('/'))
}

/**
 * Run from home page of a course.
 */
function getCanvasName() {
    canvCourseNavClass = ("#crumb_course_" + getCanvCourseID())
    return(document.querySelector(canvCourseNavClass + " > a > span").textContent)
}
