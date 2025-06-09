import tkinter as tk
import threading
import time
import socket
class Piece:
    def __init__(self, couleurs):
        self.couleur = couleurs



class Roi(Piece):
    def valider_mouvement(self, depart, arrivee):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        return abs(x_dep - x_arr) <= 1 and abs(y_dep - y_arr) <= 1
    def __repr__(self):
        if self.couleur == 'blanc':
            return ' KB '
        else:
            return ' KN '


class Reine(Piece):
    def valider_mouvement(self, depart, arrivee):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        return x_dep == x_arr or y_dep == y_arr or abs(x_dep - x_arr) == abs(y_dep - y_arr)
    def __repr__(self):
        if self.couleur == 'blanc':
            return ' QB '
        else:
            return ' QN '

class Tour(Piece):
    def valider_mouvement(self, depart, arrivee):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        return x_dep == x_arr or y_dep == y_arr
    def __repr__(self):
        if self.couleur == 'blanc':
            return ' TB '
        else:
            return ' TN '



class Fou(Piece):
    def valider_mouvement(self, depart, arrivee):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        return abs(x_dep - x_arr) == abs(y_dep - y_arr)
    def __repr__(self):
        if self.couleur == 'blanc':
            return ' FB '
        else:
            return ' FN '

class Cavalier(Piece):
    def valider_mouvement(self, depart, arrivee):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        return (abs(x_dep - x_arr) == 2 and abs(y_dep - y_arr) == 1) or (
                    abs(x_dep - x_arr) == 1 and abs(y_dep - y_arr) == 2)
    def __repr__(self):
        if self.couleur == 'blanc':
            return ' CB '
        else:
            return ' CN '

class Pion(Piece):
    def valider_mouvement(self, depart, arrivee, promotion=False):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        if self.couleur == 'blanc':
            if promotion and x_arr == 7:
                return y_dep == y_arr and x_arr - x_dep == 1
            if x_arr - x_dep == 1:
                if y_dep == y_arr:
                    return True
                if abs(y_dep - y_arr) == 1 and x_arr - x_dep == 1:
                    return True
            if x_dep==1 and  x_arr - x_dep == 2:
                if y_dep == y_arr:
                    return True
        else:
            if promotion and x_arr == 0:
                return y_dep == y_arr and x_dep - x_arr == 1
            if x_dep - x_arr == 1:
                if y_dep == y_arr:
                    return True
                if abs(y_dep - y_arr) == 1 and x_dep - x_arr == 1:
                    return True
            if x_dep==6 and  x_dep - x_arr == 2:
                if y_dep == y_arr:
                    return True
        return False
    def __repr__(self):
        if self.couleur == 'blanc':
            return ' PB '
        else:
            return ' PN '

class Plateau:
    def __init__(self):
        self.board = self.initialiser_plateau()
        self.rois = {'blanc': None, 'noir': None}
        self.trouver_rois()
        self.roque_disponible = {'blanc': True, 'noir': True}
        self.joueur_actuel = 'blanc'  # Le joueur blanc commence

    def jouer(self, gui,client,player_color):
        gui.receive_moves()

    def obtenir_position(self, message,gui):
        while True:
            try:
                gui.cli=False
                while gui.cli==False:
                    x=0
                x, y = gui.selected_square[0], gui.selected_square[1]
                if not (0 <= x < 8 and 0 <= y < 8):
                    raise ValueError
                return x, y
            except (IndexError, ValueError):
                print("Position invalide. Réessayez.")
    def initialiser_plateau(self):
        plateaus = [[], [], [], [], [], [], [], []]
        for i in range(8):
            for j in range(8):
                plateaus[i].append(None)
        plateaus[0][0] = Tour('blanc')
        plateaus[0][1] = Cavalier('blanc')
        plateaus[0][2] = Fou('blanc')
        plateaus[0][3] = Reine('blanc')
        plateaus[0][4] = Roi('blanc')
        plateaus[0][5] = Fou('blanc')
        plateaus[0][6] = Cavalier('blanc')
        plateaus[0][7] = Tour('blanc')

        plateaus[7][0] = Tour('noir')
        plateaus[7][1] = Cavalier('noir')
        plateaus[7][2] = Fou('noir')
        plateaus[7][3] = Reine('noir')
        plateaus[7][4] = Roi('noir')
        plateaus[7][5] = Fou('noir')
        plateaus[7][6] = Cavalier('noir')
        plateaus[7][7] = Tour('noir')

        for i in range(8):
            plateaus[1][i] = Pion('blanc')
            plateaus[6][i] = Pion('noir')

        return plateaus

    def afficher_plateau(self):
        c=0
        for row in self.board:
            print("[",end='')
            c=0
            for i in row:
                c+=1
                if i==None:
                    print("    ",end='')
                else:
                    print(i,end='')
                if c!=8:
                    print(",",end="")
            print("]")
    def deplacer_piece2(self, depart, arrivee):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        x_diff = x_arr-x_dep
        y_diff = y_arr - y_dep
        r=0
        piece = self.board[x_dep][y_dep]
        p2 = self.board[x_arr][y_arr]
        if piece is None:
            print("Il n'y a pas de pièce à cet emplacement !")
            return False
        elif piece.couleur != self.joueur_actuel:
            print("le pion choisie est de la mauvaise couleur")
            return False
        elif self.board[x_arr][y_arr] is not None and p2.couleur==piece.couleur:
            print("Une pièce occupe déjà cette case !")
            return False
        elif not piece.valider_mouvement(depart, arrivee):
            print("Mouvement invalide pour cette pièce !")
            return False
        else:
            if not isinstance(piece, Cavalier):
                while x_diff!=0 or y_diff!=0:
                    if x_diff == 0:
                        if y_diff>0:
                            y_diff-=1
                        else:
                            y_diff+=1
                        if self.board[x_dep][y_dep+y_diff] is not None and y_diff!=0:
                            print("mauvais deplacement")
                            return False

                    elif y_diff == 0:
                        if x_diff > 0:
                            x_diff -= 1
                        else:
                            x_diff += 1
                        if self.board[x_dep+x_diff][y_dep] is not None and x_diff != 0:
                            print("mauvais deplacement")
                            return False
                    else:
                        if x_diff > 0:
                            x_diff -= 1
                        else:
                            x_diff += 1
                        if y_diff > 0:
                            y_diff -= 1
                        else:
                            y_diff += 1
                        if self.board[x_dep + x_diff][y_dep+y_diff] is not None and x_diff != 0:
                            print("mauvais deplacement")
                            return False
        if isinstance(piece, Pion):
            if piece.couleur == 'blanc':
                if abs(y_dep - y_arr) == 1 and x_arr - x_dep == 1:
                    print
                    if p2 is None or p2.couleur!='noir':
                        print("mauvais deplacement")
                        return False
            if piece.couleur == 'noir':
                if abs(y_dep - y_arr) == 1 and x_dep - x_arr == 1:
                    if p2 is None or p2.couleur!='blanc':
                        print("mauvais deplacement")
                        return False
            if piece.couleur == 'blanc':
                if abs(y_dep - y_arr) == 0 and x_arr - x_dep == 1:
                    if p2 is not None and p2.couleur == 'noir':
                        print("mauvais deplacement")
                        return False
            if piece.couleur == 'noir':
                if abs(y_dep - y_arr) == 0 and x_dep - x_arr == 1:
                    if p2 is not None and p2.couleur == 'blanc':
                        print("mauvais deplacement")
                        return False

        if isinstance(piece, Roi):
            couleur = piece.couleur
            if self.roque_disponible[couleur]:
                if y_dep - y_arr == 2:  # Petit roque
                    if not self.verifier_case_vide((x_dep, y_dep - 1)) or not self.verifier_case_vide(
                            (x_dep, y_dep - 2)):
                        print("Impossible de faire le roque !")
                        return False
                    if self.est_en_echec(couleur) or self.est_en_echec_apres_mouvement(couleur, depart, arrivee):
                        print("Impossible de faire le roque car le roi est en échec !")
                        return False
                    self.board[x_dep][y_dep - 1] = piece
                    self.board[x_dep][y_dep - 2] = self.board[x_dep][0]
                    self.board[x_dep][0] = None
                elif y_arr - y_dep == 2:  # Grand roque
                    if not self.verifier_case_vide((x_dep, y_dep + 1)) or not self.verifier_case_vide(
                            (x_dep, y_dep + 2)):
                        print("Impossible de faire le roque !")
                        return False
                    if self.est_en_echec(couleur) or self.est_en_echec_apres_mouvement(couleur, depart, arrivee):
                        print("Impossible de faire le roque car le roi est en échec !")
                        return False
                    self.board[x_dep][y_dep + 1] = piece
                    self.board[x_dep][y_dep + 1] = self.board[x_dep][7]
                    self.board[x_dep][7] = None
                self.roque_disponible[couleur] = False

        if isinstance(piece, Pion) and (x_arr == 0 or x_arr == 7):
            self.promotion_pion(arrivee, piece.couleur)

        self.board[x_dep][y_dep] = None
        self.board[x_arr][y_arr] = piece
        return True



    def deplacer_piece(self, depart, arrivee):
        x_dep, y_dep = depart
        x_arr, y_arr = arrivee
        x_diff = x_arr-x_dep
        y_diff = y_arr - y_dep
        r=0
        piece = self.board[x_dep][y_dep]
        p2 = self.board[x_arr][y_arr]
        if piece is None:
            print("Il n'y a pas de pièce à cet emplacement !")
            return False
        elif piece.couleur != self.joueur_actuel:
            print("le pion choisie est de la mauvaise couleur")
            return False
        elif self.board[x_arr][y_arr] is not None and p2.couleur==piece.couleur:
            print("Une pièce occupe déjà cette case !")
            return False
        elif not piece.valider_mouvement(depart, arrivee):
            print("Mouvement invalide pour cette pièce !")
            return False
        else:
            if not isinstance(piece, Cavalier):
                while x_diff!=0 or y_diff!=0:
                    if x_diff == 0:
                        if y_diff>0:
                            y_diff-=1
                        else:
                            y_diff+=1
                        if self.board[x_dep][y_dep+y_diff] is not None and y_diff!=0:
                            print("mauvais deplacement")
                            return False

                    elif y_diff == 0:
                        if x_diff > 0:
                            x_diff -= 1
                        else:
                            x_diff += 1
                        if self.board[x_dep+x_diff][y_dep] is not None and x_diff != 0:
                            print("mauvais deplacement")
                            return False
                    else:
                        if x_diff > 0:
                            x_diff -= 1
                        else:
                            x_diff += 1
                        if y_diff > 0:
                            y_diff -= 1
                        else:
                            y_diff += 1
                        if self.board[x_dep + x_diff][y_dep+y_diff] is not None and x_diff != 0:
                            print("mauvais deplacement")
                            return False
        if isinstance(piece, Pion):
            if piece.couleur == 'blanc':
                if abs(y_dep - y_arr) == 1 and x_arr - x_dep == 1:
                    if p2 is None or p2.couleur!='noir':
                        print("mauvais deplacement")
                        return False
            if piece.couleur == 'noir':
                if abs(y_dep - y_arr) == 1 and x_dep - x_arr == 1:
                    if p2 is None or p2.couleur!='blanc':
                        print("mauvais deplacement")
                        return False
            if piece.couleur == 'blanc':
                if abs(y_dep - y_arr) == 0 and x_arr - x_dep == 1:
                    if p2 is not None and p2.couleur=='noir':
                        print("mauvais deplacement")
                        return False
            if piece.couleur == 'noir':
                if abs(y_dep - y_arr) == 0 and x_dep - x_arr == 1:
                    if p2 is not None and p2.couleur=='blanc':
                        print("mauvais deplacement")
                        return False

        if self.est_en_echec_apres_mouvement(piece.couleur, depart, arrivee):
            print("le roi sera en échec !")
            return False

        if isinstance(piece, Roi):
            couleur = piece.couleur
            if self.roque_disponible[couleur]:
                if y_dep - y_arr == 2:  # Petit roque
                    if not self.verifier_case_vide((x_dep, y_dep - 1)) or not self.verifier_case_vide(
                            (x_dep, y_dep - 2)):
                        print("Impossible de faire le roque !")
                        return False
                    if self.est_en_echec(couleur) or self.est_en_echec_apres_mouvement(couleur, depart, arrivee):
                        print("Impossible de faire le roque car le roi est en échec !")
                        return False
                    self.board[x_dep][y_dep - 1] = piece
                    self.board[x_dep][y_dep - 2] = self.board[x_dep][0]
                    self.board[x_dep][0] = None
                elif y_arr - y_dep == 2:  # Grand roque
                    if not self.verifier_case_vide((x_dep, y_dep + 1)) or not self.verifier_case_vide(
                            (x_dep, y_dep + 2)):
                        print("Impossible de faire le roque !")
                        return False
                    if self.est_en_echec(couleur) or self.est_en_echec_apres_mouvement(couleur, depart, arrivee):
                        print("Impossible de faire le roque car le roi est en échec !")
                        return False
                    self.board[x_dep][y_dep + 1] = piece
                    self.board[x_dep][y_dep + 1] = self.board[x_dep][7]
                    self.board[x_dep][7] = None
                self.roque_disponible[couleur] = False

        if isinstance(piece, Pion) and (x_arr == 0 or x_arr == 7):
            self.promotion_pion(arrivee, piece.couleur)

        self.board[x_dep][y_dep] = None
        self.board[x_arr][y_arr] = piece
        return True

    def trouver_rois(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if isinstance(piece, Roi):
                    self.rois[piece.couleur] = (i, j)
    def est_en_echec(self, couleur):
        self.trouver_rois()
        roi_x, roi_y = self.rois[couleur]
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None and piece.couleur != couleur:
                    self.joueur_actuel=piece.couleur
                    if self.deplacer_piece2((i, j), (roi_x, roi_y)):
                        self.board[i][j] = piece
                        self.board[roi_x][roi_y] = Roi(couleur)
                        self.joueur_actuel=couleur
                        return True
        self.joueur_actuel = couleur
        return False
    def est_en_echec2(self, couleur):
        self.trouver_rois()
        roi_x, roi_y = self.rois[couleur]
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None and piece.couleur != couleur:
                    self.joueur_actuel=piece.couleur
                    if self.deplacer_piece((i, j), (roi_x, roi_y)):
                        self.board[i][j] = piece
                        self.board[roi_x][roi_y] = Roi(couleur)
                        self.joueur_actuel=couleur
                        return True
        self.joueur_actuel = couleur
        return False

    def est_en_echec_apres_mouvement(self, couleur, depart, arrivee):
        temp_piece = self.board[depart[0]][depart[1]]
        temp_piece_arrivee = self.board[arrivee[0]][arrivee[1]]
        self.board[arrivee[0]][arrivee[1]] = temp_piece
        self.board[depart[0]][depart[1]] = None
        est_echec = self.est_en_echec(couleur)
        self.board[arrivee[0]][arrivee[1]] = temp_piece_arrivee
        self.board[depart[0]][depart[1]] = temp_piece
        return est_echec
    def est_en_echec_apres_mouvement2(self, couleur, depart, arrivee):
        temp_piece = self.board[depart[0]][depart[1]]
        temp_piece_arrivee = self.board[arrivee[0]][arrivee[1]]
        self.board[arrivee[0]][arrivee[1]] = temp_piece
        self.board[depart[0]][depart[1]] = None
        est_echec = self.est_en_echec2(couleur)
        self.board[arrivee[0]][arrivee[1]] = temp_piece_arrivee
        self.board[depart[0]][depart[1]] = temp_piece
        return est_echec
    def echec_et_mat(self,couleur):
        roi_x, roi_y = self.rois[couleur]
        for i in range(8):
            for j in range(8):
                depart=[i,j]
                piece = self.board[i][j]
                if piece is not None and piece.couleur == couleur:
                    for i2 in range(8):
                        for j2 in range(8):
                            arrivee=[i2,j2]
                            piece2 = self.board[i2][j2]
                            if self.deplacer_piece(depart, arrivee):
                                self.board[i2][j2] = piece2
                                self.board[i][j] = piece
                                if not self.est_en_echec_apres_mouvement2(couleur,depart,arrivee):
                                    return False
        return True

    def verifier_case_vide(self, position):
        x, y = position
        return self.board[x][y] is None

    def promotion_pion(self, position, couleur):
        x, y = position
        choix_promotion = input("Choisissez la pièce de promotion (Reine, Tour, Fou, Cavalier): ")
        piece_promotion = None
        if choix_promotion.lower() == "reine":
            piece_promotion = Reine(couleur)
        elif choix_promotion.lower() == "tour":
            piece_promotion = Tour(couleur)
        elif choix_promotion.lower() == "fou":
            piece_promotion = Fou(couleur)
        elif choix_promotion.lower() == "cavalier":
            piece_promotion = Cavalier(couleur)
        else:
            print("Choix invalide. Promotion par défaut à la reine.")
            piece_promotion = Reine(couleur)
        self.board[x][y] = piece_promotion
class ChessGUI:
    def __init__(self, root, board,client,player_color):
        self.root = root
        self.board = board
        self.selected_square = None  # Variable to store the clicked square
        self.client = client
        self.player_color = player_color
        self.cli = False
        self.create_widgets()
        threading.Thread(target=self.receive_moves, daemon=True).start()
    def change(self,board):
        self.board=board
        self.joueur_actuel = board.joueur_actuel
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=800)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        colors = ['white', 'gray']
        for row in range(8):
            for col in range(8):
                x1 = col * 100
                y1 = row * 100
                x2 = x1 + 100
                y2 = y1 + 100
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece:
                    x = col * 100 + 50
                    y = row * 100 + 50
                    self.canvas.create_text(x, y, text=str(piece), font=('Helvetica', 24))

    def refresh(self):
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
    def on_click(self, event):
        if self.player_color==self.board.joueur_actuel:
            col = event.x // 100
            row = event.y // 100
            if self.selected_square is None:
                self.selected_square = (row, col)
                self.cli = True
                print("ok bro")
            else:
                start_pos = self.selected_square
                end_pos = (row, col)
                self.selected_square = None
                self.change(self.board)
                self.refresh()
                print("Tour du joueur", self.board.joueur_actuel)
                depart = start_pos
                arrivee = end_pos
                if self.board.deplacer_piece(depart, arrivee):
                    self.change(self.board)
                    self.refresh()
                    self.client.send(f"{start_pos[0]},{start_pos[1]},{end_pos[0]},{end_pos[1]}".encode('utf-8'))
                    self.board.joueur_actuel = 'noir' if self.board.joueur_actuel == 'blanc' else 'blanc'
                    if self.board.est_en_echec(self.board.joueur_actuel):
                        print("Le roi est en échec !")
                        if self.board.echec_et_mat(self.board.joueur_actuel):
                            print("Échec et mat. Le joueur", self.board.joueur_actuel, "a perdu !")

    def receive_moves(self):
        while True:
            move = self.client.recv(1024).decode('utf-8')
            print(move)
            start_row, start_col, end_row, end_col = map(int, move.split(','))
            print("Tour du joueur", self.board.joueur_actuel)
            depart = (start_row,start_col)
            arrivee =  (end_row, end_col)
            if self.board.deplacer_piece(depart, arrivee):
                self.change(self.board)
                self.refresh()
                self.board.joueur_actuel = 'noir' if self.board.joueur_actuel == 'blanc' else 'blanc'
                if self.board.est_en_echec(self.board.joueur_actuel):
                    print("Le roi est en échec !")
                    if self.board.echec_et_mat(self.board.joueur_actuel):
                        print("Échec et mat. Le joueur", self.board.joueur_actuel, "a perdu !")
                        break


if __name__ == "__main__":
    # Adresse IP publique ou nom de domaine du serveur
    server_ip = '127.0.0.1'

    # Se connecter au serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5555))
    player_color = client_socket.recv(1024).decode('utf-8')

    # Démarrer l'interface graphique
    root = tk.Tk()
    root.title("Jeu d'échecs en ligne")

    board = Plateau()
    gui = ChessGUI(root, board, client_socket, player_color)

    root.mainloop()