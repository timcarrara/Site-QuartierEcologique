-- Suppression des tables --
DROP TABLE IF EXISTS ContratAppart;
DROP TABLE IF EXISTS Colocation;
DROP TABLE IF EXISTS CompteursMensuels;
DROP TABLE IF EXISTS Contrat;
DROP TABLE IF EXISTS Appartement;
DROP TABLE IF EXISTS TypeAppartement;
DROP TABLE IF EXISTS Locataire;
DROP TABLE IF EXISTS Batiment;

-- Création des tables --
CREATE TABLE Batiment(
   num_bat INT AUTO_INCREMENT,
   nom VARCHAR(50),
   nbr_appart INT,
   PRIMARY KEY(num_bat)
);

CREATE TABLE Locataire(
   num_locataire INT AUTO_INCREMENT,
   nom VARCHAR(50),
   prenom VARCHAR(50),
   tel VARCHAR(50),
   mail VARCHAR(50),
   rib VARCHAR(50),
   iban VARCHAR(50),
   age INT,
   PRIMARY KEY(num_locataire)
);

CREATE TABLE Contrat(
   num_contrat INT AUTO_INCREMENT,
   date_debut DATE,
   date_fin DATE,
   charges NUMERIC(5,2),
   num_locataire INT NOT NULL,
   PRIMARY KEY(num_contrat),
   FOREIGN KEY(num_locataire) REFERENCES Locataire(num_locataire)
);

CREATE TABLE CompteursMensuels(
   id_releve INT AUTO_INCREMENT,
   kw_h_elec DECIMAL(15,2),
   quantite_dechets DECIMAL(15,2),
   date_releve DATE,
   litre_eau DECIMAL(15,2),
   num_bat INT NOT NULL,
   PRIMARY KEY(id_releve),
   FOREIGN KEY(num_bat) REFERENCES Batiment(num_bat)
);

CREATE TABLE TypeAppartement(
   id_type INT AUTO_INCREMENT,
   libelle VARCHAR(10),
   PRIMARY KEY(id_type)
);

CREATE TABLE Colocation(
   id_coloc INT AUTO_INCREMENT,
   date_debut DATE,
   remarque VARCHAR(200),
   num_locataire INT NOT NULL,
   num_contrat INT NOT NULL,
   PRIMARY KEY(id_coloc),
   FOREIGN KEY(num_locataire) REFERENCES Locataire(num_locataire),
   FOREIGN KEY(num_contrat) REFERENCES Contrat(num_contrat)
);

CREATE TABLE Appartement(
   num_appart INT AUTO_INCREMENT,
   surface DECIMAL(5,2),
   loyer DECIMAL(15,2),
   etage INT,
   id_type INT NOT NULL,
   num_bat INT NOT NULL,
   PRIMARY KEY(num_appart),
   FOREIGN KEY(id_type) REFERENCES TypeAppartement(id_type),
   FOREIGN KEY(num_bat) REFERENCES Batiment(num_bat)
);

CREATE TABLE ContratAppart(
   num_appart INT,
   num_contrat INT,
   PRIMARY KEY(num_appart, num_contrat),
   FOREIGN KEY(num_appart) REFERENCES Appartement(num_appart),
   FOREIGN KEY(num_contrat) REFERENCES Contrat(num_contrat)
);

-- Ajout de données dans les tables --
INSERT INTO Batiment (num_bat, nom, nbr_appart) VALUES
(NULL, 'Bâtiment A', 10),
(NULL, 'Bâtiment B', 8),
(NULL, 'Bâtiment C', 12),
(NULL, 'Bâtiment D', 15),
(NULL, 'Bâtiment E', 9);

INSERT INTO Locataire (num_locataire, nom, prenom, tel, mail, rib, iban, age) VALUES
(NULL, 'Dupont', 'Jean', '0612345678', 'jean.dupont@email.com', 'FR123456789', 'FR76 3000 4000 7000 0123 4567 890', 62),
(NULL, 'Tremblay', 'Sophie', '0678901234', 'sophie.tremblay@email.com', 'FR987654321', 'FR12 3456 7890 0001 2345 6789 012', 34),
(NULL, 'Garcia', 'Luis', '0698765432', 'luis.garcia@email.com', 'FR456789012', 'FR98 7654 3210 0009 8765 4321 098', 23),
(NULL, 'Chen', 'Wei', '0643210987', 'wei.chen@email.com', 'FR654321098', 'FR54 3210 9876 0008 7654 3210 987', 31),
(NULL, 'Abraham', 'Sarah', '0612345678', 'sarah.abraham@email.com', 'FR321098765', 'FR43 2109 8765 0007 6543 2109 876', 19);

INSERT INTO Contrat (num_contrat, date_debut, date_fin, num_locataire, charges) VALUES
(NULL, '2023-01-15', '2023-12-31', 1, 60.95),
(NULL, '2023-02-20', '2023-11-30', 2, 54.12),
(NULL, '2023-03-10', '2023-10-15', 3, 72.54),
(NULL, '2023-04-05', '2023-09-25', 4, 45.67),
(NULL, '2023-05-12', '2023-08-20', 5, 120.45);

INSERT INTO CompteursMensuels (id_releve, kw_h_elec, quantite_dechets, date_releve, litre_eau, num_bat) VALUES
(NULL, 250.75, 3.2, '2023-01-31', 500.2, 1),
(NULL, 320.50, 2.8, '2023-02-28', 480.0, 2),
(NULL, 280.00, 3.5, '2023-03-31', 510.3, 3),
(NULL, 310.25, 2.6, '2023-04-30', 490.5, 4),
(NULL, 290.80, 3.0, '2023-05-31', 520.1, 5);

INSERT INTO TypeAppartement (id_type, libelle) VALUES
(NULL, 'T1'),
(NULL, 'T2'),
(NULL, 'T3'),
(NULL, 'T4'),
(NULL, 'Studio');

INSERT INTO Colocation (id_coloc, date_debut, remarque, num_locataire, num_contrat) VALUES
(NULL, '2023-01-15', 'Colocation étudiante', 2, 1),
(NULL, '2023-02-20', 'Colocation jeune actif', 3, 2),
(NULL, '2023-03-10', 'Colocation seniors', 4, 3),
(NULL, '2023-04-05', 'Colocation mixte', 5, 4),
(NULL, '2023-05-12', 'Colocation artistique', 1, 5);

INSERT INTO Appartement (num_appart, surface, loyer, etage, id_type, num_bat) VALUES
(NULL, 50.00, 700.00, 2, 1, 1),
(NULL, 65.00, 850.00, 3, 2, 1),
(NULL, 80.00, 950.00, 1, 3, 2),
(NULL, 45.00, 600.00, 2, 4, 3),
(NULL, 40.00, 550.00, 3, 5, 3);

INSERT INTO ContratAppart (num_appart, num_contrat) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);