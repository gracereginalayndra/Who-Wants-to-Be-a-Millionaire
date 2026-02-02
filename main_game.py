from game import Game
from screens import *
from questions import QuestionGenerator

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 650
def main():
    """
    This method in the main_game module encapsulates all the complexity in the previous modules.
    Combining all the inheritance, abstractions, encapsulations, etc and controling the gameflow.
    """
    with Resource(SCREEN_WIDTH, SCREEN_HEIGHT) as resource:
        game = Game()
        if not IntroScreen(resource).display():
            return
        selection = SelectionScreen(resource)
        if not selection.display():
            return
        question_gen = QuestionGenerator(selection.subject, selection.difficulty, 15)
        game.set_generator(question_gen)
        for question in game:
            question_screen = QuestionScreen(resource, question, 45)
            if not question_screen.display():
                if question_screen.is_timed_out():
                    LoseMessageScreen(resource, game).display()
                return
            if not question.check_answer(question_screen.answer):
                LoseMessageScreen(resource, game).display()                
                return
        WinMessageScreen(resource).display()

if __name__ == "__main__":
    main()