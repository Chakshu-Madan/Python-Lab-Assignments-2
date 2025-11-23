# Mini Project Assignment: Gradebook Analyzer
# Course: Programming for Problem Solving uisng Python
# Title: Analysing and Reporting Student Grades
# By: Chakshu Madan
# Date: 22/11/2025

#--- Project Setup and Initialization ---#
import csv
import os


def display_menu():
    print("\n"+"="*40)
    print(" 📚 GradeBook Analyzer CLI ")
    print("="*40)
    print("1. Manual entry of Student Marks")
    print("2. Load marks from CSV file")
    print("3. Exit Program")
    print("-"*40)
    
def get_manual_marks():
    #Allows user to manually enter student names and marks.
    marks = {}
    print("\n---Manual Data Entry ---")
    while True:
        name = input("Enter student name (or type 'done' to finish): ").strip()
        if name.lower() == "done":
            break
        while True:
            try:
                mark = int(input(f"Enter marks for {name}:"))
                if 0 <=mark <=100:
                    marks[name] = mark
                    break
                else:
                    print("Marks must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter valid marks.")
    if marks:
        print(f"\nSuccessfully stored marks for {len(marks)} student(s).")
    else:
        print("\nNo marks entered.")
        
    return marks

def load_csv_marks():
    # Loads student names and marks frima CSV file.
    marks = {}
    print("\n---CSV Data Import---")
    filename = input("Enter the CSV filename(e.g. student_data.csv):")
    if not os.path.exists(filename):
        print(f"Error:File '{filename}' not found. Please check the path.")
        return marks
    try:
        with open(filename, mode='r',newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row)>=2:
                    name=row[0].strip()
                    try:
                        #Assumes marks is in the second column
                        mark = int(row[1].strip())
                        if 0<=mark <100:
                            marks[name] = mark
                        else:
                            print(f"Warning: Skipping {name}.Mark {mark} is out of range.")
                    except ValueError:
                        print(f"Warning: Skipping {name}.Mark is not a valid number")
    except Exception as e:
        print(f"An unexpected error occurred during file reading:{e}")
        return {}
    if marks:
        print(f"\nSuccessfully loaded marks for {len(marks)} student(s) from {filename}.")
    else:
        print("\nNo valid marks were loaded from the file.")
    return marks

def calculate_average(scores):
    # calculates the mean (average) score.
    if not scores:
        return 0
    return sum(scores)/len(scores)

# Grade Assignment and Distribution
def assign_grades(marks_dict):
    grades = {}
    distribution = {'A':0, 'B':0, 'C':0, 'D':0, 'F':0}
    for name,mark in marks_dict.items():
        if mark >= 90:
            grade='A'
        elif 80 <= mark <= 89:
            grade='B'
        elif 70 <= mark <=79:
            grade= 'C'
        elif 60 <= mark <=69:
            grade='D'
        else: #<60
            grade='F'
        
        grades[name] = grade
        distribution[grade] += 1
    return grades, distribution

def calculate_median(scores):
    # calculates the median (middle) score.
    if not scores:
        return 0
    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    if n%2 == 1:
        return sorted_scores[n//2]
    else:
        mid1 = sorted_scores[n//2-1]
        mid2 = sorted_scores[n//2]
        return (mid1+mid2)/2
    
def find_max_score(scores):
    # Finds the maximum score.
    return max(scores) if scores else 0

def find_min_score(scores):
    # Finds the minimum score.
    return min(scores) if scores else 0
            
def print_statistics(stats):
    # Displays the calculated statistical summary.
    print("\n"+"="*40)
    print(" 📈 STATISTICAL SUMMARY 📉")
    print("-"*40)
    print(f"Total Students: {stats['count']}")
    print(f"Highest Score (Max): {stats['max']:.2f}")
    print(f"Lowest Score (Min): {stats['min']:.2f}")
    print(f"Class Average (Mean): {stats['average']:.2f}")
    print(f"Class Median: {stats['median']:.2f}")
    print("-"*40)

def print_grade_distribution(distribution):
    print("\n" + "="*40)
    print(" 🎓 GRADE DISTRIBUTION")
    print("-"*40)
    for grade, count in distribution.items():
        print(f"Grade {grade}: {count} student(s)")
    print("-"*40)

# Pass/Fail filter with List Comprehension
def filter_pass_fail(marks_dict):
    # Filters students into pass and fail list
    pass_mark = 40
    passed_students = [
        name for name, mark in marks_dict.items() if mark >= pass_mark               
    ]
    failed_students = [
        name for name, mark in marks_dict.items() if mark < pass_mark    
    ]
    return passed_students, failed_students

def print_pass_fail_summary(passed_students, failed_students):
    # Displays the count and names of passing and failing students.
    print("\n" + "="*40)
    print(" ✅ PASS/ ❌ FAIL SUMMARY")
    print("-"*40)
    print(f"Total Passed Students (Score >= 40): {len(passed_students)}")
    if passed_students:
        print(f"Names:{','.join(passed_students)}")
    print(f"\nTotal Failed Students (Score < 40): {len(failed_students)}")
    if failed_students:
        print(f"Names:{','.join(failed_students)}")
    print("-"*40)
    
# Results Table and User Loop
def print_results_table(marks_dict, grades_dict):
    print("\n" + "="*45)
    print(" 📋 FINAL CLASS RESULTS TABLE")
    print("="*45)
    print(f"{'Name':<15}{'Marks':>10}{'Grade':>10}")
    print("-"*45)
    
    for name in marks_dict:
        mark = marks_dict[name]
        grade = grades_dict[name]
        print(f"{name:<15}{mark:>10}{grade:>10}")
        print("-"*45)
        
def run_analysis(marks):
    if not marks:
        print("Analysis cancelled. No student data available.")
        return
    print("\n---Starting GradeBook Analysis---")
    # Extracting scores into a list
    scores = list(marks.values())
    # ---Task 3---
    stats = {
        'count':len(scores),
        'average':calculate_average(scores),
        'median':calculate_median(scores),
        'max':find_max_score(scores),
        'min':find_min_score(scores)
    }
    print_statistics(stats)       # Displays the results

    # ---Task 4---
    grades_dict, distribution = assign_grades(marks)
    print_grade_distribution(distribution)
    
    # ---Task 5---
    passed_students, failed_students = filter_pass_fail(marks)
    print_pass_fail_summary(passed_students, failed_students)
    
    # ---Task 6---
    print_results_table(marks, grades_dict)
    
    return marks, grades_dict
    
def main_cli_loop():
    while True:
        display_menu()
        choice=input("Enter your choice from (1-3): ")
        
        marks = {}
        
        if choice == '1':
            marks = get_manual_marks()
        elif choice == '2':
            marks = load_csv_marks()
        elif choice == '3':
            print("\nExiting GradeBook Analyzer. GoodBye!!")
            break
        else:
            print("Invalid choice. Please enter 1,2 or 3")
            continue
        
        if marks:
            print("\nData loaded successfully!! Proceeding to analysis..")
            run_analysis(marks)
            
if __name__ == "__main__":
    main_cli_loop()
    