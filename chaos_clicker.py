# Wallem's Funny Jack Garland Simulator

from tkinter import *
import time
from tkinter.font import BOLD
import os

master = Tk()

# The width and height of the window
WIDTH, HEIGHT = 700, 750
# Our currency
punches = 0
# The total amount of punches we've collected
total_punches = 0
# The main loop. Setting to false quits the game.
enable_loop = True
# The tooltip timer. Goes down once per loop. Normal tooltip timer is 125.
tooltips_left = 0
# The list of items available in the shop
shops = []
# Chaos' base max health.
chaos_maxhealth = (1.0 * 10**20)
# Chaos' current health.
chaos_health = chaos_maxhealth
# How much we're going to try and buy from the shop
buyamount = 1
# The timer for deciding if you want to ascend or not.
decide_ascend_timer = 0
# Our ascensions, measured in Memories.
memories = 1
# Punches made throughout your entire playtime. Currently no real use to it.
lifetime_punches = 0
# Are tooltips currently active?
tooltips_active = False
# Is the ascend verifier active?
ascend_button_active = False
# Has the memories count been updated?
memories_updated = False
# Have we loaded chaos' health yet?
chaos_healthbar_loaded = False
# have we set the UI up?
finished_setup = False
# Current hatred level.
hatred = 0
# Total possible hatred, increases with memories
max_hatred = 100

# Updates the UI text with current punches & resets the shop tooltips
def uiPrint():
    global punches
    global chaos_health
    global tooltips_active
    global chaos_healthbar_loaded
    global enable_loop
    global finished_setup
    global hatred
    global memories
    global memories_updated
    
    if not enable_loop:
        return
    
    if not finished_setup:
        updatePPS()
    
    # Punch counter
    visual_punches = "{:.5e}".format(round(punches)) if punches > 9999999 else round(punches)
    punchCounter.config(text = f"Punched {visual_punches} times.")
    
    #Chaos healthbar
    chaos_health = round(chaos_maxhealth - int(total_punches))
    # To save on computing power, only change chaos' HP if it's a value we'd visually see.
    if total_punches >= (10**14) or not chaos_healthbar_loaded:
        if (chaos_health > 0):
            # Turn into scientific notation if it's over 9999
            visual_chaoshp = "{:.3e}".format(chaos_health) if chaos_health > 9999 else chaos_health
            visual_chaosmax = "{:.3e}".format(chaos_maxhealth)
            chaosHealth.config(text = f"Chaos HP: {visual_chaoshp} / {visual_chaosmax}")
        else:
            chaosHealth.config(text = f"You beat Chaos' corpse {-chaos_health} times.")
            display_ascension_button()
        
        if not chaos_healthbar_loaded:
            chaos_healthbar_loaded = True
    
    hatredLabel.config(text = f"Hatred: {round(hatred)}")
    
    # Handles showing current amount of items
    for item in shops:
        if(item.label_set == False):
            amount_owned = item.levels if item.ignore_first == False else (item.levels - 1)
            display_cost = "{:.5e}".format(item.cost) if item.cost > 9999999 else item.cost
            display_amount = "{:.2e}".format(amount_owned) if amount_owned > 9999999 else amount_owned
            item.shoplabel.config(text = f"Buying {item.name} costs {display_cost} punches! Owned: {display_amount}")
        if(item.current_tooltip > 0):
            item.current_tooltip -= 1
        else:
            item.label.config(text = item.desc)
    
    if(memories >= 2) and not memories_updated:
        imgMemories.config(text=f"You've recovered {memories - 1} memories.",fg="#494893")
        memories_updated = True
    
    if(tooltips_left <= 0) and tooltips_active:
        loadtip.config(text = "??", fg="#1e1e1e")
        tooltips_active = False

def display_ascension_button():
    global ascend_button_active
    global decide_ascend_timer
    if(decide_ascend_timer <= 0) and ascend_button_active:
                ascendButton.config(text="Ascend", bg="#494893", activebackground="#6665b0")
                ascend_button_active = False

def updatePPS():
    visual_ppc = "{:.3e}".format(calc_button_punches()) if calc_button_punches() > 9999 else round(calc_button_punches())
    visual_pps = "{:.3e}".format(calc_auto_punch(1)) if calc_auto_punch(1) > 9999 else round(calc_auto_punch(1))
    ppcLabel.config(text=f"PPC: {visual_ppc} | PPS: {visual_pps}")

# Shop actions
def purchaseCutsceneSkipper():
    cutscenes.PurchaseItem()

def purchaseLimpBizkit():
    albums.PurchaseItem()
    
def purchaseFucksReducer():
    fucks_not_given.PurchaseItem()

def purchaseKnucklesStronger():
    knuckles.PurchaseItem()

def purchaseiPhone():
    iphone.PurchaseItem()

def purchaseSidekicks():
    ash_n_jed.PurchaseItem()

def purchaseCrystal():
    crystals.PurchaseItem()

# Toggle the multibuy function
def toggleMultibuy():
    global buyamount
    if buyamount == 1:
        buyamount = 10
        multibuy.config(text="Buy 10")
    elif buyamount == 10:
        buyamount = 100
        multibuy.config(text="Buy 100")
    elif buyamount == 100:
        buyamount = 1000
        multibuy.config(text="Buy 1000")
    elif buyamount == 1000:
        buyamount = 9999
        multibuy.config(text="Buy Max")
    elif buyamount == 9999:
        buyamount = 1
        multibuy.config(text="Buy 1")

# Punch chaos!!!  
def calc_button_punches():
    global enable_loop
    
    if not enable_loop:
        return
    return (1 + knuckles.levels) * cutscenes.levels

# Punch chaos AUTOMATICALLY.
def calc_auto_punch(time_dialation):
    global enable_loop
    
    if not enable_loop:
        return
    return ((albums.levels * (0.25 + (iphone.levels * 0.25))) * fucks_not_given.levels) * time_dialation

# Button to punch chaos.
def player_punch_command():
    global punches
    global cutscenes
    global total_punches
    global lifetime_punches
    global hatred
    global memories
    global max_hatred
    # Hatred increases punches gained by 1% per point
    manual_punches = (calc_button_punches() * memories) * (1 + (hatred/100))
    punches += manual_punches
    total_punches += manual_punches
    lifetime_punches += manual_punches
    # Increase our hatred
    if(hatred < max_hatred):
        hatred += 3.5
    
# Ends the game and prints your current punches
def endGame():
    global enable_loop
    global punches
    global lifetime_punches
    enable_loop = False
#    print(f"You've ended the game with {round(lifetime_punches)} total punches!")

# Attempt to ascend
def ascendAttempt():
    global decide_ascend_timer
    global chaos_maxhealth
    global chaos_health
    global memories
    global ascend_button_active
    global memories_updated
    global max_hatred
    
    if chaos_health >=1:
        return
    if(decide_ascend_timer >= 1):
        ResetValues()
        chaos_maxhealth *= (memories + 0.5)
        chaos_health = chaos_maxhealth
        memories += crystals.levels
        ascendButton.config(text="Ascend")
        max_hatred = (100 * memories) * 0.75
        ascend_button_active = False
        memories_updated = False
        return
    else:
        ascendButton.config(text="Are you sure?")
        decide_ascend_timer = 100
        ascend_button_active = True
        return
        

# Reset all values to initial ones
def ResetValues():
    global punches
    global total_punches
    global tooltips_left
    global tooltips_active
    global chaos_healthbar_loaded
    
    total_punches = 0
    punches = 0
    tooltips_left = 2
    tooltips_active = True
    chaos_healthbar_loaded = False
    for item in shops:
        if not item.ascension_proof:
            item.cost = item.initial_cost
            item.levels = item.initial_levels
            item.button.config(text = item.init_button_name, bg = item.init_button_bg)
            item.label_set = False
    
# Save the game using a save file
def saveGame():
    global total_punches
    global punches
    global chaos_maxhealth
    global memories
    global lifetime_punches
    with open('chaos_savefile.txt', 'w') as file:
        file.write(f"{round(total_punches)}" + "\n")
        file.write(f"{round(punches)}" + "\n")
        file.write(f"{round(chaos_maxhealth)}" + "\n")
        file.write(f"{round(memories)}" + "\n")
        file.write(f"{round(lifetime_punches)}" + "\n")
        for item in shops:
            file.write(f"{item.name},{item.levels}" + "\n")

# Load the game from a save file
def loadGame():
    global total_punches
    global punches
    global chaos_maxhealth
    global memories
    global lifetime_punches
    global memories_updated
    global tooltips_left
    global max_hatred
    
    if(os.path.exists('chaos_savefile.txt')):
        with open('chaos_savefile.txt', 'r') as file:
            # Split the save data into lines
            total_save_data = file.read().splitlines()
            # Line one is total punches this ascension, used to calculate damage done to chaos
            total_punches = int(total_save_data[0])
            # Line two is our punches, as in currency
            punches = int(total_save_data[1])
            # Line three is chaos' maximum health
            chaos_maxhealth = int(total_save_data[2])
            # Line four is our current number of memories
            memories = int(total_save_data[3])
            # Line five is the total amount of punches we've done throughout our entire game
            lifetime_punches = int(total_save_data[4])
            for line in total_save_data:
                if "," in line:
                    # Split into name and number
                    my_data = line.split(",")
                    for item in shops:
                        # If the name of a shop item matches the name of the data
                        if item.name == my_data[0]:
                            # If the amount of items in the file is more than 0
                            if int(my_data[1]) != 0:
                                # Increase the cost of each item
                                item.cost = item.initial_cost
                                for i in range(int(my_data[1])):
                                    item.cost = round(item.cost * 1.2)
                            item.levels = int(my_data[1])
            # Show ascensions button if already used
            if memories >= 2:
                max_hatred = (100 * memories) * 0.75
                memories_updated = False
                ascendButton.config(text="Ascend", bg="#494893", activebackground="#6665b0")
                         
    else:
        loadtip.config(text = "Place the savefile in the same folder as the .exe!", fg = "white")
        tooltips_left = 125

def auto_punch_calculation(delta_time):
    global punches
    global total_punches
    global lifetime_punches
    
    auto_punch_increase = 0
    if(albums.levels >= 1):
        auto_punch_increase += calc_auto_punch(delta_time) * (1 + (hatred/100))
    if(ash_n_jed.levels > 0):
        auto_punch_increase += (calc_button_punches() * delta_time) * (1 + (hatred/100))
    punches += auto_punch_increase
    total_punches += auto_punch_increase
    lifetime_punches += auto_punch_increase

# Builds the visuals

boldfont = 3
# C H A O S
chaosHealth = Label(master, text = f"Loading!", font=("Franklin Gothic Medium", 30, BOLD), fg="red", bg="#1e1e1e")
chaosHealth.pack()

# Chaos Puncher
punchCounter = Label(master, text = f"Loading!", font=("Franklin Gothic Medium", 25, BOLD), fg="red", bg="#1e1e1e")
punchCounter.pack()

ppcLabel = Label(master, text = "Loading!", fg="red", bg="#1e1e1e")
ppcLabel.pack()

mainClickButton = Button(master, text="Punch Chaos!", command = player_punch_command, bg = "#7c1e1e", font=(15), fg="white", activebackground="#a93131", activeforeground="white")
mainClickButton.pack()

# Stronger Knuckles
shopKnuckles = Label(master, text = f"Loading!", font=(boldfont), fg="white", bg="#1e1e1e")
shopKnuckles.pack()

descKnuckles = Label(master, text = "Increases manual punching power by 1", fg="white", bg="#1e1e1e")
descKnuckles.pack()

purchaseKnuckles = Button(master, text="Purchase Stronger Knuckles", command = purchaseKnucklesStronger, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
purchaseKnuckles.pack()

# Limp Bizkit Albums
shopAlbum = Label(master, text = f"Loading!", font=(boldfont), fg="white", bg="#1e1e1e")
shopAlbum.pack()

descAlbum = Label(master, text = "Automatic 0.25 punches every second.", fg="white", bg="#1e1e1e")
descAlbum.pack()

purchaseAlbumButton = Button(master, text="Purchase Limp Bizkit Album", command = purchaseLimpBizkit, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
purchaseAlbumButton.pack()

# iPhones
shopPhone = Label(master, text = f"Loading!", font=(boldfont), fg="white", bg="#1e1e1e")
shopPhone.pack()

descPhone = Label(master, text = "Increase album punching power by 0.25.", fg="white", bg="#1e1e1e")
descPhone.pack()

purchasePhone = Button(master, text="Purchase iPhone", command = purchaseiPhone, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
purchasePhone.pack()

# Cutscene Skipper
shopSkipper = Label(master, text = f"Loading!", font=(boldfont), fg="white", bg="#1e1e1e")
shopSkipper.pack()

descSkipper = Label(master, text = "Doubles manual punching power.", fg="white", bg="#1e1e1e")
descSkipper.pack()

purchaseSkipperButton = Button(master, text="Purchase Cutscene Skipper", command = purchaseCutsceneSkipper, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
purchaseSkipperButton.pack()

# Fucks Reducers
shopFucks = Label(master, text = f"Loading!", font=(boldfont), fg="white", bg="#1e1e1e")
shopFucks.pack()

descFucks = Label(master, text = "Doubles album punching power.", fg="white", bg="#1e1e1e")
descFucks.pack()

purchaseFucks = Button(master, text="Purchase Fucks Reducer", command = purchaseFucksReducer, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
purchaseFucks.pack()

# Ash & Jed
shopSlaves = Label(master, text = f"Loading!", font=(boldfont), fg="white", bg="#1e1e1e")
shopSlaves.pack()

descSlaves = Label(master, text = "One time buy. Automatically manually punches Chaos.", fg="white", bg="#1e1e1e")
descSlaves.pack()

purchaseSlaves = Button(master, text="Hire Ash & Jed", command = purchaseSidekicks, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
purchaseSlaves.pack()

# Crystals
shopJO = Label(master, text = f"Loading!", font=(boldfont), fg="white", bg="#1e1e1e")
shopJO.pack()

descJO = Label(master, text = "Does... something.", fg="white", bg="#1e1e1e")
descJO.pack()

purchaseJO = Button(master, text="Purchase Crystal", command = purchaseCrystal, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
purchaseJO.pack()

# Hatred
hatredLabel = Label(master, text = "Loading!", fg="red", bg="#1e1e1e")
hatredLabel.pack()

# Multibuy
multibuy = Button(master, text="Buy 1", command = toggleMultibuy, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
multibuy.pack(side=LEFT)

# Ascend.
ascendButton = Button(master, text="??????", command = ascendAttempt, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
ascendButton.pack(side=LEFT)

# Memories
imgMemories = Label(master, text = "Something used to go here...", fg="#1e1e1e", bg="#1e1e1e")
imgMemories.pack(side=LEFT)

# End the game
stopGameButton = Button(master, text="End Game", command = endGame, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
stopGameButton.pack(side = RIGHT)

# Load
loadbutton = Button(master, text="Load", command = loadGame, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
loadbutton.pack(side=RIGHT)

# Save
savebutton = Button(master, text="Save", command = saveGame, fg="white", bg="#1e1e1e", activebackground="#3d3c3c", activeforeground="white")
savebutton.pack(side=RIGHT)

# Tip
loadtip = Label(master, text = "?????", fg="#1e1e1e", bg="#1e1e1e")
loadtip.pack(side=RIGHT)

master.title("CHAOS KILLER")
master.geometry("%sx%s+%s+%s" % (WIDTH,HEIGHT,512,512))
master.configure(bg="#1e1e1e")

# The upgrades in the game.
class Upgrade:
    def __init__(self, cost = 0, levels = 0, name = "", label = Label, shoplabel = Label, desc = "", button = Button, levelcap = 0, ascension_proof = False):
        # How much the upgrade costs
        self.cost = cost
        # Amount the upgrade starts with. 1 for things that multiply, 0 for things that don't.
        self.levels = levels
        # The name of the upgrade
        self.name = name
        # The upgrade's description label in the shop.
        self.label = label
        # The upgrade's shop title lable
        self.shoplabel = shoplabel
        # The description label's text
        self.desc = desc
        # The button this upgrade relies on
        self.button = button
        # The level cap. Setting to 0 makes it have no cap.
        self.levelcap = levelcap
        # Survives ascensions
        self.ascension_proof = ascension_proof
        
        # Ignore the first level when displaying owned amounts
        if(levels == 1):
            self.ignore_first = True
        else:
            self.ignore_first = False
        
        # Is our label already set?
        self.label_set = False
        
        # Used for ascending
        self.initial_cost = cost
        self.initial_levels = levels
        self.init_button_name = self.button.cget("text")
        self.init_button_bg = self.button.cget("bg")
        
        # This button's tooltips, lowers every tick
        self.LONG_TOOLTIP = 100
        self.SHORT_TOOLTIP = 50
        self.current_tooltip = 0
        
    
    # Checks if the player has enough punches to buy it. If they do, deduct those punches from their account,
    # increase the levels of the upgrade. Checks buyamount to see if they want to purchase more than one at once.
    def PurchaseItem(self):
        global punches
        global buyamount
        # Check if we wanna buy more than one
        if self.levelcap == 0:
            if buyamount == 10:
                self.PurchaseX(10)
                return
            elif buyamount == 100:
                self.PurchaseX(100)
                return
            elif buyamount == 1000:
                self.PurchaseX(1000)
                return
            elif buyamount == 9999:
                self.PurchaseMax()
                return
        if self.levelcap > 0 and self.levels >= self.levelcap:
            self.Tooltip("Purchase cap reached on this item!", self.LONG_TOOLTIP)
            return
        if punches < self.cost:
            self.Tooltip("Not enough punches!", self.SHORT_TOOLTIP)
        elif punches >= self.cost:
            punches -= self.cost
            self.levels += 1
            self.Tooltip(f"{self.name} Purchased!", self.LONG_TOOLTIP)
            self.cost = round(self.cost * 1.2)
            self.label_set = False
            updatePPS()
            # Show people that this can't be bought anymore
            if self.levelcap > 0 and self.levels >= self.levelcap:
                self.button.config(text="Purchased!", bg="#a93131")
            
    # Change the shop label and set the tooltips timer.
    def Tooltip(self, words, length):
        global tooltips_left
        global tooltips_active
        self.label.config(text = words)
        self.current_tooltip = length
        
    # Purchase X amount of an item.
    def PurchaseX(self, amount_to_buy):
        global punches
        total_cost, exponential_cost = self.cost, self.cost
        for i in range(amount_to_buy):
            exponential_cost *= 1.2
            total_cost += round(exponential_cost)
        if punches < total_cost:
            self.Tooltip("Not enough punches!", self.SHORT_TOOLTIP)
        elif punches >= (self.cost * amount_to_buy):
            punches -= (self.cost * amount_to_buy)
            self.levels += amount_to_buy
            self.Tooltip(f"{amount_to_buy} {self.name} Purchased!", self.LONG_TOOLTIP)
            self.label_set = False
            updatePPS()
            for i in range(amount_to_buy):
                self.cost = round(self.cost * 1.2)
    
    # Purchase as much of an item as possible.
    def PurchaseMax(self):
        global punches
        amount_bought = 0
        if punches < self.cost:
            self.Tooltip("Not enough punches!", self.SHORT_TOOLTIP)
        else:
            while punches >= self.cost:
                self.levels += 1
                punches -= self.cost
                amount_bought +=1
                self.cost = round(self.cost * 1.2)
            self.Tooltip(f"{amount_bought} {self.name} Purchased!", self.LONG_TOOLTIP)
            self.label_set = False
            updatePPS()

# Each upgrade
knuckles = Upgrade(25,0,"Stronger Knuckles", descKnuckles, shopKnuckles, "Increases manual punching power by 1", purchaseKnuckles)
albums = Upgrade(100, 0, "Limp Bizkit Album", descAlbum, shopAlbum, "Automatic 0.25 punches every second.", purchaseAlbumButton)
iphone = Upgrade(500, 0, "iPhone", descPhone, shopPhone, "Increase album punching power by 0.25.", purchasePhone)
cutscenes = Upgrade(1000, 1, "Cutscene Skipper", descSkipper, shopSkipper, "Doubles manual punching power.", purchaseSkipperButton)
fucks_not_given = Upgrade(2500, 1, "Fucks Reducer", descFucks, shopFucks, "Doubles album punching power.", purchaseFucks)
ash_n_jed = Upgrade((2.5 * (10 ** 15)), 0, "Ash and Jed", descSlaves, shopSlaves, "Single Purchase. Hire Ash n' Jed to click your punch button for you every second.", purchaseSlaves, levelcap=1)
crystals = Upgrade((1 * (10 ** 75)), 1, "Crystal", descJO, shopJO, "Does... Something.", purchaseJO, ascension_proof = True)

# Adds upgrades to shop
items = (
    knuckles,
    albums,
    iphone,
    cutscenes,
    fucks_not_given,
    ash_n_jed,
    crystals
)
shops += items

# the main loop, fires every 0.01 seconds, with upgrades firing roughly every second.
def game_main_loop():
    global enable_loop
    global punches
    global tooltips_left
    global total_punches
    global decide_ascend_timer
    global lifetime_punches
    global hatred
    
    before_time = time.time()
    delta_time = 0
    while enable_loop:
        # The seconds that have elapsed since our last loop.
        time_elapsed = time.time() - before_time
        delta_time += time_elapsed
        # Print the UI
        uiPrint()
        # Lower hatred
        if(hatred >= 1):
            hatred -= 1.2
        # Lower tooltip timer
        if(tooltips_left >= 1):
            tooltips_left -= 1
        # Lower the ascend deciding timer
        if(decide_ascend_timer >= 1):
            decide_ascend_timer -= 1
        # Calculate our automatic gains
        if(delta_time >= 1):
            auto_punch_calculation(delta_time)
            delta_time = 0
        master.update_idletasks()
        master.update()
        before_time = time.time()
        time.sleep(0.05)



game_main_loop()