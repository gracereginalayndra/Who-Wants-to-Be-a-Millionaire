import math
import pygame
from abc import ABC, abstractmethod
from widgets import RadioButton
from game import Game, GameQuestion, UsedLifelineError

"""
In this module, we are trying to separate different screens
into different classes to ease the tracking of errors as well as the flow of the game. 
"""

class Resource:
    """
    Contains all the resources such as screen width, screen height,
    background music, clock, sound effects, fonts, and buttons.
    This is to ease the usage throughout all the functions and modules in the future. 
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("sound\obgm.mp3") 
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([width, height])
        self.notif = pygame.mixer.Sound("sound\obuttonclick.mp3")
        self.clap = "sound\clapping.mp3"
        self.youlose = "sound\youlost.mp3"
        self.font = pygame.font.Font("Font\ofont.ttf", 50)
        self.font50 = pygame.font.Font("Font\ofont.ttf", 25)
        self.font_gk = pygame.font.Font("Font\ofont.ttf", 15)
        self.font_question = pygame.font.SysFont(None, 50)
        self.font_timer = pygame.font.Font("Font\ofont.ttf", 20)
        self.callafriend = pygame.image.load("images\jpgePhone.jpg").convert_alpha()
        self.callafriend_rect = pygame.rect.Rect((width - self.callafriend.get_width()) / 2, 100, self.callafriend.get_width(), self.callafriend.get_height())
        self.eliminate50 = pygame.image.load("images\jpge50.jpg").convert_alpha()
        self.eliminate50_rect = pygame.rect.Rect(((width - self.callafriend.get_width()) / 2) - self.eliminate50.get_width() - 50, 100, self.eliminate50.get_width(), self.eliminate50.get_height())
        self.asktheaudience = pygame.image.load("images\jpgePeople.jpg").convert_alpha()
        self.asktheaudience_rect = pygame.rect.Rect(((width - self.callafriend.get_width()) / 2) + self.asktheaudience.get_width() + 50, 100, self.asktheaudience.get_width(), self.asktheaudience.get_height())

    def __enter__(self):
        """ This function is to enter the main game and utilizing the resources"""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """ This function is to exit the main game"""
        pygame.mixer.quit()
        pygame.quit()

    def use_callafriend(self):
        """ This function is to initialize the lifeline call a friend"""
        self.callafriend = pygame.image.load("images\jpgePhoneX.jpg").convert_alpha()

    def use_eliminate50(self):
        """ This function is to initialize the lifeline fifty-fifty"""
        self.eliminate50 = pygame.image.load("images\jpge50X.jpg").convert_alpha()

    def use_asktheaudience(self):
        """ This function is to initialize the lifeline ask the audience"""
        self.asktheaudience = pygame.image.load("images\jpgePeopleX.jpg").convert_alpha()

class MultilineText:
    """
    This class functions to regulate the display of the questions into multiple
    lines in case the length of the sentence or question is longer than the
    width of the screen. Adjusting the proper amount of spacing and new lines so
    that even the long questions are readable to the player.
    """
    def __init__(
            self,
            resources: Resource,
            text: str,
            ypos: int,
            spacing: int,
            font: pygame.font.Font = None,
            antialias = True,
            color = (255, 255, 255)):
        self.resources = resources
        self.text = text
        if font is None:
            self.font = resources.font_question
        else:
            self.font = font
        self.antialias = antialias
        self.color = color
        self.ypos = ypos
        self.spacing = spacing

    def __split(self, width: int):
        """
        This function is to split the lines when the width of the lines
        are longer than the width of the screen.
        It uses loops and checking to get the divisions and segments.
        It also utilizes math.ceil by importing the math module
        """
        divisions = math.ceil(width / (self.resources.width - 50))
        splits = self.text.split()
        segments = ["" for _ in range(divisions)]
        space_width = self.font.render(" ", self.antialias, self.color).get_width()
        dash_width = self.font.render("-", self.antialias, self.color).get_width()
        lens = [self.font.render(segment, self.antialias, self.color).get_width() for segment in splits]
        line_width = width // divisions
        idx = 0
        for segment in range(divisions):
            width = line_width
            while width > 50 and idx < len(splits):
                if lens[idx] + dash_width + space_width > width:
                    if len(segments[segment]) != 0:
                        segments[segment] += " "
                    cutoff = (width * len(splits[idx])) // lens[idx]
                    segments[segment] += splits[idx][0:cutoff]
                    if segment != divisions - 1:
                        segments[segment] += "-"
                    splits[idx] = splits[idx][cutoff:]
                    lens[idx] = self.font.render(splits[idx], self.antialias, self.color).get_width()
                    break
                else:
                    if len(segments[segment]) != 0:
                        segments[segment] += " "
                    segments[segment] += splits[idx]
                    width -= lens[idx]
                    idx += 1
        self.text = segments

    def get_height(self) -> int:
        """This function is to get the height of the line after each splitting"""
        if type(self.text) == list:
            return self.font.render(self.text[0], self.antialias, self.color).get_height()
        output = self.font.render(self.text, self.antialias, self.color)
        if output.get_width() > self.resources.width:
            self.__split(output.get_width())
            return self.font.render(self.text[0], self.antialias, self.color).get_height()
        else:
            return output.get_height()

    def __display_multiline(self):
        """
        This function serves as the private function that hides the specific
        details about displaying the multiple lines on the question screen.
        It eases and simplifies the content presented in the display() function as
        it is then called in the display (self) function
        """
        for i, line in enumerate(self.text):
            output = self.font.render(line, self.antialias, self.color)
            rect = ((self.resources.width - output.get_width()) / 2, self.ypos + ((output.get_height() + self.spacing) * i))
            self.resources.screen.blit(output, rect)

    def display(self):
        """
        This function calls the __display_multiline() function, __split(),
        and the get_width() functions as it
        acts as the mother functions which outputs the display onto the screen
        """
        if type(self.text) == list:
            self.__display_multiline()
        else:
            output = self.font.render(self.text, self.antialias, self.color)
            if output.get_width() > self.resources.width:
                self.__split(output.get_width())
                self.__display_multiline()
            else:
                rect = ((self.resources.width - output.get_width()) / 2, self.ypos)
                self.resources.screen.blit(output, rect)

class Screen(ABC):
    """
    This class utilizes the abstract class and abstract method
    to further emphasize on inheritance, polymorphism, abstraction,
    as well as encapsulation.
    """
    resources = None

    def __init__(self, resources: Resource):
        self.resources = resources
    
    @abstractmethod
    def display():
        """ This is the method that will be overwritten by
        different screens in different stages of the game"""
        pass

class IntroScreen(Screen):
    """
    This class inherits from the resource class to utilize the
    initialized fonts, texts, etc. and this class will overwrite the screen class.
    """
    def __init__(self, resource: Resource):
        super().__init__(resource)
        logo = pygame.image.load('images\logo.png').convert_alpha()
        self.logo = pygame.transform.scale(logo, (450, 450))
        self.logo_center = (
            (resource.width - self.logo.get_width()) / 2,
            (resource.height - self.logo.get_height()) / 2 - 85
        )

        start = pygame.image.load('images\start.png').convert_alpha()
        self.start = pygame.transform.scale(start, (150, 150))
        self.start_center = (
            (resource.width - self.start.get_width()) / 2,
            (resource.height - self.start.get_height()) / 2 + 250
        )
        self.start_rect = pygame.Rect(self.start_center[0], self.start_center[1], self.start.get_width(), self.start.get_height())

    def display(self) -> bool:
        """
        This method overrides the parent class,
        screen(ABC)’s display() abstract method
        """
        while True:
            self.resources.clock.tick(60)
            self.resources.screen.fill((224, 170, 62))
            self.resources.screen.blit(self.logo, self.logo_center)
            self.resources.screen.blit(self.start, self.start_center)
            event_list = pygame.event.get()
            pygame.display.flip()
            for event in event_list:
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        mouse_pos = pygame.mouse.get_pos()
                        if self.start_rect.collidepoint(mouse_pos):
                            self.resources.notif.play()
                            return True
                        
class SelectionScreen(Screen):
    """
    This class inherits from the resource class to
    utilize the initialized fonts, texts, etc.
    and this class will overwrite the screen class
    """
    def __init__(self, resource: Resource):
        super().__init__(resource)
        self.subject = None
        self.difficulty = None
        next = pygame.image.load("images\onext.png").convert_alpha()
        self.next = pygame.transform.scale(next, (100, 100))
        self.next_rect = pygame.Rect(resource.width - self.next.get_width() - 30, resource.height - self.next.get_height() - 30, self.next.get_width(), self.next.get_height())
        self.radioButtons1 = [
            RadioButton(50, 150, 200, 60, resource.font_gk, "General Knowledge"),
            RadioButton(377, 150, 200, 60, resource.font50, "Maths"),
            RadioButton(704, 150, 200, 60, resource.font50, "Sciences"),  
            RadioButton(1030, 150, 200, 60, resource.font50, "Geography")
        ]
        self.radioButtons2 = [
            RadioButton(50, 450, 200, 60, resource.font50, "Easy"),
            RadioButton(resource.screen.get_rect().centerx - 100, 450, 200, 60, resource.font50, "Medium"),
            RadioButton(1030, 450, 200, 60, resource.font50, "Hard")
        ]
        for rb in self.radioButtons1:
            rb.setRadioButtons(self.radioButtons1)
        self.radioButtons1[0].clicked = True

        for rb in self.radioButtons2:
            rb.setRadioButtons(self.radioButtons2)
        self.radioButtons2[0].clicked = True
        self.group1 = pygame.sprite.Group(self.radioButtons1)
        self.group2 = pygame.sprite.Group(self.radioButtons2)
    
    def display(self) -> bool:
        """
        This method overrides the parent class,
        screen(ABC)’s display() abstract method
        """
        while True:
            self.resources.clock.tick(60)
            event_list = pygame.event.get()
            self.resources.screen.fill((224, 170, 62))
            text1 = self.resources.font.render("Choose your topic:", True, (255, 255, 255))
            text2 = self.resources.font.render("Choose the level of difficulty:", True, (255, 255, 255))
            text1_rect = (50, 50)
            text2_rect = (50, 325)
            self.resources.screen.blit(text1, text1_rect)
            self.resources.screen.blit(text2, text2_rect)
            self.resources.screen.blit(self.next, self.next_rect)
            self.group1.update(event_list)
            self.group2.update(event_list)
            # Draw the button surface and text on the screen
            for rb in self.radioButtons1:
                self.resources.screen.blit(rb.image, rb.rect)
            for rb in self.radioButtons2:
                self.resources.screen.blit(rb.image, rb.rect)
            pygame.display.flip()
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        mouse_pos = pygame.mouse.get_pos()
                        if self.next_rect.collidepoint(mouse_pos):
                            self.resources.notif.play()
                            self.subject = [(rb.text) for rb in self.radioButtons1 if rb.clicked][0]
                            self.difficulty = [(rb.text) for rb in self.radioButtons2 if rb.clicked][0]
                            return True
                elif event.type == pygame.QUIT:
                    return False


class QuestionScreen(Screen):
    """
    This class inherits from the resource class to
    utilize the initialized fonts, texts, etc.
    and this class will overwrite the screen class
    """
    def __init__(self, resources: Resource, question: GameQuestion, time: int):
        super().__init__(resources)
        self.question = question
        self.counter = time
        self.timeout = False
        width = (resources.width - 90) / 2
        answers = question.get_answers()
        self.choices = [
            RadioButton(30, self.resources.height - 60 - 200, width, 60, resources.font_question, answers[0]),
            RadioButton(width + 60, self.resources.height - 60 - 200, width, 60, resources.font_question, answers[2]),
            RadioButton(30, self.resources.height - 60 - 100, width, 60, resources.font_question, answers[1]),
            RadioButton(width + 60, self.resources.height - 60 - 100, width, 60, resources.font_question, answers[3])
        ]
        for button in self.choices:
            button.setRadioButtons(self.choices)
        self.choice_group = pygame.sprite.Group(self.choices)
        self.suggested_answer = None
        self.suggested_answer_prompt = None

    def is_timed_out(self):
        """This method checks if the player ran out of time (which was set to 45 seconds per question)"""
        return self.timeout
    
    def __show(self, event_list):
        """
        This is a private method, not accessible to other instances.
        This method shows the process of displaying the question screen.
        This method is later called by the display method in this class
        """
        self.resources.screen.fill((224, 170, 62))
        question = MultilineText(self.resources, self.question.get_question_text(), 200, 20)
        question.display()
        self.resources.screen.blit(self.resources.eliminate50, self.resources.eliminate50_rect)
        #change5050(event_list)
        self.resources.screen.blit(self.resources.callafriend, self.resources.callafriend_rect)
        self.resources.screen.blit(self.resources.asktheaudience, self.resources.asktheaudience_rect)
        text = str(self.counter).rjust(3) if self.counter > 0 else 'Game Over!'
        timer_text = self.resources.font_timer.render(f"Seconds:{text}", True, (255, 255, 255))
        timer_text_rect = ((self.resources.width - timer_text.get_width()) / 2, 20)
        weighting1_text = self.resources.font_timer.render("Weighting:", True, (255, 255, 255))
        weighting1_text_rect = (30, 20)
        self.resources.screen.blit(weighting1_text, weighting1_text_rect)
        Totalscore_text = self.resources.font_timer.render("Total Score:", True, (255, 255, 255))
        Totalscore_text_rect = ((self.resources.width - Totalscore_text.get_width()) -30, 20)
        self.resources.screen.blit(Totalscore_text, Totalscore_text_rect)
        self.resources.screen.blit(timer_text, timer_text_rect)
        weighting_text = self.resources.font_timer.render(f"{self.question.get_weighting():,}", True, (255, 255, 255))
        self.resources.screen.blit(weighting_text, (30, 40))
        score_text = self.resources.font_timer.render(f"{self.question.get_score():,}", True, (255, 255, 255))
        self.resources.screen.blit(score_text, (self.resources.width - score_text.get_width() - 30, 40))
        for rb in self.choices:
            self.resources.screen.blit(rb.image, rb.rect)
        self.choice_group.update(event_list)
        if self.suggested_answer is not None:
            answer_text = self.resources.font_question.render(f"{self.suggested_answer_prompt} \"{self.suggested_answer}\".", True, (255, 255, 255))
            answer_rect = ((self.resources.width - answer_text.get_width()) / 2, self.resources.height - answer_text.get_height() - 30)
            self.resources.screen.blit(answer_text, answer_rect)
        pygame.display.flip()

    def display(self) -> bool:
        """
        Display method will call the __show method
        to ease the displaying and overriding of the Screen class.
        """
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.__show([])

        while self.counter != 0:
            self.resources.clock.tick(60)
            event_list = pygame.event.get()
            self.__show(event_list)
            for event in event_list:
                if event.type == pygame.USEREVENT:
                    self.counter -= 1
                    self.__show(event_list)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.resources.callafriend_rect.collidepoint(mouse_pos):
                            self.resources.notif.play()
                            self.resources.use_callafriend()
                            try:
                                self.suggested_answer = self.question.use_lifeline("Phone a Friend")
                                self.suggested_answer_prompt = "Your friend answered"
                            except UsedLifelineError:
                                continue
                        elif self.resources.asktheaudience_rect.collidepoint(mouse_pos):
                            self.resources.notif.play()
                            self.resources.use_asktheaudience()
                            try:
                                self.suggested_answer = self.question.use_lifeline("Ask the Audience")
                                self.suggested_answer_prompt = "The audience answered"
                            except UsedLifelineError:
                                continue
                        elif self.resources.eliminate50_rect.collidepoint(mouse_pos):
                            self.resources.notif.play()
                            self.resources.use_eliminate50()
                            self.question.use_lifeline("Fifty-Fifty")
                            width = (self.resources.width - 90) / 2
                            answers = self.question.get_answers()
                            self.choices = [RadioButton(width + 60 if i > 1 else 30, self.resources.height - 60 - (100 if i % 2 else 200), width, 60, self.resources.font_question, answer) for i, answer in enumerate(answers) if answer is not None]
                            for button in self.choices:
                                button.setRadioButtons(self.choices)
                            self.choice_group = pygame.sprite.Group(self.choices)
                        else:
                            self.choice_group.update(event_list)
                            choice = [rb.text for rb in self.choices if rb.clicked]
                            if len(choice) != 0:
                                self.answer = choice[0]
                                return True
                    self.__show(event_list)
                elif event.type == pygame.QUIT:
                    return False
        self.timeout = True
        return False
    
class MessageScreen(Screen):
    """
    This class inherits from the resource class to
    utilize the initialized fonts, texts, etc.
    and this class will overwrite the screen class. 
    """
    def __init__(self, resources: Resource, text: str):
        super().__init__(resources)
        self.text = text

    def display(self) -> bool:
        """
        This method is to format the message display of the screen (including padding and line separations)
        """
        while True:
            self.resources.clock.tick(60)
            self.resources.screen.fill((224, 170, 62))
            lines = self.text.split("\n")
            lines_output = [self.resources.font.render(line, True, (255, 255, 255)) for line in lines]
            line_height = lines_output[0].get_height() + 10
            first_y = (self.resources.height - (len(lines) * lines_output[0].get_height()) - ((len(lines) - 1) * 10)) / 2
            lines_rect = [((self.resources.width - line.get_width()) / 2, first_y + (line_height * i)) for i, line in enumerate(lines_output)]
            for out, rect in zip(lines_output, lines_rect):
                self.resources.screen.blit(out, rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

class WinMessageScreen(MessageScreen):
    """
    This class overrides the MessageScreen class to display the congratulatory message if the user wins
    """
    def __init__(self, resources: Resource):
        super().__init__(resources, "Congratulations!\nYou win!\nA millionaire is found")
        
    def display(self):
        """
        This method is to format the message display of the screen (including padding and line separations)
        """
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self.resources.clap)
        pygame.mixer.music.play()
        super().display()

class LoseMessageScreen(MessageScreen):
    """
    This class overrides the MessageScreen class to display the congratulatory message if the user loses
    """
    def __init__(self, resources: Resource, game: Game):
        super().__init__(resources, f"Game Over!\nSomeone's not getting\na million dollars today\nYour Final Score: {game.score:,}")

    def display(self):
        """
        This method is to format the message display of the screen (including padding and line separations)
        """
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self.resources.youlose)
        pygame.mixer.music.play()
        super().display()