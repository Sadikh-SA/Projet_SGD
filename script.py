import db_connexion
from pprint import pprint
from bson.code import Code
db = db_connexion.db


#####################################################Jeux les mieux notés
meilleursJeux = db.Avis.aggregate([
    {'$lookup':{'from' :"Jeux",'localField':"IdJeu",'foreignField':"identifiant", 'as': "Jeux_avis"}},
    {'$group': {'_id':"$Jeux_avis.nom",'total':{'$avg':"$note"}}},
    {'$group':{'_id':"$_id",'moyenne':{'$sum':"$total"}}},
    {'$sort':{"moyenne":-1}}
])
#################Affichage
print("\n************************Jeux les mieux notes")
for jeu in meilleursJeux:
    print(jeu)

#####################################################PIRE NOTE VS MEILLEURE NOTE
noteMinMax = db.Avis.aggregate([
    {'$lookup':
        {'from' :"Jeux",
        'localField':"IdJeu",
        'foreignField':"identifiant",
        'as': "Jeux_avis"}
    },
    {'$group' :
        {
          '_id':'$Jeux_avis.nom',
          'noteMax': {'$max':'$note'},
          'noteMin': {'$min':'$note'},
        }
    }
])

#################Affichage
print("\n\n************************Note min / max de chaque jeu")
for note in noteMinMax:
    pprint (note)

#####################################################MEILLEURS JEUX AU MEILLEUR PRIX
platinum = db.Avis.aggregate([
    {'$lookup':
        {'from' :"Jeux",
        'localField':"IdJeu",
        'foreignField':"identifiant",
        'as': "Jeux_avis"}
    },
    {'$group':
        {
        '_id':{'nom':"$Jeux_avis.nom",'prix':"$Jeux_avis.prix"},
        'total':{'$avg':"$note"}
        }
    },
    {'$group':
        {
        '_id':"$_id",
        'moyenne':{'$sum':"$total"}
        }
    },
    {'$match':
        {
            'moyenne':{'$gt':70},
            '_id.prix':{'$lt':50}
        }
    }
])

#################Affichage
print("\n\n************************Meilleurs jeux au meilleur prix")
for jeu in platinum:
    pprint (jeu)


#####################################################JEUX LES PLUS COMMENTÉS
jeuxPopulaires = db.Avis.aggregate([
  {
    '$lookup':
    {
      'from' :"Jeux", 'localField':"IdJeu",'foreignField':"identifiant", 'as': "Jeux"
    }
  },
  {'$unwind':"$IdJeu"},
  {'$group':
    {
      '_id':{'nom':"$Jeux.nom"}, "nbAvis":{'$sum':1}
    }
  },
  {'$sort':{"nbAvis":-1}}
])

#################Affichage
print("\n\n************************Jeux qui font le plus parler")
for jeu in jeuxPopulaires:
    pprint (jeu)


#####################################################POURCENTAGE D'AVIS POSITIF
map = Code("""
    function(){
          var value = {note: this.note, nbAvisPositif:1, nbAvis:1};
          emit(this.IdJeu,value);
    }
""")
reduce = Code("""
    function(idjeu,val){
        reduceValue = {nbAvisPositif:0, nbAvis:0};
        for(var i=0; i<val.length; i++)
        {
          reduceValue.nbAvis += val[i].nbAvis;
          if(val[i].note>50)
          {
            reduceValue.nbAvisPositif += val[i].nbAvisPositif;
          }
        }
        reduceValue.pourcentage=reduceValue.nbAvisPositif*100/reduceValue.nbAvis;
        return reduceValue;
    }
""")

#################Affichage
resultat = db.Avis.map_reduce(map,reduce,"pourcentageAvisPositifs");
print("\n\n************************Pourcentage d'avis positifs sur le site");
for res in resultat.find():
    pprint(res)


#####################################################MinMax
def minMax(nomJeu):
    noteMinMax = db.Avis.aggregate([
        {'$lookup':
            {'from' :"Jeux",
            'localField':"IdJeu",
            'foreignField':"identifiant",
            'as': "Jeux_avis"}
        },
        {'$group' :
            {
              '_id':nomJeu,
              'noteMax': {'$max':'$note'},
              'noteMin': {'$min':'$note'},
            }
        }
    ])
    for res in noteMinMax:
        print(res)

print("\n\n************************Note min / max de Mario Kart");
minMax("Mario Kart");

#####################################################COUP DE COEUR
def coupDeCoeur(nomJoueur):
    cdc = db.Avis.aggregate([
        {'$lookup':
            {'from' :"Jeux",
            'localField':"IdJeu",
            'foreignField':"identifiant",
            'as': "Jeux"}
        },
        {'$lookup':
            {'from' :"Joueur",
            'localField':"IdJoueur",
            'foreignField':"identifiant",
            'as': "Joueur"}
        },
        {'$group':
            {
            '_id':{'login':"$Joueur.login", 'nomJeu': '$Jeux.nom','note':'$note'}
            }
        },
        {'$match':
            {
                '_id.login':nomJoueur,
                '_id.note':{'$gt':70}
            }
        }
    ])
    for res in cdc:
        print(res)
#################Affichage
print("\n\n************************oa258899: ses coups de coeur");
coupDeCoeur("oa258899");


#####################################################RECHERCHE
def rechercheJeu(nomJeu):
    jeux = db.Avis.aggregate([
        {'$lookup':
            {'from' :"Jeux",
            'localField':"IdJeu",
            'foreignField':"identifiant",
            'as': "Jeux"}
        },
        {'$group':
            {
            '_id':"$Jeux.nom",
            'moyenne':{'$avg':"$note"}
            }
        },
        {'$sort':{"moyenne":-1}},
        {'$match':
            {
            '_id':{'$regex':'^'+nomJeu}
            }
        }
    ])
    for j in jeux : print(j)

#################Affichage
print("\n\n************************RECHERCHE: Mario");
rechercheJeu('Mario')
