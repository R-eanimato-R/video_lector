from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# --- TEACHER ---
class TeacherBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=150)
    position: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=5)

class TeacherCreate(TeacherBase):
    password: str = Field(..., min_length=6)

class TeacherResponse(TeacherBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- DISCIPLINE ---
class DisciplineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
class DisciplineCreate(DisciplineBase): ...
class DisciplineResponse(DisciplineBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- AVATAR ---
class AvatarBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    file_path: str = Field(..., min_length=1)
class AvatarCreate(AvatarBase): ...
class AvatarResponse(AvatarBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- VOICE ---
class VoiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    demo_path: str = Field(..., min_length=1)
    api_code: str = Field(..., min_length=1)
class VoiceCreate(VoiceBase): ...
class VoiceResponse(VoiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- LECTURE ---
STATUS_PATTERN = r"^(черновик|генерация|готово)$"
class LectureBase(BaseModel):
    teacher_id: int
    avatar_id: int
    voice_id: int
    title: str = Field(..., min_length=1, max_length=150)
    source_text: str = Field(..., min_length=1)
    edited_text: Optional[str] = None
    presentation_path: Optional[str] = None
    status: str = Field("черновик", pattern=STATUS_PATTERN)

class LectureCreate(LectureBase): ...
class LectureUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    source_text: Optional[str] = Field(None, min_length=1)
    edited_text: Optional[str] = None
    presentation_path: Optional[str] = None
    status: Optional[str] = Field(None, pattern=STATUS_PATTERN)

class LectureResponse(LectureBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)