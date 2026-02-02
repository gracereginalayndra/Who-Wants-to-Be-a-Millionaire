from questions import Question, QuestionGenerator

class UsedLifelineError(Exception):
    """
    This class is to check if the selected lifeline is used
    """
    def __init__(self, name: str):
        self.name = name

class Game:
    """
    This class tracks the current score of the player, then also checks the status of the lifelines
    """
    def __init__(self):
        self.score = 0
        self.generator = None
        self.lifelines = {
            "Phone a Friend": PhoneAFriend(),
            "Fifty-Fifty": FiftyFifty(),
            "Ask the Audience": AskTheAudience()
        }

    def use_lifeline(self, lifeline_name: str, question: Question):
        """
        If a lifeline is used, it is automatically recorded to avoid future usage
        since the lifelines are only available once only
        """
        if lifeline_name in self.lifelines:
            return self.lifelines.pop(lifeline_name).use_lifeline(question)
        else:
            raise UsedLifelineError(lifeline_name)
    
    def set_generator(self, generator: QuestionGenerator):
        """
        Generate next question
        """
        self.generator = generator

    def add_score(self, points):
        """
        Adding the weighting of the question to the player's total score
        """
        self.score += points

    def __iter__(self):
        """
        A function acting as the iterator
        """
        return self
    
    def __next__(self):
        """
        Getting the next question
        """
        return GameQuestion(self, next(self.generator))

class GameQuestion:
    """
    This class includes the small details for the game including, the scoring,
    weighting, lifelines, questions, answers, and even checking the credibility of player's inputted answer
    """
    def __init__(self, game: Game, question: Question):
        self.__game = game
        self.question = question

    def get_score(self):
        return self.__game.score
    
    def get_weighting(self):
        return self.question.weighting

    def use_lifeline(self, name: str):
        return self.__game.use_lifeline(name, self.question)

    def get_question_text(self):
        return self.question.get_question_text()
    
    def get_answers(self):
        return self.question.get_answers()
    
    def check_answer(self, answer):
        correct = self.question.check_answer(answer)
        if correct:
            self.__game.add_score(self.question.weighting)
        return correct

class Lifeline:
    """
    Parent class for the other lifelines (fifty-fifty, phone a friend, ask the audience)
    """
    def use_lifeline(self, question: Question):
        pass

class FiftyFifty(Lifeline):
    """
    Inherits from the lifeline class and can modify
    according to the parameter passed in the lifeline class
    """
    def use_lifeline(self, question: Question):
        question.remove_two_incorrect()

class PhoneAFriend(Lifeline):
    """
    Inherits from the lifeline class and can modify
    according to the parameter passed in the lifeline class
    """
    def use_lifeline(self, question: Question):
        return question.get_correct_answer()

class AskTheAudience(Lifeline):
    """
    Inherits from the lifeline class and can modify
    according to the parameter passed in the lifeline class
    """
    def use_lifeline(self, question: Question):
        return question.get_correct_answer()