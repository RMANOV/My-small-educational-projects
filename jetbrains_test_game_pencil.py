type: edu
files:
- name: game.py
  visible: true
  text: |-
    print ("How many pencils would you like to use: ")
    pencils = int(input())
    print ("Who will be the first (John, Jack): ")
    names= str(input())
    print(pencils * "|")
    print(names + " is going to be the first")
  learner_created: false
- name: tests.py
  visible: false
  text: |-
    from hstest import *
    import re


    class LastPencilTest(StageTest):
        @dynamic_test()
        def CheckOutput(self):
            main = TestedProgram()
            output = main.start().lower()
            lines = output.strip().split('\n')
            if len(lines) != 1 or "how many pencils" not in output:
                raise WrongAnswer("When the game just started, it should output only one line asking the user about amount "
                                  "of pencils he would like to use with \"How many pencils\" substring")

            output2 = main.execute("1")
            output2 = output2.replace(" ", "")
            pattern = re.compile(".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)")
            if not re.match(pattern, output2):
                raise WrongAnswer("When the user replies with amount of pencils - game should ask who will"
                                  " be the first player ending with \"(\"Name\", \"Name2\")\" substring")
            return CheckResult.correct()

        test_data = [
            [5, 1, [2, 1, 2]],
            [20, 1, [3, 2, 3, 1, 2, 3, 3, 3]],
            [30, 1, [3, 2, 3, 1, 2, 3, 3, 3, 2, 1, 2, 3, 2]],
            [15, 1, [8, 9]],
            [5, 2, [2, 1, 2]],
            [20, 2, [3, 2, 3, 1, 2, 3, 3, 3]],
            [30, 2, [3, 2, 3, 1, 2, 3, 3, 3, 2, 1, 2, 3, 2]],
            [15, 2, [8, 9]]
        ]

        @dynamic_test(data=test_data)
        def CheckGame(self, amount, first, moves):
            main = TestedProgram()
            main.start()
            output2 = main.execute(str(amount))
            output2 = output2.replace(" ", "")

            leftName = output2[output2.rfind('(') + 1:output2.rfind(',')]
            rightName = output2[output2.rfind(',') + 1:output2.rfind(')')]

            prevPlayer = ""
            nextPlayer = ""
            if first == 1:
                prevPlayer = leftName
                nextPlayer = rightName
            else:
                prevPlayer = rightName
                nextPlayer = leftName

            output3 = main.execute(prevPlayer).lower()

            lines = output3.strip().split('\n')
            linesNonEmpty = [s for s in lines if len(s) != 0]

            if len(linesNonEmpty) != 2:
                raise WrongAnswer("When the player provided the game initial conditions"
                                  ", there should be printed exactly 2 non-empty lines")

            checkPencils = [s for s in lines if '|' in s]
            if len(checkPencils) == 0:
                raise WrongAnswer("When the player provided the game initial conditions"
                                  ", there should be printed pencils-line with '|' symbols")
            if len(checkPencils) > 1:
                raise WrongAnswer("When the player provided the game initial conditions"
                                  ", there should be exactly one line in output, that contains '|' symbols")
            if len(list(set(checkPencils[0]))) != 1:
                raise WrongAnswer("The pencils-line should not contain any other symbols except the '|'")

            if len(checkPencils[0]) != int(amount):
                raise WrongAnswer("When the player provided the game correct initial conditions,"
                                  "the pencils-line should contain as much '|' symbols, as there are in initial conditions")

            checkTurn = any((prevPlayer.lower() in s) and ("turn" in s) for s in lines)

            if not checkTurn:
                raise WrongAnswer(f"When the player provided the game initial conditions"
                                  f" there should be a line in output containing \"{prevPlayer}\" and \"turn\""
                                  f" substrings if {prevPlayer} was chosen as the first player")

            onTable = amount

            for i in moves:
                onTable -= i
                output = main.execute(str(i)).lower()
                lines = output.strip().split('\n')
                linesNonEmpty = [s for s in lines if len(s) != 0]

                if onTable <= 0:
                    if len(linesNonEmpty) != 0:
                        raise WrongAnswer("After the last pencil was taken, there should be no output")
                    else:
                        break

                if len(linesNonEmpty) != 2:
                    raise WrongAnswer("When one of the players enters amount of pencils, he wanted to remove"
                                      ", there should be printed exactly 2 non-empty lines")

                checkPencils = [s for s in lines if '|' in s]
                if len(checkPencils) == 0:
                    raise WrongAnswer("When one of the players enters amount of pencils, he wanted to remove"
                                      ", there should be printed pencils-line with '|' symbols")
                if len(checkPencils) > 1:
                    raise WrongAnswer("When one of the players enters amount of pencils, he wanted to remove"
                                      ", there should be exactly one line in output, that contains '|' symbols")
                if len(list(set(checkPencils[0]))) != 1:
                    raise WrongAnswer("The pencils-line should not contain any other symbols except the '|'")

                if len(checkPencils[0]) != onTable:
                    raise WrongAnswer("When one of the players enters amount of pencils, he wanted to remove, "
                                      "the pencils-line should contain as much '|' symbols, as there are pencils left")

                checkTurn = any((nextPlayer.lower() in s) and ("turn" in s) for s in lines)

                if not checkTurn:
                    raise WrongAnswer(f"When {prevPlayer} enters amount of pencils, he wanted to remove"
                                      f" there should be a line in output containing \"{nextPlayer}\" and \"turn\"")
                prevPlayer, nextPlayer = nextPlayer, prevPlayer
            if not main.is_finished():
                raise WrongAnswer("Your program should not request anything, when there are no pencils left")

            return CheckResult.correct()


    if __name__ == '__main__':
        LastPencilTest().run_tests()
  learner_created: false
- name: calculators.py
  visible: true
  learner_created: true
feedback_link: https://hyperskill.org/learn/step/20065#comment
status: Failed
feedback:
  message: |-
    Error in test #1

    Cannot decide which file to run out of the following: "calculators.py", "game.py"
    Write "if __name__ == '__main__'" in one of them to mark it as an entry point.
  time: Sun, 03 Jul 2022 18:28:23 UTC
record: -1
