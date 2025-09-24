from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    telegramId: str
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str
    option1: str
    option2: str
    option3: str
    option4: str
    correctAnswer: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True

class TestAnswerBase(BaseModel):
    questionId: int
    userAnswer: int

class TestAnswerCreate(TestAnswerBase):
    testId: int
    isCorrect: bool

class TestAnswer(TestAnswerBase):
    id: int
    testId: int
    isCorrect: bool
    
    class Config:
        from_attributes = True

class TestBase(BaseModel):
    userId: int

class TestCreate(TestBase):
    pass

class Test(TestBase):
    id: int
    startedAt: datetime
    finishedAt: Optional[datetime] = None
    isPassed: Optional[bool] = None
    totalTime: Optional[int] = None
    score: Optional[int] = None
    
    class Config:
        from_attributes = True

class TestResultBase(BaseModel):
    testId: int
    userId: int
    score: int
    totalTime: int
    isPassed: bool

class TestResultCreate(TestResultBase):
    pass

class TestResult(TestResultBase):
    id: int
    createdAt: datetime
    
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    userId: int
    telegramPaymentId: str
    amount: int
    status: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True