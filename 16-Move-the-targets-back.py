'''
#16 - Move the targets back
Give the user the option to move the targets back to the right by `n` 
with each movement occuring at a cost of `-2` points 
i.e. moving 3 back to the right would be -6
'''
import re
import random
import math

def Main():
    NumbersAllowed = []
    Targets = []
    MaxNumberOfTargets = 20
    MaxTarget = 0
    MaxNumber = 0
    TrainingGame = False
    Choice = input("Enter y to play the training game, anything else to play a random game: ").lower()
    print()
    if Choice == "y":
        MaxNumber = 1000
        MaxTarget = 1000
        TrainingGame = True
        Targets = [-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 43, 23, 119]
    else:
        MaxNumber = 10
        MaxTarget = 50
        Targets = CreateTargets(MaxNumberOfTargets, MaxTarget)        
    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber)
    PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber)
    input()
    
def PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber):
    Score = 0
    GameOver = False
    while not GameOver:
        DisplayState(Targets, NumbersAllowed, Score)
        UserInput = input("Enter an expression or enter n bruh: ")
        print()
        if UserInput == 'n':
            Targets, Score = MoveBack(Targets, Score)
        elif CheckIfUserInputValid(UserInput):
            UserInputInRPN = ConvertToRPN(UserInput)
            if CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
                IsTarget, Score = CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score)
                if IsTarget:
                    NumbersAllowed = RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed)
                    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber)
        Score -= 1
        if Targets[0] != -1:
            GameOver = True
        else:
            Targets = UpdateTargets(Targets, TrainingGame, MaxTarget)        
    print("Game over!")
    DisplayScore(Score)

def MoveBack(Targets, Score):
    
    x = int(input('how many times you wanna shift? : '))
    ShiftTarget(Targets, x)
    Score -= 2*x
    Score += 1
    return Targets, Score
    
def ShiftTarget(Targets, x):
    l = len(Targets)
    print(f'{Targets}')
    for i in range(l-x-1, 0, -1):
        Targets[i+x] = Targets[i]
        print(f'{Targets}')
    
    # -1, -1, -1, 3, 5, 7, 9

    '''
    how many times you wanna shift? : 10
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 43, 23, 119]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 43, 23, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 43, 82, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 140, 82, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 9, 140, 82, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 9, 140, 82, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, -1, 23, 9, 140, 82, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, -1, -1, 23, 9, 140, 82, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, -1, -1, -1, 23, 9, 140, 82, 121]
[-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, -1, -1, -1, -1, 23, 9, 140, 82, 121]
| | | | |23|9|140|82|121|34| | | | |23|9|140|82|121|121|
    
    '''
    

    # TODO or just uhhhhhh chop of the tail(the last element) and uhhhh add in the beginnign '-1'

def CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score):
    UserInputEvaluation = EvaluateRPN(UserInputInRPN)
    UserInputEvaluationIsATarget = False
    if UserInputEvaluation != -1:
        for Count in range(0, len(Targets)):
            if Targets[Count] == UserInputEvaluation:
                Score += 2
                Targets[Count] = -1
                UserInputEvaluationIsATarget = True        
    return UserInputEvaluationIsATarget, Score
    
def RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed):
    UserInputInRPN = ConvertToRPN(UserInput)
    for Item in UserInputInRPN:
        if CheckValidNumber(Item, MaxNumber):
            if int(Item) in NumbersAllowed:
                NumbersAllowed.remove(int(Item))
    return NumbersAllowed

def UpdateTargets(Targets, TrainingGame, MaxTarget):
    for Count in range (0, len(Targets) - 1):
        Targets[Count] = Targets[Count + 1]
    Targets.pop()
    if TrainingGame:
        Targets.append(Targets[-1])
    else:
        Targets.append(GetTarget(MaxTarget))
    return Targets

def CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
    Temp = []
    for Item in NumbersAllowed:
        Temp.append(Item)
    for Item in UserInputInRPN:
        if CheckValidNumber(Item, MaxNumber):
            if int(Item) in Temp:
                Temp.remove(int(Item))
            else:
                return False            
    return True

def CheckValidNumber(Item, MaxNumber):
    if re.search("^[0-9]+$", Item) is not None:
        ItemAsInteger = int(Item)
        if ItemAsInteger > 0 and ItemAsInteger <= MaxNumber:
            return True            
    return False
    
def DisplayState(Targets, NumbersAllowed, Score):
    DisplayTargets(Targets)
    DisplayNumbersAllowed(NumbersAllowed)
    DisplayScore(Score)    

def DisplayScore(Score):
    print("Current score: " + str(Score))
    print()
    print()
    
def DisplayNumbersAllowed(NumbersAllowed):
    print("Numbers available: ", end = '')
    for N in NumbersAllowed:
        print(str(N) + "  ", end = '')
    print()
    print()
    
def DisplayTargets(Targets):
    print("|", end = '')
    for T in Targets:
        if T == -1:
            print(" ", end = '')
        else:
            print(T, end = '')           
        print("|", end = '')
    print()
    print()

def ConvertToRPN(UserInput):
    Position = 0
    Precedence = {"+": 2, "-": 2, "*": 4, "/": 4}
    Operators = []
    Operand, Position = GetNumberFromUserInput(UserInput, Position)
    UserInputInRPN = []
    UserInputInRPN.append(str(Operand))
    Operators.append(UserInput[Position - 1])
    while Position < len(UserInput):
        Operand, Position = GetNumberFromUserInput(UserInput, Position)
        UserInputInRPN.append(str(Operand))
        if Position < len(UserInput):
            CurrentOperator = UserInput[Position - 1]
            while len(Operators) > 0 and Precedence[Operators[-1]] > Precedence[CurrentOperator]:
                UserInputInRPN.append(Operators[-1])
                Operators.pop()                
            if len(Operators) > 0 and Precedence[Operators[-1]] == Precedence[CurrentOperator]:
                UserInputInRPN.append(Operators[-1])
                Operators.pop()    
            Operators.append(CurrentOperator)
        else:
            while len(Operators) > 0:
                UserInputInRPN.append(Operators[-1])
                Operators.pop()
    return UserInputInRPN

def EvaluateRPN(UserInputInRPN):
    S = []
    while len(UserInputInRPN) > 0:
        while UserInputInRPN[0] not in ["+", "-", "*", "/"]:
            S.append(UserInputInRPN[0])
            UserInputInRPN.pop(0)        
        Num2 = float(S[-1])
        S.pop()
        Num1 = float(S[-1])
        S.pop()
        Result = 0.0
        if UserInputInRPN[0] == "+":
            Result = Num1 + Num2
        elif UserInputInRPN[0] == "-":
            Result = Num1 - Num2
        elif UserInputInRPN[0] == "*":
            Result = Num1 * Num2
        elif UserInputInRPN[0] == "/":
            Result = Num1 / Num2
        UserInputInRPN.pop(0)
        S.append(str(Result))       
    if float(S[0]) - math.floor(float(S[0])) == 0.0:
        return math.floor(float(S[0]))
    else:
        return -1

def GetNumberFromUserInput(UserInput, Position):
    Number = ""
    MoreDigits = True
    while MoreDigits:
        if not(re.search("[0-9]", str(UserInput[Position])) is None):
            Number += UserInput[Position]
        else:
            MoreDigits = False            
        Position += 1
        if Position == len(UserInput):
            MoreDigits = False
    if Number == "":
        return -1, Position
    else:
        return int(Number), Position    

def CheckIfUserInputValid(UserInput):
    if re.search("^([0-9]+[\\+\\-\\*\\/])+[0-9]+$", UserInput) is not None:
        return True
    else:
        return False

def GetTarget(MaxTarget):
    return random.randint(1, MaxTarget)
    
def GetNumber(MaxNumber):
    return random.randint(1, MaxNumber)   

def CreateTargets(SizeOfTargets, MaxTarget):
    Targets = []
    for Count in range(1, 6):
        Targets.append(-1)
    for Count in range(1, SizeOfTargets - 4):
        Targets.append(GetTarget(MaxTarget))
    return Targets
    
def FillNumbers(NumbersAllowed, TrainingGame, MaxNumber):
    if TrainingGame:
        return [2, 3, 2, 8, 512]
    else:
        while len(NumbersAllowed) < 5:
            NumbersAllowed.append(GetNumber(MaxNumber))      
        return NumbersAllowed

if __name__ == "__main__":
    Main()