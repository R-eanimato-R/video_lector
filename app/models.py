from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, CheckConstraint, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""
    pass


class Teacher(Base):
    __tablename__ = "teachers"
    __table_args__ = (
        CheckConstraint("char_length(trim(full_name)) > 0", name="chk_teacher_full_name"),
        CheckConstraint("char_length(trim(position)) > 0", name="chk_teacher_position"),
        CheckConstraint("email LIKE '%@%'", name="chk_teacher_email"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    position: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    lectures: Mapped[list["Lecture"]] = relationship(back_populates="teacher", cascade="all, delete-orphan")
    disciplines: Mapped[list["Discipline"]] = relationship(secondary="teacher_disciplines", back_populates="teachers")

class Discipline(Base):
    __tablename__ = "disciplines"
    __table_args__ = (CheckConstraint("char_length(trim(name)) > 0", name="chk_discipline_name"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    teachers: Mapped[list["Teacher"]] = relationship(secondary="teacher_disciplines", back_populates="disciplines")

class TeacherDiscipline(Base):
    __tablename__ = "teacher_disciplines"
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id", ondelete="CASCADE"), primary_key=True)

class Avatar(Base):
    __tablename__ = "avatars"
    __table_args__ = (CheckConstraint("char_length(trim(name)) > 0", name="chk_avatar_name"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    lectures: Mapped[list["Lecture"]] = relationship(back_populates="avatar")

class Voice(Base):
    __tablename__ = "voices"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="chk_voice_name"),
        CheckConstraint("char_length(trim(demo_path)) > 0", name="chk_voice_demo_path"),
        CheckConstraint("char_length(trim(api_code)) > 0", name="chk_voice_api_code"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    demo_path: Mapped[str] = mapped_column(String(255), nullable=False)
    api_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    lectures: Mapped[list["Lecture"]] = relationship(back_populates="voice")

class Lecture(Base):
    __tablename__ = "lectures"
    __table_args__ = (
        CheckConstraint("char_length(trim(title)) > 0", name="chk_lecture_title"),
        CheckConstraint("char_length(trim(source_text)) > 0", name="chk_lecture_source_text"),
        CheckConstraint("status IN ('черновик', 'генерация', 'готово')", name="chk_lecture_status"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    avatar_id: Mapped[int] = mapped_column(ForeignKey("avatars.id", ondelete="RESTRICT"), nullable=False)
    voice_id: Mapped[int] = mapped_column(ForeignKey("voices.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    edited_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    presentation_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'черновик'"))
    teacher: Mapped["Teacher"] = relationship(back_populates="lectures")
    avatar: Mapped["Avatar"] = relationship(back_populates="lectures")
    voice: Mapped["Voice"] = relationship(back_populates="lectures")