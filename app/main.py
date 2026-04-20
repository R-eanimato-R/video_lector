from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base, Lecture, Teacher, Avatar, Voice, Discipline
from app.schemas import (
    LectureCreate, LectureResponse, LectureUpdate,
    TeacherCreate, TeacherResponse,
    AvatarCreate, AvatarResponse,
    VoiceCreate, VoiceResponse,
    DisciplineCreate, DisciplineResponse
)

# Создаём таблицы при старте (для разработки)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Видео-Лектор API", version="1.0.0", docs_url="/docs")

# ==========================================
# TEACHERS
# ==========================================
@app.post("/teachers/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    teacher_data = teacher.model_dump(exclude={'password'})
    db_teacher = Teacher(**teacher_data, password_hash=teacher.password)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@app.get("/teachers/", response_model=list[TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()

# ==========================================
# AVATARS
# ==========================================
@app.post("/avatars/", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
def create_avatar(avatar: AvatarCreate, db: Session = Depends(get_db)):
    db_avatar = Avatar(**avatar.model_dump())
    db.add(db_avatar)
    db.commit()
    db.refresh(db_avatar)
    return db_avatar

@app.get("/avatars/", response_model=list[AvatarResponse])
def get_avatars(db: Session = Depends(get_db)):
    return db.query(Avatar).all()

# ==========================================
# VOICES
# ==========================================
@app.post("/voices/", response_model=VoiceResponse, status_code=status.HTTP_201_CREATED)
def create_voice(voice: VoiceCreate, db: Session = Depends(get_db)):
    db_voice = Voice(**voice.model_dump())
    db.add(db_voice)
    db.commit()
    db.refresh(db_voice)
    return db_voice

@app.get("/voices/", response_model=list[VoiceResponse])
def get_voices(db: Session = Depends(get_db)):
    return db.query(Voice).all()

# ==========================================
# DISCIPLINES
# ==========================================
@app.post("/disciplines/", response_model=DisciplineResponse, status_code=status.HTTP_201_CREATED)
def create_discipline(discipline: DisciplineCreate, db: Session = Depends(get_db)):
    db_discipline = Discipline(**discipline.model_dump())
    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline

@app.get("/disciplines/", response_model=list[DisciplineResponse])
def get_disciplines(db: Session = Depends(get_db)):
    return db.query(Discipline).all()

# ==========================================
# LECTURES
# ==========================================
@app.post("/lectures/", response_model=LectureResponse, status_code=status.HTTP_201_CREATED)
def create_lecture(lecture: LectureCreate, db: Session = Depends(get_db)):
    new_lecture = Lecture(**lecture.model_dump())
    db.add(new_lecture)
    db.commit()
    db.refresh(new_lecture)
    return new_lecture

@app.get("/lectures/{lecture_id}", response_model=LectureResponse)
def get_lecture(lecture_id: int, db: Session = Depends(get_db)):
    lecture = db.query(Lecture).filter(Lecture.id == lecture_id).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="Лекция не найдена")
    return lecture

@app.get("/lectures/", response_model=list[LectureResponse])
def get_lectures(db: Session = Depends(get_db)):
    return db.query(Lecture).all()