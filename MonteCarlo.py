"""
Policies
    Policy 1 -> If Hand >=17 Stick, Else Hit
    Policy 2 -> If Hand >=17 and Hard, Stick, else hit unless Hand = 21
    Policy 3 -> Always Stick
    Policy 4 -> 7 Players In A Game
    Policy 5 -> Split If Idential Pair

    Versions
    Version 1 -> Infinite Deck 
    Version 2 -> Single Deck

    Policy 1 will be kept as a standard when using Policy 4 & 5
"""
import random;

Actualcards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];
#        A   2  3  4  5  6  7  8  9  10   J   Q   K
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10];
used = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
infinite = True;
stay17 = True;
cpu6 = True;
pairSplit = False;
winCount = [0,0,0];  # Player, dealer Tie
runCount = 1000000;
extraRun = 0;
checkSoft = False;
isDealer = False;
splitHandActive = False;

# Function To Reset Cards Used For A New Game
def resetGame(hands):
    for hand in hands:
        hand.has = [];
        hand.value = 0;
        hand.bust = False;
        hand.aceCount = 0;

    # Clear the 'used' list
    global used
    used = [0] * len(cards);

def resetWinCount():
    winCount = [0,0,0];

def clearUsed():
    used = [0,0,0,0,0,0,0,0,0,0,0,0,0,0];


class hand():
    def __init__(self):
        self.has = [];
        self.value = 0;
        self.bust = False;
        self.aceCount = 0;
    
    # Function used to add a card to the hand & update the hand value;
    def addToHand(self):
        card = getCard();
        self.has.append(card);
        self.value += cards[card];
        if (card == 0):  # Ace
            self.aceCount += 1

    # Used to add card until 17 then check if bust
    def checkHand(self):
        if(self.value > 21):
            self.bust = True;

    # Used to add card until 17 then check if bust
    def stayAt17(self):
        global isDealer;
        if(isDealer == True):
            while(self.value < 17):
                self.addToHand();
                self.checkHand();
                if self.bust:
                    if self.aceCount > 0:
                        self.value -= 10;
                        self.aceCount -= 1;
                        self.bust = False;
                self.checkHand();

        else:
            while(self.value < 17 or (self.value != 21 and self.aceCount > 0 and checkSoft == True)):
                self.addToHand();
                self.checkHand();
                if self.bust:
                    if (self.aceCount > 0):
                        self.value -= 10;
                        self.aceCount -= 1;
                        self.bust = False;
            self.checkHand();

#        if(checkSoft == True):
#            if(self.aceCount > 0):
            

# Function To Select Random Card from A-K 0-12
def getCard():
    selectedCard = random.randint(0, 12);

    # Function To Test For V2 Single Deck
    if(not infinite):
        #print("Before Updating Used List: ", used);
        #print("Selected card: ", selectedCard);
        #print("Player Hand is: ", playerHand.has, "and dealer hand it ", dealerHand.has, "\n");
        # If card has been sued 4 times Select New Card
        while(used[selectedCard] >= 4):
            #print(used, selectedCard);
            #print("Card has already been used.");
            #print(playerHand.has, " ", dealerHand.has, "\n\n");

            selectedCard = random.randint(0,12);
        # Add card to used count
        used[selectedCard] += 1;
        #print("After Updating used list: ", used);
    return selectedCard;

def createCPU():
    for x in range(6):
        cpus.append(hand());

# Function to start new hand
def startHand():
    for x in range(2):
        # Function for V4 add new hands
        if(cpu6 == True):
            for cpu in cpus:
                cpu.addToHand();
        # Add To Player & Dealer Hand
        playerHand.addToHand();
        dealerHand.addToHand();
    
    if pairSplit:
        if playerHand.has[0] == playerHand.has[1]:
            card = playerHand.has.pop();
            if(card == 0):
                playerHand.aceCount -= 1;
                splitHand.aceCount += 1;
            splitHand.has.append(card);
            splitHand.value += cards[card];
            playerHand.value -= cards[card];
            # Add Cards To Hand & Activate
            splitHand.addToHand();
            playerHand.addToHand();
            global splitHandActive;
            splitHandActive = True;
            global extraRun;
            extraRun += 1;


# Function To Check Winner
def checkWinner(playerHand, dealerHand):
    if(playerHand.value > 21):
        winCount[1] += 1;
    elif(dealerHand.value > 21):
        winCount[0] += 1;
    elif(playerHand.value > dealerHand.value):
        winCount[0] += 1;
    elif(dealerHand.value == playerHand.value):
        winCount[2] += 1;
    else:
        winCount[1] += 1;


def game():
    # Function to get 2 cards in everyones hand
    startHand();

    # Inser Function To Split If Pair

    # Policy 1 -> Hit on Stay <17 regardles of soft
    if(stay17 == True):
        global isDealer;
        if cpu6:
            for cpu in cpus:
                cpu.stayAt17();
        playerHand.stayAt17();
        global splitHandActive;
        if (splitHandActive == True):
            splitHand.stayAt17();
        isDealer = True;
        dealerHand.stayAt17();
        isDealer = False;


    #if (stay17 == False):
        # Always stick is being used
    else:
        isDealer = True;
        dealerHand.stayAt17();
        isDealer = False;
    

    #FOR TESTING
    # print(playerHand.value, dealerHand.value);
    #if cpu6:
    #    for cpu in cpus:
    #        print("cpu has", cpu.has, cpu.value);
    #if pairSplit:
    #    print("Split has ", splitHand.has, splitHand.value);
    #print("Player has ", playerHand.has, playerHand.value);
    #print("Dealer has ", dealerHand.has, dealerHand.value), "\n\n";

    # Add To Win Count & Reset Cards
    checkWinner(playerHand, dealerHand);
    # Add To Win Count If Hand Was Split
    if splitHandActive:
        checkWinner(splitHand, dealerHand);
    if cpu6:
        resetGame([playerHand, dealerHand] + cpus);
    elif splitHand:
        resetGame([playerHand, dealerHand, splitHand]);
        splitHandActive = False;
    else:
        resetGame([playerHand, dealerHand]);

playerHand = hand();
splitHand = hand();
dealerHand = hand();
cpus = [];
createCPU();




# VERSION 1
    # Policy 1 -> If Hand >=17 Stick, Else Hit
# infinite = True;
# stay17 = True;
# cpu6 = False;
# pairSplit = False;
# checkSoft = False;

# for x in range (runCount):
#    game();

# print("With Policy 1 & Infinite Deck: ");
# print(winCount);
# print("Win rate: ", winCount[0]/runCount)
# resetWinCount();


# # VERSION 1
#     # Policy 2 -> If Hand >=17 and Hard, Stick, else hit unless Hand = 21
# infinite = True;
# stay17 = True;  # LEAVE TRUE, if false does not add cards
# cpu6 = False;
# pairSplit = False;
# checkSoft = True;

# for x in range(runCount):
#     game();

# print("With Policy 2 & Infinite Deck: ");
# print(winCount);
# print("Win rate: ", winCount[0]/runCount)
# resetWinCount();


# VERSION 1
#     # Policy 3 -> Always Stick
# infinite = True;
# stay17 = False;
# cpu6 = False;
# pairSplit = False;
# checkSoft = False;

# for x in range(runCount):
#     game();

# print("With Policy 3 & Infintite Deck: ")
# print(winCount);
# print("Win rate: ", winCount[0]/runCount);
# resetWinCount();


# VERSION 1
    # Policy 4 -> 7 Players In A Game
# infinite = True;
# stay17 = True;
# cpu6 = True;
# pairSplit = False;
# checkSoft = False;

# for x in range(runCount):
#     game();

# print("With Policy 4 & Infinite Deck: ");
# print(winCount);
# print("Win rate: ", winCount[0]/runCount);
# resetWinCount()


# VERSION 1 
    # Policy 5 -> Split If Idential Pair
infinite = True;
stay17 = True;
cpu6 = False;
pairSplit = True;
checkSoft = False;

for x in range(runCount):
    game();

print("With Policy 5 & Infinite Deck: ");
print(winCount);
print("Win Rate: ", winCount[0]/(runCount + extraRun));
print("Tie rate: ", winCount[2]/(runCount+ extraRun));
resetWinCount();
extraRun = 0;


""" VERSION 2 Single Deck 
        STARTS HERE       """
# VERSION 2
    # Policy 1 -> If Hand >=17 Stick, Else Hit
# infinite = False;
# stay17 = True;
# cpu6 = False;
# pairSplit = False;
# checkSoft = False;

# for x in range (runCount):
#     game();

# print("With Policy 1 & Single Deck: ");
# print(winCount);
# print("Win rate: ", winCount[0]/(runCount))
# resetWinCount();


# # VERSION 2
#     # Policy 2 -> If Hand >=17 and Hard, Stick, else hit unless Hand = 21
# infinite = False;
# stay17 = True;  # LEAVE TRUE, if false does not add cards
# cpu6 = False;
# pairSplit = False;
# checkSoft = True;
# for x in range(runCount):
#     game();

# print("With Policy 2 & Infinite Deck: ");
# print(winCount);
# print("Win rate: ", winCount[0]/runCount)
# resetWinCount();


# VERSION 2
    # Policy 3 -> Always Stick
# infinite = False;
# stay17 = False;
# cpu6 = False;
# pairSplit = False;
# checkSoft = False;

# for x in range(runCount):
#     game();

# print("With Policy 3 & Infintite Deck: ")
# print(winCount);
# print("Win rate: ", winCount[0]/runCount);
# resetWinCount();


# VERSION 2
    # Policy 4 -> 7 Players In A Game
# infinite = False;
# stay17 = True;
# cpu6 = True;
# pairSplit = False;
# checkSoft = False;

# for x in range(runCount):
#     game();

# print("With Policy 4 & Infinite Deck: ");
# print(winCount);
# print("Win rate: ", winCount[0]/runCount);
# resetWinCount()


# VERSION 2
    # Policy 5 -> Split If Idential Pair
# infinite = False;
# stay17 = True;
# cpu6 = False;
# pairSplit = True;
# checkSoft = False;

# for x in range(runCount):
#     game();

# print("With Policy 5 & Infinite Deck: ");
# print(winCount);
# print("Win Rate: ", winCount[0]/(runCount + extraRun));
# print("Tie rate: ", winCount[2]/(runCount+ extraRun));
# resetWinCount();
# extraRun = 0;