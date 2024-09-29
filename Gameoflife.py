# Automate cellulaire "Jeu de la vie" de Conway

import tkinter as tk
# from random import randrange

haut = 90  # hauteur du tableau
larg = 90  # largeur du tableau
cote = 15  # côté d'une cellule
vivant = 1
mort = 0
pause = 1

# Matrix creation
cell = [[0 for row in range(haut)] for col in range(larg)]
etat = [[mort for row in range(haut)] for col in range(larg)]
temp = [[mort for row in range(haut)] for col in range(larg)]

# Compute and draw the next board

def activation():
    boardDraw()
    if pause != 1:
        compute()
    fenetre.after(100, activation)

def pauseResume(event):
    global pause
    pause *= -1

# Données initiales
def init():
    for y in range(haut):
        for x in range(larg):
            etat[x][y] = mort
            temp[x][y] = mort
            cell[x][y] = canvas.create_rectangle((x*cote, y*cote, (x+1)*cote, (y+1)*cote), outline="gray", fill="white")


    # placer au hasard 25% de cellules vivantes
    # for i in range(larg*haut//4):
    #     etat[randrange(larg)][randrange(haut)] = vivant

# Appliquer les 4 règles

def change_color(event):
    # Récupérer l'identifiant de l'objet cliqué
    item = canvas.find_closest(event.x, event.y)[0]
    if etat[(item-1)%larg][(item-1)//larg] == mort:
        etat[(item-1)%larg][(item-1)//larg] = vivant
    else:
        etat[(item-1)%larg][(item-1)//larg] = mort
    boardDraw()

def compute():
    for y in range(haut):
        for x in range(larg):
            nb_neigbour = living_neigbour_count(x,y)
            # Règle 1 - Mort de solitude
            if etat[x][y] == vivant and nb_neigbour < 2:
                temp[x][y] = mort
            # Règle 2 - Toute cellule avec 2 ou 3 voisins survit.
            if etat[x][y] == vivant and (nb_neigbour == 2 or nb_neigbour == 3):
                temp[x][y] = vivant
            # Règle 3 - Mort par asphyxie
            if etat[x][y] == vivant and nb_neigbour > 3:
                temp[x][y] = mort 
            # Règle 4 - Naissance
            if etat[x][y] == mort and nb_neigbour == 3:
                temp[x][y] = vivant
    for y in range(haut):
        for x in range(larg):
            etat[x][y] = temp[x][y]

# Compter les voisins vivants - tableau torique
def living_neigbour_count(a,b):
    nb_neigbour = 0
    if etat[(a-1)%larg][(b+1)%haut] == 1:
        nb_neigbour += 1
    if etat[a][(b+1)%haut] == 1:
        nb_neigbour += 1
    if etat[(a+1)%larg][(b+1)%haut] == 1:
        nb_neigbour += 1
    if etat[(a-1)%larg][b] == 1:
        nb_neigbour += 1
    if etat[(a+1)%larg][b] == 1:
        nb_neigbour += 1
    if etat[(a-1)%larg][(b-1)%haut] == 1:
        nb_neigbour += 1
    if etat[a][(b-1)%haut] == 1:
        nb_neigbour += 1
    if etat[(a+1)%larg][(b-1)%haut] == 1:
        nb_neigbour += 1
    return nb_neigbour

# Dessiner toutes les cellules
def boardDraw():
    for y in range(haut):
        for x in range(larg):
            if etat[x][y]==0:
                if pause == 1:
                    coul = "lightgrey"
                else:
                    coul = "white"
            else:
                if pause == 1:
                    coul = "navy"
                else:
                    coul = "blue"
            canvas.itemconfig(cell[x][y], fill=coul)

# Lancement du programme
fenetre = tk.Tk()
fenetre.title("Le jeu de la vie de Conway")
canvas = tk.Canvas(fenetre, width=cote*larg, height=cote*haut, highlightthickness=0)
canvas.pack()
init()
activation()
canvas.bind("<Button-1>", change_color)
canvas.bind("<Button-3>", pauseResume)
fenetre.mainloop()
