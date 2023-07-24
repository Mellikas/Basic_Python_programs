from Exam_tests_table import engine, Exam_test, Question, Answer, Attempt, Solution, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Session = sessionmaker(bind=engine)
session = Session()

while True:
    choise = int(input(
        "\nChoose: \n1 - create new user \n2 - create new exam test \n3 - attempt of exam test \n4 - exit\n"))

    if choise == 1:  # CREAT NEW USER
        user_name = input("\nChoose your user name:")
        pasword = input("Choose your pasword:")
        user = User(user_name=user_name, pasword=pasword)
        session.add(user)
        session.commit()
        print("\n(Info):user created")

    if choise == 2:  # CREAT NEW EXAM TEST
        print(
            "\n(Info):\n1. First step: creat exam if not allready created. \n2. Second step: creat quesiton if not allready created. \n3. Third step: creat answer.")

        print("\n(Existing exam tests):")
        for x in session.query(Exam_test).all():
            print("(Exam test ID): {} (Exam test name): {}".format(x.id, x.name))
        creat = int(input("\nChoose:\n1 - creat new test\n2 - creat new question\n3 - creat new answer"))

        if creat == 1:  # creat new test
            name = input("\nInsert new exam test name:")
            exam_test = Exam_test(name=name)
            session.add(exam_test)
            session.commit()
            print("\n(Info): exam test created")
        if creat == 2:  # creat new question
            print("\n(Questions allready assigned to tests):")
            for x, y in session.query(Exam_test, Question).filter(Exam_test.id == Question.exam_test_id).all():
                print(
                    "(Exam test ID): {} (Question ID): {} (Question): {}"
                    .format(x.id, y.id, y.question))

            exam_test_id = input("\nInsert existing exam test ID:")
            new_question = input("\nInsert new question:")
            question = Question(question=new_question, exam_test_id=exam_test_id)
            session.add(question)
            session.commit()
            print("\n(Info): question created")
        if creat == 3:  # creat new answer
            print("\n(Answers allready assigned to questions):")
            for x, y in session.query(Question, Answer).filter(Question.id == Answer.question_id).all():
                print(
                    "(Question ID): {} (Question): {} (Answer ID): {} (Answer): {} (Value): {}"
                    .format(x.id, x.question, y.id, y.answer, y.value))

            question_id = input("\nInsert existing question ID:")
            new_answer = input("\nInsert new answer:")
            value = input("\nInsert answer's value:")
            answer = Answer(answer=new_answer, value=value, question_id=question_id)
            session.add(answer)
            session.commit()
            print("\n(Info): question created")

    if choise == 3:  # attempt of exam test
        user_querry = session.query(User.id, User.user_name, User.pasword).all()
        print("\n(Allready created users):")
        for user in user_querry:
            print("User ID:{} User name: {}".format(user.id, user.user_name))

        user_name = input("\nWrite your user name:") # user check
        pasword = input("Write your pasword:")
        correct = False
        for x in user_querry:
            if x.user_name == user_name and x.pasword == pasword:
                correct = True
                print("\n(Existing exam tests):")
                for x in session.query(Exam_test).all():
                    print("(Exam test ID): {} (Exam test name): {}".format(x.id, x.name))

                user_id = session.query(User.id).filter_by(user_name=user_name, pasword=pasword)
                choosed_exam_test_id = input("\nInsert exam test ID to attempt it:")
                attempt = Attempt(user_id=user_id, exam_test_id=choosed_exam_test_id)

                question_query = session.query(Exam_test.id, Question).filter(Exam_test.id == choosed_exam_test_id,
                                                                              Exam_test.id == Question.exam_test_id).all()
                answer_query = session.query(Exam_test.id, Question, Answer).filter(
                    Exam_test.id == choosed_exam_test_id,
                    Exam_test.id == Question.exam_test_id,
                    Question.id == Answer.question_id).all()
                for t, q in question_query:
                    print("Question ID:{} - {}".format(q.id, q.question))
                    for t2, q2, a2 in answer_query:
                        if q2 == q:
                            print("Answer ID:{} - {}".format(a2.id, a2.answer))
                    choosed_answers=[]
                    choosed_answers.append(int(input("\nInsert right answer(s) ID(s) (exp.: 13):")))
                    while True:
                        y_n = input("\nAre there any more corect answer (y/n):\n")
                        if y_n == "y":
                            choosed_answers.append(int(input("\nInsert right answer(s) ID(s) (exp.: 13):")))
                        else:
                            break
                    for answer_id in choosed_answers:
                        new_answer = Solution(answer_id=answer_id, question_id=q.id)
                        attempt.solutions.append(new_answer)
                        session.add(attempt)
                        session.commit()
                new_attempt = session.query(func.max(Attempt.id)).filter(Attempt.id)
                max_available_result_query = session.query(Answer.value).filter(Exam_test.id == choosed_exam_test_id,
                                                                                Exam_test.id == Question.exam_test_id,
                                                                                Question.id == Answer.question_id).all()

                max_available_result = 0
                for value in max_available_result_query:
                    max_available_result += value.value

                results = session.query(Answer.value).filter(Attempt.id == Solution.attempt_id,
                                                             Answer.id == Solution.answer_id,
                                                             Attempt.id == new_attempt).all()

                test_result = 0
                for ans in results:
                    test_result += ans.value

                print(f"\n(Result):")
                print(f"Collected {float(test_result)} from {max_available_result} available points")
                print(f"Answered {float(test_result)} from {int(max_available_result)} available questions")
                break
        if correct == False:
            print("\n(Info): Incorect user or pasword")

    if choise == 4:
        exit()
