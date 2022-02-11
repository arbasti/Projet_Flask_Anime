
#------------------------------------------------------------------------
from flask import *
import sqlite3
#------------------------------------------------------------------------


def lire_base(table):
	""" Récupère tous les éléments de la table en question
		Le renvoie sous forme de tuple
	"""
	connexion = sqlite3.connect("bdd_anime.db")
	curseur = connexion.cursor()
	requete_sql = """
	SELECT *
	FROM ?;"""
	resultat = curseur.execute(requete_sql, (table))
	resultat = resultat.fetchall()
	connexion.close()
	return resultat


def index_max(table):
	""" Récupère l'id du prochain enregistrement
		On renvoie un entier
	"""
	connexion = sqlite3.connect("bdd_anime")
	curseur = connexion.cursor()
	requete_sql = """
	SELECT MAX(?)
	FROM ?;"""
	if table == "Animes":
		id_table = "id_anime"
	elif table == "Characters":
		id_table = "id_perso"
	resultat = curseur.execute(requete_sql, (id_table,table))
	index = resultat.fetchall()
	connexion.close()
	return int(index[0][0]) + 1  # Transtype le résultat de la recherche et ajoute 1


def recherche_sql_anime(donnee):
	"""
	"""

	parametre = ""
	connexion = sqlite3.connect('bdd/bdd_anime.db')
	curseur = connexion.cursor()

	if donnee != "":
		if donnee.isdigit():
			parametre = int(donnee)
			requete_sql = """
			SELECT *
			FROM Animes
			WHERE id_anime LIKE ?"""

		else:
			parametre = str('%' + donnee + '%')
			requete_sql = """
			SELECT *
			FROM Animes
			WHERE name_anime LIKE ?"""

	parametres = [parametre]
	print(parametres)

	resultat = curseur.execute(requete_sql, parametres)
	liste_animes = resultat.fetchall()
	print(liste_animes)
	connexion.close()
	return liste_animes


def recherche_sql_character(donnees):
	"""
	"""

	parametre = ""
	connexion = sqlite3.connect('bdd/bdd_anime.db')
	curseur = connexion.cursor()

	if donnees[0] != "":

		if donnees[0].isdigit():
			parametre = int(donnees[0])
			requete_sql = """
			SELECT C.id_character, C.name_character, C.id_anime, A.name_anime
			FROM Characters AS C
			JOIN Animes AS A ON C.id_anime = A.id_anime
			WHERE C.id_character LIKE ?;
			"""

		else:
			parametre = str('%' + donnees[0] + '%')
			requete_sql = """
			SELECT C.id_character, C.name_character, C.id_anime, A.name_anime
			FROM Characters AS C
			JOIN Animes AS A ON C.id_anime = A.id_anime
			WHERE C.name_character LIKE ?;
			"""

	elif donnees[1] != "":

		if donnees[1].isdigit():
			parametre = int(donnees[1])
			requete_sql = """
			SELECT C.id_character, C.name_character, C.id_anime, A.name_anime
			FROM Characters AS C
			JOIN Animes AS A ON C.id_anime = A.id_anime
			WHERE A.id_anime LIKE ?;
			"""

		else:
			parametre = str('%' + donnees[1] + '%')
			requete_sql = """
			SELECT C.id_character, C.name_character, C.id_anime, A.name_anime
			FROM Characters AS C
			JOIN Animes AS A ON C.id_anime = A.id_anime
			WHERE A.name_anime LIKE ?;
			"""

	parametres = [parametre]
	print(parametres)

	resultat = curseur.execute(requete_sql, parametres)
	liste_characters = resultat.fetchall()
	print(liste_characters)
	connexion.close()
	return liste_characters


#------------------------------------------------------------------------


app = Flask(__name__, static_url_path='/static')

@app.route("/")
def accueil():
	""" Courte présentation du site via la page accueil
	"""
	return render_template("page_accueil.html")

@app.route("/recherche")
def recherchee():
	return render_template("menu_recherche.html")

@app.route("/recherche4anime")
def recherchee4anime():
	return render_template("recherche_anime.html")

@app.route("/recherche4character")
def recherchee4character():
	return render_template("recherche_character.html")

@app.route("/recherche_anime", methods= ['POST'])
def recherche_anime():
	result = request.form
	print(result)
	liste_animes = recherche_sql_anime(result['Anime_name'])
	return render_template("recherche_parametree_anime.html", anime_name = result['Anime_name'], animes = liste_animes)

@app.route("/recherche_character", methods= ['POST'])
def recherche_character():
	result = request.form
	liste_characters = recherche_sql_character([result['Character_name'], result['Anime_name']])
	return render_template("recherche_parametree_character.html", character_name = result['Character_name'], anime_name = result['Anime_name'], recherche = liste_characters)


#------------------------------------------------------------------------


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=1664, debug=True)


#------------------------------------------------------------------------

