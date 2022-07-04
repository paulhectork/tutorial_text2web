from plotly.colors import make_colorscale
import plotly.graph_objs as go
from plotly.io import to_html
import json

from text2web_html import read_input  # on importe la fonction de l'autre fichier python


# --------------------------------------------------------------------
# intégrer des visualisations au fichier produit avec text2web_html.py
# disponible sous MIT License. tutoriel par Paul, H. Kervegan
# --------------------------------------------------------------------


def count_words():
    """
    compter les occurrences des différents mots de la source et les stocker dans un json
    :return:
    """
    source = read_input("../input/source.txt")  # on lit le fichier en entrée

    # comment faire pour compter tous les mots ? ce n'est pas une opération totalement anodine.
    # - d'abord, on nettoie le fichier : supprimer la ponctuation et les mots "courts"
    #   qui sont généralement des déterminants, supprimer les majuscules pour bien dédoublonner
    # - ensuite, il faut faire le comptage à proprement parler. cela demande 2 choses:
    #   - tokeniser au mot (c'est à dire, dire à python de traiter le texte mots par mots).
    #     python tokenénise les chaînes de caractères caractères par caractère (il lit lettre par lettre).
    #     il faut donc changer de type de données pour tokeniser correctement: on retype donc
    #     la source en liste.
    #   - il faut aussi un type de données qui permette d'associer à chaque mot, le nombre d'occurences du mot.
    #     dès qu'on parle d'associer une donnée à une autre (c'est-à-dire de faire du mapping), il faut penser
    #     dictionnaire ! c'est le type de donnée qui permet ça. en plus, les dictionnaires correspondent
    #     à du json, ils peuvent donc être passés à JavaScript ou à d'autres languages de programmation.
    # tout ce découpage peut sembler compliqué, mais en fait on réalise la même opération si on le fait à la
    # main: on commencerait par vouloir compter les mots directement dans le texte, mais on devrait vite
    # noter les choses. on se retrouverait à écrire sur un papier dans une colonne les mots,
    # dans une autre le nombre de fois qu'on mot apparaît: c'est le principe du dictionnaire !
    # (par contre, un cerveau peut retyper et retirer la ponctuation tout seul. c'est partique, d'être humain)

    source = source.lower()  # on met tout en minuscule

    # on commence donc par le nettoyage de la ponctuation. le processus doit être relativement évident
    # à ce stade: on prend une liste de ponctuation, on itère sur la liste, et à chaque fois qu'un
    # caractère apparaît, on le supprime
    punct = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
             '+', '=', '{', '}', '[', ']', ':', ';', '"', "'", '|',
             '<', '>', ',', '.', '?', '/', '~', '`']
    for p in punct:
        source = source.replace(p, "")

    # les listes, ça commence à être facile. ce qui peut être plus intéressant, c'est
    # de remplacer les accents par des caractères non-accentués. pour ce faire, on doit
    # associer un caractère accentué à sa version sans accent. vous l'avez deviné, il faut
    # donc un *dictionnaire*. un dictionnaire associe des clés et des valeurs. il s'écrit
    # de la manière suivante: dico = {clé1: valeur1, clé2: valeur2, cléN: valeurN}.
    # on peut accéder
    # - aux clés avec dico.keys(), qui produit une liste des clés
    # - aux valeurs avec dico.values(), qui produit une liste des valeurs
    # - à un mapping clé-valeur avec dico.items(), qui produit une liste des couples clés-valeurs
    #   on va utiliser cette fonction ci-dessous
    accents = {"é": "e", "è": "e", "ç": "c",  "à": "a", "ê": "e", "â": "a", "ô": "o",
               "ò": "o", "ï": "i", "ì": "i", "ö": "o"}

    # on déplie le dictionnaire une liste de couple de clés et de valeurs; on itère
    # sur tous les couples. si il y a une clé dans le texte (une lettre accentuée),
    # on la remplace par sa version non-accentuée (la valeur, donc)
    for key, value in accents.items():
        source = source.replace(key, value)  # remplacer la clé par la valeur: "é" => "e".

    # on a nettoyé le texte. il faut maintenant compter, et donc
    # - retyper la source en liste
    # - construire un dictionnaire d'occurrences

    # on fait une liste à partir de la source pour pouvoir travailler mot par mot (et non lettre par lettre)
    sourcelist = source.split()

    # on construit la base du dictionnaire: on sélectionne tous les mots uniques de plus de 2 lettres
    # dans sourcelist et on fait de ces valeurs les clés de notre dictionnaire d'occurrences
    occurrences = {}
    # on itère sur tous les mots s de sourcelist.
    for s in sourcelist:
        # si s fait plus de 2 lettres
        if len(s) > 2 and s != r"\n\n\n":
            # si c'est la première fois qu'on rencontre ce mot, il n'est pas dans les clés de notre dictionnaire
            # d'occurrences. on le rajoute donc avec dictionnaire[clé] = 1: on a trouvé cette clé une fois dans source.
            if s not in occurrences.keys():
                occurrences[s] = 1
            # si le mot s est déjà une clé de occurrences, on l'a déjà rencontré.
            # dans ce cas, on incrémente la valeur associée à s de 1.
            else:
                occurrences[s] += 1

    # voilà, le dictionnaire est construit ! pour plus d'élégance, on le réordonne
    # par nombre d'occurrences, c'est à dire en fonction des valeurs. ce n'est pas
    # une méthode évidente (je ne la comprends pas totalement), mais c'est celle
    # qui marche le mieux: on réordonne en fonction d'une clé (key). en toute
    # honnêteté pour ce genre de détails on regarde sur *humhum* stackoverflow *humhum*
    occurrences = {key: value for key, value in sorted(occurrences.items(), key=lambda item: item[1])}

    # maintenant, on écrit le json dans un fichier à l'aide de la bien nommée librairie json.
    # le fonctionnement est pareil que pour un fichier texte: on ouvre avec with open(), ensuite
    # on écrit (avec json.dump() pour du json)
    with open("../output/occurrences.json", mode="w") as fh:
        json.dump(occurrences, fh, indent=4)  # json.dump(data, fichier, indentation)

    return None


def figmaker():
    """
    pour finir le tutoriel, on va produire de jolies petites visualisations avec Plotly.
    la librairie a deux gros avantages: elle produit directement du HTML/JavaScript, et non
    une image statique. on a donc d'office un graphique interactif. en plus, Plotly python est la
    traduction en Python d'une librairie JavaScript; les versions python et js sont développées
    par la même entreprise, donc la version python est très complète et personnalisable. d'expérience,
    ce n'est pas une librairie évidente à prendre en main (du tout) si on veut travailler avec des données
    complexes ou qu'on doit préparer nos données. cependant, on a déjà bien préparé nos données avec la fonction
    au dessus. ça va donc être relativement simple. cette petite introduction va surtout nous servir à finir de nous
    familiariser avec la manipulation du json. on va aussi voir que json et le python, c'est quand même fort chouette !
    """
    count_words()  # on crée le json qui compte les mots

    # à ce stade, vous savez ce qui se passe: on ouvre un fichier json en lecture
    with open("../output/occurrences.json", mode="r") as fh:
        data = json.load(fh)  # on charche le json dans une variable. c'est un dictionnaire !

    # à un niveau abstrait, les librairies de visualisations fonctionnent de cette manière:
    # on a besoin de deux listes de valeurs, l'une pour les x/abscisses, l'autre pour les y/ordonnées.
    # il faut donc que chaque valeur de x ait son équivalent dans y, ce qui est le cas chez nous
    x = list(data.keys())  # l'axe des abscisses correspond à nos clés
    y = list(data.values())  # l'axe des ordonnées correspond à nos valeurs

    # on prépare le style de plotly: un dictionnaire pour les couleurs et une échelle de couleurs
    colors = {"white": "#ffffff", "cream": "#fcf8f7", "blue": "#0000ef", "purple": "#bd148b"}
    scale = make_colorscale([colors["blue"], colors["purple"]])  # créer une échelle de couleurs

    # plotly fonctionne en créant un object go.Figure qui contient d'un côté
    # des informations sur le graphique en lui-même (go.Bar), de l'autre des
    # informations sur le style et la mise en page (go.Layout)
    fig = go.Figure(
        data=[go.Bar(x=x, y=y, width=1.1, marker={"color": y, "colorscale": scale,
                                       "cauto": False, "cmin": 0, "cmax": 10},
                     hovertemplate="<b>'%{x}'</b>: %{y} occurrences<extra></extra>")],
        layout=go.Layout({
            "paper_bgcolor": colors["white"],
            "plot_bgcolor": colors["cream"],
            "margin": {"l": 5, "r": 5, "t": 30, "b": 30},
            # "showlegend": False,
            "yaxis_range": [0, 20],
            "xaxis": {"anchor": "x", "title": {"text": "Mot"}},
            "yaxis": {"anchor": "y", "title": {"text": "Nombre d'occurrences"}},
            "title": "Nombre d'occurrences par mot",
        })
    )

    # on transforme fig (qui est un objet figure, alors qu'on veut une chaîne
    # de caractères) en chaîne de caractères html
    htmlfig = to_html(fig, include_plotlyjs="cdn", full_html=False, default_width="100%",
                      default_height="70%")

    # on met à jour le fichier html en ajoutant le graphique au document
    with open("../output/catalog_web.html", mode="r") as fh:
        html = fh.read()  # on lit le fichier source
    html = html.replace("{PLACEHOLDER_GRAPH}", htmlfig)  # on remplace le placeholder par la figure

    # on écrit le nouveau fichier en sortie
    with open("../output/catalog_web.html", mode="w") as fh:
        fh.write(html)

    return None


if __name__ == "__main__":
    figmaker()