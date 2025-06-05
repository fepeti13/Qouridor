
GameController
-it has a main loop, which in every round is receiving a move
-the move can come from the bot, or from a HUMAN(through the UI)
-after each move, the function which made the move, needs to add the move to the LogicModel and the UIModel

handle_bot_move(Function of GameController):
-the logic controller will return a move, which is 100% valid, so no need to check that again
-we need function which can add a move to the LogicModel and to the UIModel
-both of these functions should be implemented in the respective class(LogicModel or UIModel)

handle_UI_move(Function of GameController):
-the UI will wait for inputs form the user
-the PLAYER move(L-s) are valid, because we get those from the LogicModel
-but when placing walls, we need to check every wall location if it is valid or not
-for that we need to ask the LogicModel
-the UI will let place the wall only if the current location is valid
-so here too, is no need to check that the move was valid or not
-after that we need to implement those changes in the LogicModel and UIModel too

UIModel
-it stores the PyGame objects, their locations and etc.

LogicModel
-it has the game logic
-it stores the state of the board
-it stores game rules

BotEngine(or it can have any other name)
-it can make a move, based on the LogicModel, and return that to the GameRuner

UIController
-it recieves the inputs from the user
-manages UILogic
-based on LogicModel it decides what moves will be correct

GameView
-it renders the UIModel

Constants
-it stores the Hardcode values

CordinateMapper
-it provides functions which can transform cordinates from UIModel to LogicModel and back

