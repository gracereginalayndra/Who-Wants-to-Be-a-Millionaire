**README.md:**

```markdown
# Who Wants to Be a Millionaire – PyGame Quiz Game

A fully-featured Python implementation of the classic TV quiz show "Who Wants to Be a Millionaire" using PyGame and OpenAI's GPT API for dynamic question generation.

## Features
- **Dynamic Question Generation**: Uses Azure ChatGPT API to generate multiple-choice questions based on selected topic and difficulty.
- **Three Difficulty Levels**: Easy (junior high), Medium (senior high), Hard (university level).
- **Classic Lifelines**:
  - 50:50 (removes two incorrect answers)
  - Phone a Friend (reveals suggested answer)
  - Ask the Audience (reveals audience answer)
- **Polished GUI**: Built with PyGame, featuring intuitive screens, buttons, and animations.
- **Sound & Music**: Includes background music, button clicks, win/lose sounds, and applause.
- **Modular OOP Design**: Clean class hierarchy with abstraction, encapsulation, inheritance, and polymorphism.
- **Timer**: 45-second limit per question.

## Project Structure
```
millionaire-pygame-quiz/
├── main_game.py              # Main entry point
├── screens/                  # GUI screen classes
├── questions/                # Question and API handling
├── widgets/                  # UI components (buttons, radio buttons)
├── game/                     # Game logic and lifeline classes
├── resources/                # Images, fonts, sounds
├── requirements.txt          # Python dependencies
├── README.md
└── report/                   # OOP design documentation
```

## Requirements
- Python 3.8+
- PyGame
- OpenAI Python library (for GPT integration)
- Additional packages listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/millionaire-pygame-quiz.git
   cd millionaire-pygame-quiz
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in a `.env` file (see `.env.example`).

## How to Run
```bash
python main_game.py
```
## Game Flow
1. **Start Screen**: Title and start button.
2. **Selection Screen**: Choose topic and difficulty.
3. **Question Screen**: Answer up to 15 timed questions.
4. **Lifelines**: Use each lifeline once per game.
5. **Result Screen**: Win/lose screen with final score.

## OOP Design
The project follows object-oriented principles with classes such as:
- `Screen` (abstract base class)
- `Question` and `QuestionGenerator`
- `Game` and `GameQuestion`
- `Lifeline` and its subclasses (`FiftyFifty`, `PhoneAFriend`, `AskTheAudience`)
- `Resource` and `MultilineText`

## Resources & Credits
- Background music: "Who Wants to Be a Millionaire" theme
- Sound effects from Pixabay and YouTube
- Images and icons sourced from open repositories
- Fonts from DaFont
- UML diagram created with Visual Paradigm

## Notes
- API calls may take time; please be patient after clicking "Next" on the selection screen.
- The game generates up to 15 questions to ensure API stability.
- Easy mode is recommended for reliable question generation.

## Acknowledgments
- Inspired by the TV show "Who Wants to Be a Millionaire"
- OpenAI GPT for question generation
