from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
import datetime

engine = create_engine('sqlite:///exams.db')
Base = declarative_base()


class Exam_test(Base):
    __tablename__ = "exam_tests"
    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    questions = relationship("Question", back_populates="exam_tests")
    attempts = relationship("Attempt", back_populates="exam_tests")

    # def __init__(self, name=0):
    #     self.name = name


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question = Column("question", String)
    exam_test_id = Column(Integer, ForeignKey("exam_tests.id"))
    exam_tests = relationship("Exam_test", back_populates="questions")
    answers = relationship("Answer", back_populates="questions")
    solutions = relationship("Solution", back_populates="questions")

    # def __init__(self, question=0, exam_test_id=0):
    #     self.question = question
    #     self.exam_test_id = exam_test_id


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    answer = Column("answer", String)
    value = Column("value", Integer)
    question_id = Column(Integer, ForeignKey("questions.id"))
    questions = relationship("Question", back_populates="answers")
    solutions = relationship("Solution", back_populates="answers")

    # def __init__(self, answer=0, value=0, question_id=0):
    #     self.answer = answer
    #     self.value = value
    #     self.question_id = question_id


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column("user_name", String)
    pasword = Column("pasword", String)
    attempts = relationship("Attempt", back_populates="users")

    # def __init__(self, user_name=0, pasword=0):
    #     self.user_name = user_name
    #     self.pasword = pasword


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True)
    date = Column("date", DateTime, default=datetime.datetime.now)
    exam_test_id = Column(Integer, ForeignKey("exam_tests.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_tests = relationship("Exam_test", back_populates="attempts")
    users = relationship("User", back_populates="attempts")
    solutions = relationship("Solution", back_populates="attempts")

    # def __init__(self, exam_test_id=0, user_id=0):
    #     self.exam_test_id = exam_test_id
    #     self.user_id = user_id


class Solution(Base):
    __tablename__ = "solutions"
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey("attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_id = Column(Integer, ForeignKey("answers.id"))
    questions = relationship("Question", back_populates="solutions")
    answers = relationship("Answer", back_populates="solutions")
    attempts = relationship("Attempt", back_populates="solutions")

    # def __init__(self, attempt_id=0, question_id=0, answer_id=0):
    #     # self.attempt_id = attempt_id
    #     self.question_id = question_id
    #     self.answer_id = answer_id


if __name__ == "__main__":
    Base.metadata.create_all(engine)
