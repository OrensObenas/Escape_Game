import tkinter as tk
from tkinter import messagebox
import threading
import time
import pygame

# Initialiser pygame
pygame.mixer.init()

# Charger les musiques
background_music = "music.mp3"  # Musique de fond d'origine
victory_music = "victory.mp3"
minuteur_music = "minuteur.mp3"# Musique pour la victoire
explosion_music = "explosion.mp3"

# Initialiser le nombre de chances
chances_restantes = 3

# Fonction pour démarrer la musique de fond
def jouer_musique(musique):
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=-1)  # "-1" signifie que la musique va se répéter en boucle indéfiniment

# Fonction pour arrêter la musique de fond
def arreter_musique():
    pygame.mixer.music.stop()
# Fonction pour vérifier si le mot saisi correspond au mot caché
def verifier_mot():
    global chances_restantes
    global countdown_active
    mot_saisi = entry_mot.get().lower()  # Récupérer le mot saisi par l'utilisateur
    mot_cache = "pixel"  # Le mot caché à deviner
    if mot_saisi == mot_cache:
        #messagebox.showinfo("Bravo!", "Vous avez deviné le mot caché.")
        entry_mot.place_forget()
        button_verifier.place_forget()
        label_chances.place_forget()
        arreter_musique()  # Arrêter la musique de fond actuelle
        jouer_musique(victory_music)  # Jouer la musique de victoire
        label_instructions['text'] = "Felicitation vous avez reussi l'epreuve avec brio !!! "
        countdown_active = False  # Arrêter le compte à rebours
        changer_image_fond("reussite.png")  # Changer l'image de fond pour la victoire
        time.sleep(5)
        arreter_musique()
    else:
        messagebox.showinfo("Désolé", "Ce n'est pas le mot caché.")
        # Réduire le nombre de chances restantes et mettre à jour l'affichage
        chances_restantes -= 1
        label_chances.config(text="Chances restantes : {}".format(chances_restantes))
        if chances_restantes == 0:
            countdown_active = False
            entry_mot.place_forget()
            button_verifier.place_forget()
            label_chances.place_forget()
            arreter_musique()  # Arrêter la musique de fond actuelle
            label_instructions['text'] = "vous avez épuisé toutes vos chances. Game Over"
            changer_image_fond("tete_de_mort.png")  # Changer l'image de fond pour la défaite
            jouer_musique(explosion_music)
            time.sleep(3)
            arreter_musique()


# Fonction pour afficher le compte à rebours
def countdown():
    for i in range(10, -1, -1):  # Compte à rebours de 10 minutes (600 secondes)
        if countdown_active:
            minutes = i // 60
            seconds = i % 60
            countdown_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            time.sleep(1)
            if minutes == 0 and seconds == 30:
                arreter_musique()
                jouer_musique(minuteur_music)
    if countdown_active:
        #messagebox.showinfo("Temps écoulé", "Le temps est écoulé. Le jeu s'arrête.")
        entry_mot.place_forget()
        button_verifier.place_forget()        
        label_chances.place_forget()
        arreter_musique()  # Arrêter la musique de fond actuelle
        jouer_musique(explosion_music)
        label_instructions['text'] = "vous etes mort "
        changer_image_fond("tete_de_mort.png")  # Changer l'image de fond pour la défaite
        time.sleep(3)
        arreter_musique()
        
# Fonction pour changer l'image de fond de la fenêtre
def changer_image_fond(nom_image):
    image = tk.PhotoImage(file=nom_image)
    label_background.config(image=image)
    label_background.image = image

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu du mot caché")
fenetre.geometry('1800x800')

# Charger l'image de fond par défaut
image_fond_defaut = tk.PhotoImage(file="bg.png")  # Assurez-vous de placer votre image par défaut dans le même répertoire que votre script
label_background = tk.Label(fenetre, image=image_fond_defaut)
label_background.place(x=0, y=0, relwidth=1, relheight=1)

# Créer les widgets avec une police plus grande et fond white
label_instructions = tk.Label(fenetre, text=" Desarmorçez la bombe ", font=("Arial", 20), bg="black", fg="white")
entry_mot = tk.Entry(fenetre, font=("Arial", 16), bg="black", fg="white")
button_verifier = tk.Button(fenetre, text="Vérifier", font=("Arial", 16), command=verifier_mot)
countdown_label = tk.Label(fenetre, text="Temps restant : 50", font=("Arial", 40), bg="black", fg="white")

# Créer les widgets pour afficher les chances restantes
label_chances = tk.Label(fenetre, text="Chances restantes : {}".format(chances_restantes), font=("Arial", 12), bg="black", fg="white")
label_chances.place(relx=0.5, rely=0.5, anchor="center")

# Placer les widgets dans la fenêtre
countdown_label.pack()
label_instructions.place(relx=0.5, rely=0.2, anchor="center")
entry_mot.place(relx=0.5, rely=0.3, anchor="center")
entry_mot.pack_forget()
button_verifier.place(relx=0.5, rely=0.4, anchor="center")

# Initialiser le statut du compte à rebours
countdown_active = True



# Démarrer la musique de fond dans un thread séparé
musique_thread = threading.Thread(target=jouer_musique, args=(background_music,))
musique_thread.start()

# Lancer le compte à rebours dans un thread séparé
countdown_thread = threading.Thread(target=countdown)
countdown_thread.start() 
entry_mot.pack_forget()

# Lancer la boucle principale
fenetre.mainloop()