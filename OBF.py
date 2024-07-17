import os
import random
import string
import tkinter as tk
from tkinter import filedialog, simpledialog
import time
import colorama
from colorama import Fore, Style
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

colorama.init(autoreset=True)

class ObfuscatorApp:
    def __init__(self):
        self.color = Fore.LIGHTYELLOW_EX  # Orange par défaut
        self.encryption_method = "xor"  # Méthode de chiffrement par défaut

    def show_animation(self):
        frames = [
            "F", "Fa", "Fai", "Fait", "Fait ", "Fait p", "Fait pa", "Fait par",
            "Fait par ", "Fait par T", "Fait par Ti", "Fait par Tit",
            "Fait par Tito", "Fait par Titou", "Fait par Titoua",
            "Fait par Titouan", "Fait par Titouan ", "Fait par Titouan C",
            "Fait par Titouan Co", "Fait par Titouan Cor", "Fait par Titouan Corn",
            "Fait par Titouan Corni", "Fait par Titouan Cornil",
            "Fait par Titouan Cornill", "Fait par Titouan Cornille",
        ]
        for frame in frames:
            self.clear_screen()
            print(self.color + frame)
            time.sleep(0.1)
        time.sleep(1)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = """
         $$$$$$\  $$$$$$$\  $$$$$$$$\       $$$$$$$\ $$\     $$\ 
        $$  __$$\ $$  __$$\ $$  _____|      $$  __$$\\$$\   $$  |
        $$ /  $$ |$$ |  $$ |$$ |            $$ |  $$ |\$$\ $$  / 
        $$ |  $$ |$$$$$$$\ |$$$$$\          $$$$$$$  | \$$$$  /  
        $$ |  $$ |$$  __$$\ $$  __|         $$  ____/   \$$  /   
        $$ |  $$ |$$ |  $$ |$$ |            $$ |         $$ |    
         $$$$$$  |$$$$$$$  |$$ |            $$ |         $$ |    
         \______/ \_______/ \__|            \__|         \__|    
        """
        print(self.color + banner)

    def generate_key(self, length):
        if self.encryption_method == "xor":
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        elif self.encryption_method == "aes":
            return os.urandom(32)  # AES-256 nécessite une clé de 32 octets
        elif self.encryption_method == "fernet":
            return Fernet.generate_key()

    def obfuscate(self, data, key):
        if self.encryption_method == "xor":
            return bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(data)])
        elif self.encryption_method == "aes":
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            return iv + encryptor.update(data) + encryptor.finalize()
        elif self.encryption_method == "fernet":
            f = Fernet(key)
            return f.encrypt(data)

    def deobfuscate(self, obfuscated_data, key):
        if self.encryption_method == "xor":
            return self.obfuscate(obfuscated_data, key)  # XOR est réversible
        elif self.encryption_method == "aes":
            iv = obfuscated_data[:16]
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            return decryptor.update(obfuscated_data[16:]) + decryptor.finalize()
        elif self.encryption_method == "fernet":
            f = Fernet(key)
            return f.decrypt(obfuscated_data)

    def save_key(self, key):
        with open(f"{self.encryption_method}_keys.txt", "a") as file:
            if isinstance(key, bytes):
                key = base64.b64encode(key).decode()
            file.write(f"{key}\n")

    def load_keys(self):
        filename = f"{self.encryption_method}_keys.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return file.read().splitlines()
        return []

    def select_file(self, title):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(title=title)

    def save_file(self, title):
        root = tk.Tk()
        root.withdraw()
        return filedialog.asksaveasfilename(title=title)

    def select_key(self):
        keys = self.load_keys()
        if not keys:
            print(f"Aucune clé enregistrée pour la méthode {self.encryption_method}.")
            return None
        
        print("Clés disponibles:")
        for i, key in enumerate(keys):
            print(f"{i + 1}. {key}")
        
        choice = input("Choisissez une clé (numéro) ou appuyez sur Entrée pour générer une nouvelle clé: ")
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            key = keys[int(choice) - 1]
            if self.encryption_method in ["aes", "fernet"]:
                return base64.b64decode(key)
            return key
        return self.generate_key(32 if self.encryption_method == "aes" else 16)

    def obfuscate_file(self, input_file, output_file, key):
        try:
            with open(input_file, 'rb') as file:
                content = file.read()
            obfuscated = self.obfuscate(content, key)
            with open(output_file, 'wb') as file:
                file.write(obfuscated)
            return True
        except IOError as e:
            print(f"Erreur lors de l'obfuscation du fichier: {e}")
            return False

    def deobfuscate_file(self, input_file, output_file, key):
        try:
            with open(input_file, 'rb') as file:
                obfuscated_content = file.read()
            deobfuscated = self.deobfuscate(obfuscated_content, key)
            with open(output_file, 'wb') as file:
                file.write(deobfuscated)
            return True
        except IOError as e:
            print(f"Erreur lors de la déobfuscation du fichier: {e}")
            return False

    def change_color(self):
        print("Couleurs disponibles:")
        print("1. Rouge")
        print("2. Vert")
        print("3. Bleu")
        print("4. Jaune")
        print("5. Magenta")
        print("6. Cyan")
        print("7. Orange (par défaut)")
        choice = input("Choisissez une couleur (1-7): ")
        if choice == '1':
            self.color = Fore.RED
        elif choice == '2':
            self.color = Fore.GREEN
        elif choice == '3':
            self.color = Fore.BLUE
        elif choice == '4':
            self.color = Fore.YELLOW
        elif choice == '5':
            self.color = Fore.MAGENTA
        elif choice == '6':
            self.color = Fore.CYAN
        elif choice == '7':
            self.color = Fore.LIGHTYELLOW_EX
        else:
            print("Choix invalide. La couleur reste inchangée.")

    def xor_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            print("\nMenu XOR:")
            print("1. Générer une clé")
            print("2. Obfusquer un fichier")
            print("3. Déobfusquer un fichier")
            print("4. Retour au menu principal")
            
            choice = input("Choisissez une option (1-4): ")
            
            if choice == '1':
                length = int(input("Entrez la longueur de la clé (16-32): "))
                if 16 <= length <= 32:
                    key = self.generate_key(length)
                    print(f"Clé générée: {key}")
                    self.save_key(key)
                    print("Clé sauvegardée.")
                else:
                    print("La longueur doit être entre 16 et 32.")
            elif choice == '2':
                self.obfuscate_workflow()
            elif choice == '3':
                self.deobfuscate_workflow()
            elif choice == '4':
                break
            else:
                print("Option invalide.")
            input("Appuyez sur Entrée pour continuer...")

    def aes_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            print("\nMenu AES:")
            print("1. Générer une clé")
            print("2. Obfusquer un fichier")
            print("3. Déobfusquer un fichier")
            print("4. Retour au menu principal")
            
            choice = input("Choisissez une option (1-4): ")
            
            if choice == '1':
                key = self.generate_key(32)
                print(f"Clé générée: {base64.b64encode(key).decode()}")
                self.save_key(key)
                print("Clé sauvegardée.")
            elif choice == '2':
                self.obfuscate_workflow()
            elif choice == '3':
                self.deobfuscate_workflow()
            elif choice == '4':
                break
            else:
                print("Option invalide.")
            input("Appuyez sur Entrée pour continuer...")

    def fernet_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            print("\nMenu Fernet:")
            print("1. Obfusquer un fichier")
            print("2. Déobfusquer un fichier")
            print("3. Retour au menu principal")
            
            choice = input("Choisissez une option (1-3): ")
            
            if choice == '1':
                self.obfuscate_workflow()
            elif choice == '2':
                self.deobfuscate_workflow()
            elif choice == '3':
                break
            else:
                print("Option invalide.")
            input("Appuyez sur Entrée pour continuer...")

    def obfuscate_workflow(self):
        input_file = self.select_file("Sélectionner le fichier à obfusquer")
        if input_file:
            if self.encryption_method == "fernet":
                key = Fernet.generate_key()
                print(f"Nouvelle clé Fernet générée: {key.decode()}")
                self.save_key(key)
            else:
                key = self.select_key()
            if key:
                output_file = self.save_file("Sauvegarder le fichier obfusqué")
                if output_file:
                    if self.obfuscate_file(input_file, output_file, key):
                        print(f"Fichier obfusqué sauvegardé sous {output_file}")

    def deobfuscate_workflow(self):
        input_file = self.select_file("Sélectionner le fichier à déobfusquer")
        if input_file:
            key = self.select_key()
            if key:
                output_file = self.save_file("Sauvegarder le fichier déobfusqué")
                if output_file:
                    if self.deobfuscate_file(input_file, output_file, key):
                        print(f"Fichier déobfusqué sauvegardé sous {output_file}")

    def run(self):
        self.show_animation()
        while True:
            self.clear_screen()
            self.print_banner()
            print("\nMenu Principal:")
            print("1. XOR (simple, non sécurisé)")
            print("2. AES (Advanced Encryption Standard)")
            print("3. Fernet (basé sur AES)")
            print("4. Changer la couleur")
            print("5. Quitter")
            
            choice = input("Choisissez une option (1-5): ")
            
            if choice == '1':
                self.encryption_method = "xor"
                self.xor_menu()
            elif choice == '2':
                self.encryption_method = "aes"
                self.aes_menu()
            elif choice == '3':
                self.encryption_method = "fernet"
                self.fernet_menu()
            elif choice == '4':
                self.change_color()
            elif choice == '5':
                self.clear_screen()
                self.print_banner()
                print("Au revoir!")
                break
            else:
                print("Option invalide. Veuillez choisir entre 1 et 5.")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    app = ObfuscatorApp()
    app.run()