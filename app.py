#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = '1606'


from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",  # "serveurmysql" sur les machines de l'IUT
            user="kstrub",
            password="mdp",
            database="BDD_kstrub",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# chercher des informations
# mycursor = get_db().cursor()
# sql='''   SELECT      '''
# mycursor.execute(sql)
# liste_enregistrement = mycursor.fetchall()
# un_enregistrement = mycursor.fetchone()

# ajouter, modifier ou supprimer des informations
# mycursor = get_db().cursor()
# sql=""
# mycursor.execute(sql)
# get_db().commit()

# mysql --user=mcourvo8  --password=1606 --host=localhost --database=BDD_mcourvo8 < sql_projet.sql
# source launcher.sh

####################################################################

@app.route('/')
@app.route('/accueil')
def accueil():
 return render_template('layout.html')

####################################################################

@app.route('/colocations/show')
def colocShow():
    mycursor = get_db().cursor()
    sql=''' SELECT * FROM Colocation; '''
    mycursor.execute(sql)
    listeColoc = mycursor.fetchall()
    return render_template('colocations/colocations_show.html', colocations=listeColoc)

@app.route('/delete/coloc')
def colocDelete():
    mycursor = get_db().cursor()
    id = request.args.get('id')
    sql=''' DELETE FROM Colocation WHERE id_coloc=%s '''
    mycursor.execute(sql,id)
    get_db().commit()
    message = u'Colocation ' + id + ' supprimé!'
    flash(message, 'alert-danger')
    return redirect('/colocations/show')

@app.route('/add/coloc', methods=['GET'])
def addColoc():

    mycursor = get_db().cursor()
    sql = ''' SELECT num_locataire, nom, prenom FROM Locataire; '''
    mycursor.execute(sql)
    infosLoc = mycursor.fetchall()

    sql = ''' SELECT num_contrat, charges FROM Contrat; '''
    mycursor.execute(sql)
    infosContrat = mycursor.fetchall()

    return render_template('colocations/colocations_add.html', locataire=infosLoc, contrat=infosContrat)

@app.route('/coloc/add', methods=['POST'])
def colocAdd():
    date = request.form.get('date')
    remarque = request.form.get('remarque')
    numLoc = request.form.get('numLoc')
    numContrat = request.form.get('numContrat')
    tuple_sql = (date,remarque,numLoc,numContrat)
    mycursor = get_db().cursor()
    sql=" INSERT INTO Colocation (id_coloc, date_debut, remarque, num_locataire, num_contrat) VALUES (NULL, %s, %s, %s, %s); "
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Colocation ajoutée: date de début='+date+' | remarque='+remarque+' | numéro de locataire='+numLoc+' | numéro de contrat='+numContrat
    flash(message, 'alert-success')
    return redirect('/colocations/show')

@app.route('/edit/coloc', methods=['GET'])
def editColoc():
    id = request.args.get('id')

    mycursor = get_db().cursor()
    sql = ''' SELECT num_locataire, nom, prenom FROM Locataire; '''
    mycursor.execute(sql)
    infosLoc = mycursor.fetchall()

    sql = ''' SELECT num_contrat, charges FROM Contrat; '''
    mycursor.execute(sql)
    infosContrat = mycursor.fetchall()

    sql = ''' SELECT date_debut, remarque, num_locataire AS locataire, num_contrat AS contrat FROM Colocation WHERE id_coloc=%s; '''
    mycursor.execute(sql,id)
    coloc = mycursor.fetchone()
    return render_template('colocations/colocations_edit.html', locataire=infosLoc, contrat=infosContrat, colocation=coloc, id=id)

@app.route('/coloc/edit', methods=['POST'])
def colocEdit():
    id = request.form.get('id')
    date = request.form.get('date')
    remarque = request.form.get('remarque')
    numLoc = request.form.get('numLoc')
    numContrat = request.form.get('numContrat')
    tuple_sql = (date,remarque,numLoc,numContrat,id)
    mycursor = get_db().cursor()
    sql= " UPDATE Colocation SET date_debut = %s, remarque = %s, num_locataire = %s, num_contrat = %s WHERE id_coloc = %s; "
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Colocation ' + id + ' mis à jour: date de début=' + date + ' | remarque=' + remarque + ' | numéro de locataire=' + numLoc + ' | numéro de contrat=' + numContrat
    flash(message, 'alert-warning')
    return redirect('/colocations/show')

@app.route('/colocations/filter')
def colocationEtat():
    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM Colocation; '''
    mycursor.execute(sql)
    listeColoc = mycursor.fetchall()
    return render_template('colocations/colocations_etats.html', colocations=listeColoc)

@app.route('/filter/colocations', methods=['POST'])
def etatColocation():
    nom = request.form.get('nom')
    typeJeu = request.form.get('typeJeu')
    prixMin = request.form.get('prixMin')
    prixMax = request.form.get('prixMax')
    if prixMin < prixMax:
        message = u'Le prix minimum doit être inférieur au prix maximum!'
        flash(message, 'alert-danger')
    else:
        message = u'Liste des jeux contenant "' + nom + '" de type "' + typeJeu + '" compris entre ' + prixMin + '€ et ' + prixMax + '€'
        flash(message, 'alert-primary')
    return redirect('/filtre/catalogue')

####################################################################

@app.route('/appartements/show')
def appartShow():
    mycursor = get_db().cursor()
    sql=''' SELECT * FROM Appartement; '''
    mycursor.execute(sql)
    listeAppart = mycursor.fetchall()
    return render_template('appartements/appartements_show.html', appartements=listeAppart)

@app.route('/delete/appart')
def appartDelete():
    mycursor = get_db().cursor()
    id = request.args.get('id')

    sql=''' DELETE FROM ContratAppart WHERE num_appart=%s '''
    mycursor.execute(sql,id)
    get_db().commit()

    sql = ''' DELETE FROM Appartement WHERE num_appart=%s '''
    mycursor.execute(sql, id)
    get_db().commit()

    message = u'Appartement ' + id + ' supprimé!'
    flash(message, 'alert-danger')
    return redirect('/appartements/show')

@app.route('/add/appart', methods=['GET'])
def addAppart():

    mycursor = get_db().cursor()
    sql = ''' SELECT id_type, libelle FROM TypeAppartement; '''
    mycursor.execute(sql)
    infosType = mycursor.fetchall()

    sql = ''' SELECT num_bat, nom FROM Batiment; '''
    mycursor.execute(sql)
    infosBat = mycursor.fetchall()

    return render_template('appartements/appartements_add.html', typeAppart=infosType, batiment=infosBat)

@app.route('/appart/add', methods=['POST'])
def appartAdd():
    surface = request.form.get('surface')
    loyer = request.form.get('loyer')
    etage = request.form.get('etage')
    id_type = request.form.get('id_type')
    num_bat = request.form.get('num_bat')
    tuple_sql = (surface,loyer,etage,id_type,num_bat)
    mycursor = get_db().cursor()
    sql=" INSERT INTO Appartement (num_appart, surface, loyer, etage, id_type, num_bat) VALUES (NULL, %s, %s, %s, %s, %s); "
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Appartement ajoutée: surface='+surface+' | loyer='+loyer+' | étage='+etage+' | type='+id_type+ '| bâtiment='+num_bat
    flash(message, 'alert-success')
    return redirect('/appartements/show')

@app.route('/edit/appart', methods=['GET'])
def editAppart():
    id = request.args.get('id')

    mycursor = get_db().cursor()
    sql = ''' SELECT id_type, libelle FROM TypeAppartement; '''
    mycursor.execute(sql)
    infosType = mycursor.fetchall()

    sql = ''' SELECT num_bat, nom FROM Batiment; '''
    mycursor.execute(sql)
    infosBat = mycursor.fetchall()

    sql = ''' SELECT num_appart, surface, loyer, etage, id_type, num_bat FROM Appartement WHERE num_appart=%s; '''
    mycursor.execute(sql,id)
    appart = mycursor.fetchone()
    return render_template('appartements/appartements_edit.html', typeAppart=infosType, batiment=infosBat, appartement=appart, id=id)

@app.route('/appart/edit', methods=['POST'])
def appartEdit():
    id = request.form.get('id')
    surface = request.form.get('surface')
    loyer = request.form.get('loyer')
    etage = request.form.get('etage')
    id_type = request.form.get('id_type')
    num_bat = request.form.get('num_bat')
    tuple_sql = (surface, loyer, etage, id_type, num_bat, id)
    mycursor = get_db().cursor()
    sql = " UPDATE Appartement SET surface=%s, loyer=%s, etage=%s, id_type=%s, num_bat=%s WHERE num_appart=%s; "
    mycursor.execute(sql, tuple_sql)
    get_db().commit()
    message = u'Appartement '+ id +' mis à jour: surface=' + surface + ' | loyer=' + loyer + ' | étage=' + etage + ' | type=' + id_type + '| bâtiment=' + num_bat
    flash(message, 'alert-warning')
    return redirect('/appartements/show')

@app.route('/appartements/filter')
def etat_appartements():
    mycursor = get_db().cursor()

    #Recap des données de chaque appartement
    sql1 = '''  SELECT Appartement.num_appart, Appartement.surface, TypeAppartement.libelle,  Appartement.loyer, Appartement.etage, Appartement.num_bat, ROUND((Appartement.loyer/Appartement.surface), 2) AS loyer_surface
     FROM Appartement
     INNER JOIN TypeAppartement ON Appartement.id_type = TypeAppartement.id_type;    '''
    mycursor.execute(sql1)
    listeAppart = mycursor.fetchall()

    # Recap des données par types d'appartement
    sql2 = '''  SELECT TypeAppartement.libelle, SUM(Appartement.loyer) AS total_loyer, ROUND(AVG(Appartement.loyer),  2) AS moyenne_loyer
    FROM Appartement
    INNER JOIN TypeAppartement ON Appartement.id_type = TypeAppartement.id_type
    GROUP BY TypeAppartement.libelle; '''
    mycursor.execute(sql2)
    listeAppart2 = mycursor.fetchall()

    # Recap des données des appartements
    sql3 = '''  SELECT COUNT(*) AS total_appartements, SUM(loyer) AS total_loyer, ROUND(AVG(loyer), 2) AS moyenne_loyer, SUM(surface) AS total_surface, ROUND(AVG(surface), 2) AS moyenne_surface
    FROM Appartement;    '''
    mycursor.execute(sql3)
    listeAppart3 = mycursor.fetchall()

    return render_template('/appartements/filtrer_appartements.html', appartement=listeAppart, appartement2=listeAppart2, appartement3=listeAppart3)

####################################################################

@app.route('/contrats/show')
def show_contrats():
    # print(contrats)
    mycursor = get_db().cursor()
    sql= '''  SELECT  * FROM Contrat;    '''
    mycursor.execute(sql)
    listeContrat = mycursor.fetchall()
    return render_template('/contrats/show_contrats.html', contrats=listeContrat)

@app.route('/add/contrats', methods=['GET'])
def addContrat():
    mycursor = get_db().cursor()
    sql = ''' SELECT num_contrat FROM Contrat; '''
    mycursor.execute(sql)
    listeContrat = mycursor.fetchall()
    sqll = ''' SELECT num_locataire FROM Locataire; '''
    mycursor.execute(sqll)
    listeLocataire = mycursor.fetchall()
    return render_template('contrats/add_contrats.html', contrats=listeContrat, contratss=listeLocataire)

@app.route('/contrats/add', methods=['POST'])
def contratAdd():
    date_debut = request.form.get('date_debut')
    date_fin = request.form.get('date_fin')
    charges = request.form.get('charges')
    num_locataire = request.form.get('num_locataire')
    tuple_sql = (date_debut,date_fin,charges,num_locataire)
    mycursor = get_db().cursor()
    sql=" INSERT INTO Contrat (num_Contrat, date_debut, date_fin, charges, num_locataire) VALUES (NULL, %s, %s, %s, %s); "
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Contrat ajouté: date de début='+date_debut+' | date de fin='+date_fin+' | montant des charges='+charges+' | numéro de locataire='+num_locataire
    flash(message, 'alert-success')
    return redirect('/contrats/show')


@app.route('/delete/contrats')
def deleteContrats():
    mycursor = get_db().cursor()
    id = request.args.get('id')
    sql=''' DELETE FROM Contrat WHERE num_contrat=%s '''
    mycursor.execute(sql,id)
    get_db().commit()
    message = u'Contrat ' + id + ' supprimé!'
    flash(message, 'alert-danger')
    return redirect('/contrats/show')

@app.route('/edit/contrats', methods=['GET'])
def editContrat():
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = ''' SELECT num_locataire FROM Contrat; '''
    mycursor.execute(sql)
    listeContrat = mycursor.fetchall()
    sql = ''' SELECT date_debut, date_fin, charges, num_locataire AS locataire FROM Contrat WHERE num_contrat=%s; '''
    mycursor.execute(sql,id)
    contr = mycursor.fetchone()
    return render_template('contrats/edit_contrats.html', contrats=listeContrat, contrat=contr, id=id)

@app.route('/contrats/edit', methods=['POST'])
def contratEdit():
    id = request.form.get('id')
    date_debut = request.form.get('date_debut')
    date_fin = request.form.get('date_fin')
    charges = request.form.get('charges')
    num_locataire = request.form.get('num_locataire')
    tuple_sql = (date_debut,date_fin,charges,num_locataire, id)
    mycursor = get_db().cursor()
    sql= " UPDATE Contrat SET date_debut = %s, date_fin = %s, charges = %s, num_locataire = %s WHERE num_contrat = %s; "
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Contrat ' + id + ' mis à jour: date de début=' + date_debut + ' | date de fin=' + date_fin + ' | montant des charges=' + charges + ' | numéro de locataire=' + num_locataire
    flash(message, 'alert-warning')
    return redirect('/contrats/show')

@app.route('/contrats/filter')
def etat_contrats():
    mycursor = get_db().cursor()

    #recap des données avec moyennes, etc...
    sql1 = '''  SELECT COUNT(num_contrat) AS nombre_contrat, ROUND(AVG(charges), 2) AS moyenne_charges, SUM(charges) AS total_charges FROM Contrat;    '''
    mycursor.execute(sql1)
    listeContrat = mycursor.fetchall()

    # Contrats de colocation avec les détails du locataire :
    sql2 = '''  SELECT Contrat.num_contrat, Contrat.date_debut, Contrat.date_fin, Contrat.charges, Locataire.nom, Locataire.prenom
    FROM Contrat
    INNER JOIN Colocation ON Contrat.num_contrat = Colocation.num_contrat
    INNER JOIN Locataire ON Colocation.num_locataire = Locataire.num_locataire;
    '''
    mycursor.execute(sql2)
    listeContrat2 = mycursor.fetchall()

    # Contrat le moins coûteux :
    sql3 = '''  SELECT *
    FROM Contrat
    WHERE charges = (SELECT MIN(charges) FROM Contrat); '''
    mycursor.execute(sql3)
    listeContrat3 = mycursor.fetchall()

    # Contrat le plus coûteux :
    sql4 = '''  SELECT *
    FROM Contrat
    WHERE charges = (SELECT MAX(charges) FROM Contrat);        '''
    mycursor.execute(sql4)
    listeContrat4 = mycursor.fetchall()

    return render_template('/contrats/etat_contrats.html', contrats=listeContrat, contrats2=listeContrat2, contrats3=listeContrat3, contrats4=listeContrat4)

####################################################################

@app.route('/compteursMensuels/show')
def compteur():
    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM CompteursMensuels; '''
    mycursor.execute(sql)
    listeCompteurs = mycursor.fetchall()
    return render_template('compteursMensuels/compteur.html', compteur = listeCompteurs)

@app.route('/compteursMensuels/filter')
def etat_compteur():
    mycursor = get_db().cursor()
    #recap des données avec moyennes, etc...
    sql1 = '''SELECT 
    ROUND(SUM(Appartement.surface) / COUNT(CompteursMensuels.kw_h_elec), 2) AS ratio_surface_kwh
    FROM 
        Appartement
    JOIN 
        Batiment ON Appartement.num_bat = Batiment.num_bat
    JOIN 
        CompteursMensuels ON Batiment.num_bat = CompteursMensuels.num_bat;'''
    mycursor.execute(sql1)
    listeCompteur = mycursor.fetchall()

    sql2 = '''SELECT ROUND(AVG(litre_eau), 2) AS moyenne_compteur_eau
    FROM CompteursMensuels;'''
    mycursor.execute(sql2)

    listeCompteur1 = mycursor.fetchall()

    sql3 = '''SELECT *
    FROM CompteursMensuels
    WHERE litre_eau >= 148 ;'''
    mycursor.execute(sql3)

    listeCompteur2 = mycursor.fetchall()

    return render_template('compteursMensuels/etats_compteur.html', compteur=listeCompteur , compteur1=listeCompteur1, compteur2=listeCompteur2  )

@app.route('/compteursMensuels/add', methods=['GET'])
def add_compteurs():
    mycursor = get_db().cursor()
    sql = ''' SELECT num_bat FROM Appartement; '''
    mycursor.execute(sql)
    num_bat = mycursor.fetchall()
    print('''affichage du formulaire pour saisir un étudiant''')
    return render_template('compteursMensuels/add_compteur.html', batiments=num_bat)

@app.route('/compteursMensuels/add', methods=['POST'])
def valid_add():
    kwh = request.form.get('kwh')
    dechets = request.form.get('dechets')
    date = request.form.get('date')
    eau = request.form.get('litre_eau')
    numbat = request.form.get('numBat')
    tuple_sql = (kwh, dechets, date, eau, numbat)
    mycursor = get_db().cursor()
    sql = " INSERT INTO CompteursMensuels ( kw_h_elec, quantite_dechets, date_releve, litre_eau, num_bat) VALUES (%s, %s, %s, %s, %s); "
    mycursor.execute(sql, tuple_sql)
    get_db().commit()
    message = u'relevé: ' + numbat + ' kwh: ' + kwh + 'dechets: ' + dechets + ' date: ' + date + ' eau: ' + eau + ' ajouté '
    flash(message, 'alert-success')
    return redirect('/compteursMensuels/show')

@app.route('/compteursMensuels/edit', methods=['GET'])
def editCompteur():
    id = request.args.get('id')

    mycursor = get_db().cursor()
    sql = ''' SELECT kw_h_elec, quantite_dechets, date_releve, litre_eau, num_bat FROM CompteursMensuels WHERE id_releve=%s; '''
    mycursor.execute(sql,id)
    infoCompteur = mycursor.fetchone()

    mycursor = get_db().cursor()
    sql = ''' SELECT num_bat FROM Batiment; '''
    mycursor.execute(sql)
    num_bat = mycursor.fetchall()
    return render_template('compteursMensuels/edit_compteur.html',CompteursMensuels=infoCompteur, id_releve=id, batiments=num_bat)

@app.route('/compteursMensuels/edit', methods=['POST'])
def compteurEdit():
    id = request.form.get('id_releve')

    print(id)

    kwh = request.form.get('kwh')
    dechets = request.form.get('dechets')
    date = request.form.get('date')
    eau = request.form.get('litre_eau')
    numbat = request.form.get('numBat')
    tuple_sql = (kwh, dechets, date, eau, numbat,id)
    mycursor = get_db().cursor()
    sql= " UPDATE CompteursMensuels SET kw_h_elec = %s, quantite_dechets = %s, date_releve = %s, litre_eau = %s, num_bat = %s WHERE id_releve = %s; "
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'relevé: ' + numbat + ' kwh: ' + kwh + 'dechets: ' + dechets + ' date: ' + date + ' eau: ' + eau + ' ajouté '
    flash(message, 'alert-warning')
    return redirect('/compteursMensuels/show')

@app.route('/delete/compteur/<id>', methods=["GET"])
def compteurDelete(id):
    mycursor = get_db().cursor()
    sql=''' DELETE FROM CompteursMensuels cm WHERE cm.id_releve=%s '''
    mycursor.execute(sql, (id,))
    get_db().commit()
    message = u'relevé ' + id + ' supprimé!'
    flash(message, 'alert-danger')
    return redirect("/compteursMensuels/show")

####################################################################

if __name__ == '__main__':
 app.run()