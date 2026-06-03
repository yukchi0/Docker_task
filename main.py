from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(title="수강기록 API")

DATA_FILE = "courses.json"


def load_courses():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_courses(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


@app.get("/courses")
def get_courses():
    courses = load_courses()
    return courses


@app.post("/courses", status_code=201)
def add_course(course: Course):
    try:
        courses = load_courses()
        courses.append(course.model_dump())
        save_courses(courses)
        return {"message": "과목이 추가되었습니다.", "course": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
