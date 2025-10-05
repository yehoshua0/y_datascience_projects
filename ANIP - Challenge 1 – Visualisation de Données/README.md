# DICTIONNAIRE DES VARIABLES ET GLOSSAIRE

## Challenge ANIP - Collecte et Analyse de Données Multisources pour le Bénin

---

**Date de création:** 05 Octobre 2025  
**Version:** 1.0  
**Pays cible:** Bénin (Code ISO: BEN)  
**Période couverte:** 2000-2024

---

## TABLE DES MATIÈRES

1. [Introduction](#introduction)
2. [Structure des Fichiers de Données](#structure-fichiers)
3. [Glossaire des Indicateurs](#glossaire-indicateurs)
   - 3.1 [Indicateurs Démographiques](#indicateurs-demographiques)
   - 3.2 [Indicateurs Économiques](#indicateurs-economiques)
   - 3.3 [Indicateurs Sociaux](#indicateurs-sociaux)
4. [Sources de Données](#sources-donnees)
5. [Méthodologie de Calcul des Scores de Qualité](#methodologie-qualite)
6. [Unités et Formats](#unites-formats)
7. [Notes d'Utilisation](#notes-utilisation)

---

## 1. INTRODUCTION {#introduction}

Ce dictionnaire documente l'ensemble des variables, indicateurs et métadonnées utilisés dans le cadre du Challenge ANIP pour la collecte et l'analyse de données multisources sur le Bénin.

### Objectifs du dictionnaire

- Fournir une définition claire et précise de chaque variable
- Expliquer la méthodologie de calcul des indicateurs
- Documenter les sources et leur fiabilité
- Assurer la reproductibilité des analyses
- Faciliter l'interprétation des résultats

### Public cible

- Analystes de données
- Décideurs politiques
- Chercheurs
- Équipes techniques ANIP

---

## 2. STRUCTURE DES FICHIERS DE DONNÉES {#structure-fichiers}

### 2.1 Colonnes Standards

Tous les fichiers consolidés contiennent les colonnes suivantes :

| Nom de Colonne      | Type      | Obligatoire | Description                      | Exemple                       |
| ------------------- | --------- | ----------- | -------------------------------- | ----------------------------- |
| **pays**            | Texte     | Oui         | Nom du pays en français          | Benin                         |
| **code_pays**       | Texte     | Oui         | Code ISO 3166-1 alpha-3          | BEN                           |
| **annee**           | Entier    | Oui         | Année de référence (format YYYY) | 2020                          |
| **indicateur**      | Texte     | Oui         | Nom standardisé de l'indicateur  | PIB par habitant              |
| **valeur**          | Numérique | Oui         | Valeur numérique de la mesure    | 1250.50                       |
| **unite**           | Texte     | Oui         | Unité de mesure                  | USD, %, pour 1000             |
| **categorie**       | Texte     | Oui         | Catégorie thématique             | demographic, economic, social |
| **source_donnees**  | Texte     | Oui         | Organisation source              | World Bank, IMF, WHO          |
| **score_qualite**   | Entier    | Non         | Score de qualité (0-100)         | 85                            |
| **date_collecte**   | Date      | Non         | Date d'extraction (YYYY-MM-DD)   | 2025-01-15                    |
| **fichier_origine** | Texte     | Non         | Nom du fichier source            | worldbank_economic_data.csv   |

### 2.2 Contraintes de Données

- **Années valides:** 2000 à 2024
- **Valeurs manquantes:** Représentées par des cellules vides ou NaN
- **Format des dates:** ISO 8601 (YYYY-MM-DD)
- **Encodage:** UTF-8
- **Séparateur décimal:** Point (.)
- **Séparateur de milliers:** Virgule (,)

---

## 3. GLOSSAIRE DES INDICATEURS {#glossaire-indicateurs}

### 3.1 Indicateurs Démographiques {#indicateurs-demographiques}

#### **Population totale**

- **Définition:** Nombre total d'habitants résidant dans le pays
- **Unité:** Nombre d'habitants
- **Source principale:** World Bank, UN Population Division
- **Fréquence de mise à jour:** Annuelle
- **Méthode de calcul:** Recensement national et estimations inter-censitaires basées sur les taux de natalité, mortalité et migration
- **Utilisation:** Planification des infrastructures, services publics, projections budgétaires
- **Notes importantes:**
  - Inclut résidents permanents et temporaires
  - Exclut les réfugiés non enregistrés
  - Basé sur la définition de facto (présence physique)

#### **Population urbaine**

- **Définition:** Nombre de personnes vivant dans les zones définies comme urbaines selon les critères nationaux
- **Unité:** Nombre d'habitants ou % de la population totale
- **Source principale:** World Bank, UN Habitat
- **Fréquence:** Annuelle
- **Méthode de calcul:** Agrégation des populations des localités classées urbaines
- **Utilisation:** Planification urbaine, services municipaux, infrastructures
- **Notes importantes:**
  - La définition d'une zone urbaine varie selon les pays
  - Au Bénin: généralement localités >10,000 habitants avec certaines caractéristiques économiques

#### **Taux de croissance de la population**

- **Définition:** Variation annuelle en pourcentage de la population totale
- **Unité:** Pourcentage (%)
- **Source principale:** World Bank, UN Population
- **Fréquence:** Annuelle
- **Formule:** `((Population année N - Population année N-1) / Population année N-1) × 100`
- **Utilisation:** Projections démographiques, planification à long terme
- **Notes importantes:**
  - Inclut l'effet des naissances, décès et migration nette
  - Un taux élevé (>2%) indique une croissance rapide
  - Le Bénin a historiquement un taux élevé (~2.7% en moyenne)

#### **Espérance de vie à la naissance**

- **Définition:** Nombre moyen d'années qu'un nouveau-né peut espérer vivre selon les conditions de mortalité actuelles
- **Unité:** Années
- **Source principale:** World Bank, WHO, UN Population
- **Fréquence:** Annuelle
- **Méthode de calcul:** Tables de mortalité basées sur les taux de survie par groupe d'âge
- **Utilisation:** Indicateur clé de santé publique et développement
- **Notes importantes:**
  - Basé sur les conditions de mortalité de l'année de référence
  - Ne prédit pas la durée de vie réelle d'un individu
  - Très sensible à la mortalité infantile

#### **Taux de fécondité total**

- **Définition:** Nombre moyen d'enfants qu'une femme aurait durant sa vie reproductive (15-49 ans)
- **Unité:** Enfants par femme
- **Source principale:** World Bank, UN Population, DHS
- **Fréquence:** Annuelle
- **Méthode de calcul:** Somme des taux de fécondité par âge
- **Utilisation:** Projections démographiques, politiques familiales
- **Notes importantes:**
  - Indicateur synthétique de fécondité (ISF)
  - Taux de remplacement: ~2.1 enfants/femme
  - Le Bénin a un taux élevé (~5-6 enfants/femme)

#### **Densité de population**

- **Définition:** Nombre moyen d'habitants par kilomètre carré de territoire
- **Unité:** Habitants/km²
- **Source principale:** World Bank
- **Fréquence:** Annuelle
- **Formule:** `Population totale / Superficie totale du pays`
- **Utilisation:** Aménagement du territoire, pression sur les ressources
- **Notes importantes:**
  - Basé sur la superficie terrestre totale (112,622 km² pour le Bénin)
  - Distribution non uniforme sur le territoire
  - Zones urbaines beaucoup plus denses que la moyenne nationale

#### **Taux de natalité brut**

- **Définition:** Nombre de naissances vivantes pour 1,000 habitants par an
- **Unité:** Pour 1,000 habitants
- **Source principale:** World Bank, UN
- **Fréquence:** Annuelle
- **Formule:** `(Naissances vivantes / Population totale) × 1,000`
- **Utilisation:** Dynamique démographique, services de santé maternelle
- **Notes importantes:**
  - "Brut" signifie non ajusté par structure d'âge
  - Sensible à la pyramide des âges

#### **Taux de mortalité brut**

- **Définition:** Nombre de décès pour 1,000 habitants par an
- **Unité:** Pour 1,000 habitants
- **Source principale:** World Bank, UN, WHO
- **Fréquence:** Annuelle
- **Formule:** `(Décès totaux / Population totale) × 1,000`
- **Utilisation:** État sanitaire général, planification services funéraires
- **Notes importantes:**
  - Non ajusté par structure d'âge
  - Pays jeunes ont généralement taux plus faibles

#### **Ratio de dépendance**

- **Définition:** Ratio entre population dépendante (0-14 ans et 65+) et population active (15-64 ans)
- **Unité:** Ratio ou pourcentage
- **Source principale:** World Bank, UN
- **Fréquence:** Annuelle
- **Formule:** `((Pop 0-14 + Pop 65+) / Pop 15-64) × 100`
- **Utilisation:** Charge économique, politiques sociales
- **Notes importantes:**
  - Ratio élevé = forte charge de dépendance
  - Le Bénin a un ratio élevé (>80%) dû à population jeune

---

### 3.2 Indicateurs Économiques {#indicateurs-economiques}

#### **PIB (Produit Intérieur Brut)**

- **Définition:** Valeur totale de tous les biens et services produits dans le pays sur une année
- **Unité:** USD courants (nominal) ou USD constants (réel)
- **Source principale:** World Bank, IMF
- **Fréquence:** Trimestrielle/Annuelle
- **Méthode de calcul:** Somme de la valeur ajoutée de tous les secteurs économiques
- **Trois approches:**
  - Production: somme valeurs ajoutées
  - Dépenses: C + I + G + (X - M)
  - Revenus: salaires + profits + taxes
- **Utilisation:** Taille de l'économie, comparaisons internationales
- **Notes importantes:**
  - PIB nominal: en prix courants (affecté par inflation)
  - PIB réel: en prix constants (volume réel)
  - PIB PPA: ajusté pour parité pouvoir d'achat

#### **PIB par habitant**

- **Définition:** PIB divisé par la population totale
- **Unité:** USD par habitant
- **Source principale:** World Bank, IMF
- **Fréquence:** Annuelle
- **Formule:** `PIB total / Population totale`
- **Utilisation:** Indicateur proxy du niveau de vie moyen
- **Notes importantes:**
  - Ne reflète pas la distribution des revenus
  - Utile pour comparaisons internationales
  - Bénin: ~1,200-1,400 USD/habitant (2024)

#### **Taux de croissance du PIB**

- **Définition:** Variation annuelle en pourcentage du PIB réel
- **Unité:** Pourcentage (%)
- **Source principale:** World Bank, IMF
- **Fréquence:** Trimestrielle/Annuelle
- **Formule:** `((PIB réel année N - PIB réel année N-1) / PIB réel année N-1) × 100`
- **Utilisation:** Performance économique, cycles conjoncturels
- **Notes importantes:**
  - Calculé sur PIB réel (volume)
  - Croissance >3% considérée bonne pour pays en développement
  - Bénin: moyenne 4-6% dernières années

#### **Taux d'inflation**

- **Définition:** Variation annuelle en pourcentage du niveau général des prix
- **Unité:** Pourcentage (%)
- **Source principale:** World Bank, IMF, Instituts statistiques nationaux
- **Fréquence:** Mensuelle/Annuelle
- **Méthode de calcul:** Variation de l'Indice des Prix à la Consommation (IPC)
- **Formule:** `((IPC année N - IPC année N-1) / IPC année N-1) × 100`
- **Utilisation:** Politique monétaire, ajustement salaires, pouvoir d'achat
- **Notes importantes:**
  - Basé sur panier de consommation représentatif
  - Bénin: membre zone franc CFA (inflation généralement <3%)
  - Cible UEMOA: <3%

#### **Taux de chômage**

- **Définition:** Pourcentage de la population active sans emploi, disponible et recherchant activement un emploi
- **Unité:** Pourcentage (%)
- **Source principale:** World Bank, ILO (Organisation Internationale du Travail)
- **Fréquence:** Annuelle (enquêtes emploi)
- **Formule:** `(Nombre de chômeurs / Population active) × 100`
- **Définition BIT du chômeur:**
  - Sans emploi durant période de référence
  - Disponible pour travailler
  - Recherche active d'emploi
- **Utilisation:** Santé du marché du travail, politiques d'emploi
- **Notes importantes:**
  - Sous-estime souvent situation réelle (secteur informel)
  - Taux de sous-emploi souvent plus pertinent en Afrique

#### **Dette publique (% du PIB)**

- **Définition:** Dette brute consolidée des administrations publiques en pourcentage du PIB
- **Unité:** Pourcentage du PIB (%)
- **Source principale:** IMF, World Bank
- **Fréquence:** Trimestrielle/Annuelle
- **Formule:** `(Dette publique totale / PIB) × 100`
- **Utilisation:** Soutenabilité fiscale, accès aux marchés financiers
- **Notes importantes:**
  - Inclut dette intérieure et extérieure
  - Seuil critique: généralement >60% pour pays émergents
  - Bénin: ~50-55% (2024)

#### **Investissement Direct Étranger (IDE)**

- **Définition:** Flux nets d'investissements étrangers dans le pays
- **Unité:** USD ou % du PIB
- **Source principale:** World Bank, UNCTAD
- **Fréquence:** Annuelle
- **Méthode de calcul:** IDE entrants - IDE sortants
- **Utilisation:** Attractivité économique, intégration mondiale
- **Notes importantes:**
  - Enregistré dans balance des paiements
  - IDE = investissement >10% capital d'une entreprise
  - Indicateur de confiance des investisseurs

#### **Exportations de biens et services**

- **Définition:** Valeur totale des biens et services vendus à l'étranger
- **Unité:** USD ou % du PIB
- **Source principale:** World Bank, UNCTAD, Douanes
- **Fréquence:** Mensuelle/Annuelle
- **Méthode:** Agrégation valeur douanière + services
- **Utilisation:** Balance commerciale, compétitivité internationale
- **Notes importantes:**
  - En USD courants
  - Principaux exports Bénin: coton, noix cajou, réexportations

#### **Importations de biens et services**

- **Définition:** Valeur totale des biens et services achetés à l'étranger
- **Unité:** USD ou % du PIB
- **Source principale:** World Bank, UNCTAD, Douanes
- **Fréquence:** Mensuelle/Annuelle
- **Utilisation:** Balance commerciale, dépendance extérieure
- **Notes importantes:**
  - Bénin: forte dépendance importations
  - Port de Cotonou: hub régional

#### **Balance commerciale**

- **Définition:** Différence entre exportations et importations
- **Unité:** USD
- **Fréquence:** Mensuelle/Annuelle
- **Formule:** `Exportations - Importations`
- **Interprétation:**
  - Excédent (positif): exporte plus qu'importe
  - Déficit (négatif): importe plus qu'exporte
- **Notes:** Bénin a historiquement un déficit commercial

#### **Taux de pauvreté**

- **Définition:** Pourcentage de la population vivant sous le seuil de pauvreté
- **Unité:** Pourcentage (%)
- **Source principale:** World Bank, Instituts nationaux statistiques
- **Fréquence:** Variable (3-5 ans, selon enquêtes ménages)
- **Seuils de pauvreté:**
  - International: 2.15 USD/jour (PPA 2017)
  - National: défini par chaque pays
- **Utilisation:** Politiques sociales, programmes de réduction pauvreté
- **Notes importantes:**
  - Basé sur enquêtes ménages (QUIBB, EMICoV au Bénin)
  - Mesure multidimensionnelle de plus en plus utilisée

#### **Coefficient de GINI**

- **Définition:** Mesure statistique de l'inégalité de distribution des revenus
- **Unité:** Indice de 0 à 100 (ou 0 à 1)
- **Source principale:** World Bank
- **Fréquence:** Variable (3-5 ans)
- **Méthode de calcul:** Aire entre courbe de Lorenz et ligne d'égalité parfaite
- **Interprétation:**
  - 0 = égalité parfaite (tous même revenu)
  - 100 = inégalité maximale (une personne a tout)
- **Utilisation:** Mesure inégalités, politique redistributive
- **Notes:** Bénin: GINI ~47-50 (inégalités modérées à élevées)

---

### 3.3 Indicateurs Sociaux {#indicateurs-sociaux}

#### **Taux d'alphabétisation des adultes**

- **Définition:** Pourcentage de personnes âgées de 15 ans et plus sachant lire et écrire
- **Unité:** Pourcentage (%)
- **Source principale:** UNESCO, World Bank
- **Fréquence:** Variable (recensements, enquêtes)
- **Méthode:** Auto-déclaration ou tests de compétences
- **Utilisation:** Niveau d'éducation, développement humain
- **Notes importantes:**
  - Définition: comprendre texte court et simple sur vie quotidienne
  - Bénin: ~43% (2024), avec fort écart homme-femme
  - Disparités urbain-rural importantes

#### **Taux de scolarisation primaire**

- **Définition:** Taux brut de scolarisation au niveau primaire
- **Unité:** Pourcentage (%)
- **Source principale:** UNESCO, World Bank
- **Fréquence:** Annuelle
- **Formule:** `(Élèves inscrits au primaire / Population d'âge primaire) × 100`
- **Utilisation:** Accès à l'éducation, OMD/ODD 4
- **Notes importantes:**
  - Taux brut peut dépasser 100% (redoublants, hors-âge)
  - Taux net exclut hors-âge
  - Bénin: taux brut ~120%, net ~90%

#### **Taux de scolarisation secondaire**

- **Définition:** Taux brut de scolarisation au niveau secondaire
- **Unité:** Pourcentage (%)
- **Source principale:** UNESCO, World Bank
- **Fréquence:** Annuelle
- **Formule:** Identique au primaire
- **Utilisation:** Niveau d'éducation, transition primaire-secondaire
- **Notes:** Bénin: ~50-55%, avec écart genre important

#### **Mortalité infantile**

- **Définition:** Nombre de décès d'enfants de moins d'un an pour 1,000 naissances vivantes
- **Unité:** Pour 1,000 naissances vivantes
- **Source principale:** WHO, UNICEF, World Bank, DHS
- **Fréquence:** Annuelle
- **Formule:** `(Décès <1 an / Naissances vivantes) × 1,000`
- **Utilisation:** Santé publique, OMD/ODD 3
- **Notes importantes:**
  - Indicateur clé de développement
  - Bénin: ~55-60 pour 1,000 (2024), en baisse continue
  - Cible ODD: <25 pour 1,000

#### **Mortalité maternelle**

- **Définition:** Nombre de décès maternels pour 100,000 naissances vivantes
- **Unité:** Pour 100,000 naissances vivantes
- **Source principale:** WHO, World Bank, DHS
- **Fréquence:** Annuelle (estimations modélisées)
- **Formule:** `(Décès maternels / Naissances vivantes) × 100,000`
- **Définition décès maternel:** Décès d'une femme pendant grossesse, accouchement ou dans 42 jours après
- **Utilisation:** Santé reproductive, OMD/ODD 3
- **Notes importantes:**
  - Bénin: ~350-400 pour 100,000 (2024)
  - Cible ODD: <70 pour 100,000
  - Principales causes: hémorragies, infections, éclampsie

#### **Accès à l'électricité**

- **Définition:** Pourcentage de la population ayant accès à l'électricité
- **Unité:** Pourcentage (%)
- **Source principale:** World Bank, IEA, SE4ALL
- **Fréquence:** Annuelle
- **Méthode:** Enquêtes ménages
- **Critère d'accès:** Connexion au réseau ou source alternative fiable
- **Utilisation:** Infrastructure, développement économique, ODD 7
- **Notes importantes:**
  - Bénin: ~45-50% (2024)
  - Fort écart urbain (~80%) vs rural (~15%)
  - Accès ≠ qualité/fiabilité du service

#### **Accès à l'eau potable**

- **Définition:** Pourcentage de la population ayant accès à une source d'eau potable améliorée
- **Unité:** Pourcentage (%)
- **Source principale:** WHO, UNICEF (JMP)
- **Fréquence:** Annuelle
- **Sources améliorées:** Eau courante, forage, puits protégé, source protégée
- **Utilisation:** Santé publique, ODD 6
- **Notes importantes:**
  - Bénin: ~75-80% (2024)
  - Accès ne garantit pas qualité/sécurité de l'eau
  - Différence accès de base vs service géré en toute sécurité

#### **Accès à l'assainissement de base**

- **Définition:** Pourcentage population avec accès installation assainissement améliorée
- **Unité:** Pourcentage (%)
- **Source principale:** WHO, UNICEF (JMP)
- **Fréquence:** Annuelle
- **Installations améliorées:** Chasse d'eau, latrine améliorée, toilettes composte
- **Utilisation:** Santé publique, ODD 6
- **Notes:** Bénin: ~20-25%, très faible comparativement

#### **Prévalence VIH (15-49 ans)**

- **Définition:** Pourcentage d'adultes (15-49 ans) vivant avec le VIH
- **Unité:** Pourcentage (%)
- **Source principale:** UNAIDS, WHO
- **Fréquence:** Annuelle (estimations modélisées)
- **Méthode:** Enquêtes séroprévalence + modélisation
- **Utilisation:** Programmes VIH/SIDA, santé publique
- **Notes importantes:**
  - Bénin: ~1.0-1.2% (2024), prévalence modérée
  - Disparités genre et géographiques
  - Tendance stable/légère baisse

#### **Dépenses de santé (% PIB)**

- **Définition:** Dépenses totales de santé en pourcentage du PIB
- **Unité:** Pourcentage du PIB (%)
- **Source principale:** WHO, World Bank
- **Fréquence:** Annuelle
- **Composantes:** Dépenses publiques + privées
- **Utilisation:** Priorités budgétaires, investissement santé
- **Notes:**
  - Bénin: ~3-4% du PIB
  - OMS recommande: minimum 5%
  - Engagement Abuja: 15% budget public

#### **Indice de Développement Humain (IDH)**

- **Définition:** Indice composite mesurant développement humain (santé, éducation, niveau de vie)
- **Unité:** Indice de 0 à 1
- **Source principale:** UNDP
- **Fréquence:** Annuelle
- **Composantes:**
  1. Espérance de vie (santé)
  2. Années de scolarisation (éducation)
  3. RNB par habitant PPA (niveau de vie)
- **Formule:** Moyenne géométrique des 3 indices
- **Catégories:**
  - Très élevé: ≥0.800
  - Élevé: 0.700-0.799
  - Moyen: 0.550-0.699
  - Faible: <0.550
- **Notes importantes:**
  - Bénin: ~0.525 (2024), développement humain faible
  - Rang mondial: ~160-165/191
  - Méthodologie révisée en 2010

#### **Femmes au parlement**

- **Définition:** Pourcentage de sièges parlementaires occupés par des femmes
- **Unité:** Pourcentage (%)
- **Source principale:** IPU (Union Interparlementaire), World Bank
- **Fréquence:** Annuelle (après chaque élection)
- **Méthode:** Comptage direct
- **Utilisation:** Égalité de genre, ODD 5
- **Notes importantes:**
  - Bénin: ~7-8% (2024), très faible
  - Moyenne mondiale: ~26%
  - Chambre basse ou unique

#### **Vaccination DTC (Diphtérie-Tétanos-Coqueluche)**

- **Définition:** Pourcentage d'enfants vaccinés avec 3 doses DTC
- **Unité:** Pourcentage (%)
- **Source principale:** WHO, UNICEF
- **Fréquence:** Annuelle
- **Utilisation:** Couverture vaccinale, santé infantile
- **Notes:** Bénin: ~70-80%, à améliorer pour atteindre immunité collective

---

## 4. SOURCES DE DONNÉES {#sources-donnees}

### 4.1 Sources Principales

#### **World Bank (Banque Mondiale)**

- **Acronyme:** WB
- **Type:** Organisation internationale
- **URL:** https://data.worldbank.org
- **API:** https://api.worldbank.org/v2
- **Couverture:** Mondiale, 217 économies
- **Fréquence mise à jour:** Trimestrielle/Annuelle
- **Domaines:** Démographie, Économie, Social, Environnement
- **Fiabilité:** ★★★★★ (Très élevée)
- **Notes:** Source la plus complète pour données macro-économiques et sociales

#### **International Monetary Fund (FMI)**

- **Acronyme:** IMF
- **Type:** Organisation internationale
- **URL:** https://www.imf.org/en/Data
- **API:** https://www.imf.org/external/datamapper/api/v1
- **Couverture:** Mondiale, 190 pays membres
- **Fréquence:** Trimestrielle
- **Domaines:** Économie, Finances publiques, Balance paiements
- **Fiabilité:** ★★★★★ (Très élevée)
- **Notes:** Référence pour données macro-économiques

#### **United Nations Population Division**

- **Acronyme:** UN Population
- **Type:** Agence ONU
- **URL:** https://population.un.org
- **API:** https://population.un.org/dataportalapi/api/v1
- **Couverture:** Mondiale
- **Fréquence:** Bisannuelle (World Population Prospects)
- **Domaines:** Démographie, Projections population
- **Fiabilité:** ★★★★★ (Très élevée)
- **Notes:** Standard international pour projections démographiques

#### **World Health Organization (OMS)**

- **Acronyme:** WHO
- **Type:** Agence ONU
- **URL:** https://www.who.int/data
- **API:** https://ghoapi.azureedge.net/api
- **Couverture:** Mondiale
- **Fréquence:** Annuelle
- **Domaines:** Santé publique, Maladies, Systèmes santé
- **Fiabilité:** ★★★★★ (Très élevée)
- **Notes:** Autorité mondiale en données de santé

#### **United Nations Development Programme (PNUD)**

- **Acronyme:** UNDP
- **Type:** Agence ONU
- **URL:** https://hdr.undp.org
- **Couverture:** Mondiale
- **Fréquence:** Annuelle (Human Development Report)
- **Domaines:** Développement humain, IDH, Inégalités
- **Fiabilité:** ★★★★★ (Très élevée)
- **Notes:** Producteur officiel de l'IDH

#### **UNESCO Institute for Statistics**

- **Acronyme:** UNESCO
- **Type:** Agence ONU
- **URL:** http://data.uis.unesco.org
- **API:** Disponible
- **Couverture:** Mondiale
- **Fréquence:** Annuelle
- **Domaines:** Éducation, Culture, Science, Alphabétisation
- **Fiabilité:** ★★★★★ (Très élevée)
- **Notes:** Référence mondiale pour statistiques éducation

#### **UNCTAD (Conférence des Nations Unies sur le Commerce et le Développement)**

- **Acronyme:** UNCTAD
- **Type:** Agence ONU
- **URL:** https://unctadstat.unctad.org
- **Couverture:** Mondiale
- **Fréquence:** Annuelle
- **Domaines:** Commerce international, IDE, Développement
- **Fiabilité:** ★★★★☆ (Élevée)
- **Notes:** Spécialisé en commerce et investissement

#### **Demographic and Health Surveys**

- **Acronyme:** DHS
- **Type:** Programme de recherche (USAID)
- **URL:** https://dhsprogram.com
- **Couverture:** Pays en développement
- **Fréquence:** Variable (3-5 ans par pays)
- **Domaines:** Santé, Démographie, Nutrition, Genre
- **Fiabilité:** ★★★★☆ (Élevée)
- **Notes:** Enquêtes approfondies, données détaillées par pays

### 4.2 Critères de Fiabilité des Sources

| Niveau | Description                                                                    | Exemples                                 |
| ------ | ------------------------------------------------------------------------------ | ---------------------------------------- |
| ★★★★★  | Très élevée - Organisations internationales reconnues, méthodologie rigoureuse | World Bank, IMF, UN, WHO                 |
| ★★★★☆  | Élevée - Organisations respectées, bonnes pratiques                            | UNCTAD, Instituts statistiques nationaux |
| ★★★☆☆  | Moyenne - Sources académiques, ONG reconnues                                   | Universités, Think tanks                 |
| ★★☆☆☆  | Modérée - Sources secondaires, données non vérifiées                           | Médias, rapports non officiels           |
| ★☆☆☆☆  | Faible - Sources non vérifiables                                               | Blogs, sources anonymes                  |

---

## 5. MÉTHODOLOGIE DE CALCUL DES SCORES DE QUALITÉ {#methodologie-qualite}

### 5.1 Score de Qualité des Données (0-100)

Le score de qualité est calculé selon plusieurs critères pondérés :

#### **Critères et Pondération**

| Critère              | Poids | Description                             | Évaluation                                            |
| -------------------- | ----- | --------------------------------------- | ----------------------------------------------------- |
| **Complétude**       | 30%   | Toutes valeurs obligatoires renseignées | (Champs remplis / Champs requis) × 100                |
| **Fiabilité source** | 25%   | Crédibilité organisation source         | Très élevée: 100, Élevée: 80, Moyenne: 60, Faible: 40 |
| **Actualité**        | 15%   | Récence de la collecte                  | Score = 100 - (Écart années × 5)                      |
| **Cohérence**        | 15%   | Absence d'anomalies statistiques        | Tests de cohérence temporelle                         |
| **Documentation**    | 10%   | Métadonnées disponibles                 | Présence unités, méthodo, notes                       |
| **Traçabilité**      | 5%    | Lien vers source originale              | Fichier origine documenté                             |

#### **Formule de Calcul**

```
Score_Qualité = (Complétude × 0.30) +
                (Fiabilité_Source × 0.25) +
                (Actualité × 0.15) +
                (Cohérence × 0.15) +
                (Documentation × 0.10) +
                (Traçabilité × 0.05)
```

#### **Interprétation des Scores**

- **90-100:** Excellente qualité - Données fiables pour analyses critiques
- **75-89:** Bonne qualité - Utilisables pour la plupart des analyses
- **60-74:** Qualité acceptable - Utiliser avec précautions
- **40-59:** Qualité faible - Nécessite validation supplémentaire
- **0-39:** Qualité insuffisante - À éviter pour analyses importantes

### 5.2 Flags de Qualité

Des indicateurs qualitatifs peuvent compléter le score :

- 🟢 **VÉRIFIÉ:** Donnée vérifiée par recoupement de sources
- 🟡 **ESTIMÉ:** Donnée estimée ou modélisée
- 🟠 **PARTIEL:** Donnée incomplète ou partielle
- 🔴 **DOUTEUX:** Donnée présentant des incohérences
- ⚪ **NON ÉVALUÉ:** Qualité non encore évaluée

---

## 6. UNITÉS ET FORMATS {#unites-formats}

### 6.1 Unités Standardisées

| Unité              | Description               | Exemple    | Contexte                        |
| ------------------ | ------------------------- | ---------- | ------------------------------- |
| **USD**            | Dollar américain          | 1,250.50   | Valeurs monétaires              |
| **%**              | Pourcentage               | 45.2       | Taux, ratios, proportions       |
| **pour 1000**      | Pour mille habitants      | 25.5       | Taux démographiques             |
| **pour 100000**    | Pour cent mille habitants | 350        | Mortalité maternelle            |
| **années**         | Années                    | 62.5       | Espérance de vie, scolarisation |
| **habitants/km²**  | Densité                   | 105.3      | Densité population              |
| **enfants/femme**  | Fécondité                 | 5.2        | Taux de fécondité               |
| **habitants**      | Nombre absolu             | 13,500,000 | Population totale               |
| **indice (0-1)**   | Indice normalisé          | 0.525      | IDH, indices composites         |
| **indice (0-100)** | Indice sur 100            | 47.5       | GINI, scores                    |

### 6.2 Formats de Données

#### **Dates**

- Format: ISO 8601 (YYYY-MM-DD)
- Exemple: 2024-01-15
- Années: Format YYYY (2024)

#### **Nombres**

- Séparateur décimal: Point (.)
- Exemple: 1250.50
- Séparateur de milliers: Virgule (,) dans affichage
- Exemple: 1,250.50
- Stockage: Sans séparateur de milliers

#### **Texte**

- Encodage: UTF-8
- Casse: Standardisée (Première lettre majuscule)
- Exemple: "Population totale"

#### **Valeurs manquantes**

- CSV: Cellule vide
- Base de données: NULL
- Python/Pandas: NaN
- Ne pas utiliser: 0, "N/A", "-", "."

---

## 7. NOTES D'UTILISATION {#notes-utilisation}

### 7.1 Bonnes Pratiques

#### **Avant Utilisation**

1. ✅ Vérifier le score de qualité (>75 recommandé)
2. ✅ Consulter les métadonnées et notes
3. ✅ Vérifier la cohérence temporelle
4. ✅ Comparer avec sources alternatives si disponibles
5. ✅ Documenter les sources utilisées

#### **Lors de l'Analyse**

1. ✅ Tenir compte des unités et conversions
2. ✅ Considérer les marges d'erreur
3. ✅ Éviter comparaisons directes entre indicateurs différents
4. ✅ Contextualiser les résultats (historique, géographie)
5. ✅ Croiser plusieurs indicateurs pour vision complète

#### **Lors de la Restitution**

1. ✅ Citer systématiquement les sources
2. ✅ Indiquer les années de référence
3. ✅ Mentionner les limites méthodologiques
4. ✅ Distinguer données réelles vs estimations
5. ✅ Fournir contexte d'interprétation

### 7.2 Limites et Précautions

#### **Limites Générales**

- Les données peuvent contenir des erreurs de mesure
- Les méthodologies varient entre sources
- Les définitions peuvent changer dans le temps
- Certains indicateurs sont modélisés/estimés
- La fréquence de mise à jour varie selon les sources

#### **Limites Spécifiques au Bénin**

- **Système statistique:** En développement, capacités limitées
- **Recensements:** Dernier en 2013, prochain prévu 2023-2024
- **Enquêtes:** Fréquence irrégulière, lacunes temporelles
- **Secteur informel:** Difficile à mesurer (70%+ emplois)
- **Zones rurales:** Sous-représentées dans certaines enquêtes

#### **Précautions d'Interprétation**

- ⚠️ Ne pas sur-interpréter variations annuelles mineures
- ⚠️ Considérer marges d'erreur (enquêtes échantillons)
- ⚠️ Attention aux ruptures de séries (changements méthodologiques)
- ⚠️ PIB et revenus: écart réalité/statistiques (informel)
- ⚠️ Indicateurs sociaux: souvent basés sur auto-déclaration

### 7.3 Recommandations par Type d'Analyse

#### **Analyses de Tendances (Séries Temporelles)**

- Utiliser au minimum 5 ans de données
- Vérifier absence ruptures méthodologiques
- Privilégier source unique pour cohérence
- Appliquer lissage si volatilité élevée
- Contextualiser avec événements majeurs

#### **Comparaisons Internationales**

- Utiliser indicateurs standardisés (World Bank, UN)
- Ajuster pour PPA si comparaisons revenus
- Comparer pays similaires (niveau développement, région)
- Considérer différences structurelles
- Citer année exacte de comparaison

#### **Analyses d'Impact (Causalité)**

- Croiser plusieurs sources/indicateurs
- Vérifier ordre temporel (cause avant effet)
- Contrôler pour facteurs confondants
- Utiliser méthodes statistiques appropriées
- Rester prudent sur causalité (corrélation ≠ causalité)

#### **Projections et Scénarios**

- Baser sur tendances historiques solides
- Expliciter hypothèses clairement
- Fournir intervalles de confiance
- Présenter plusieurs scénarios (optimiste/pessimiste)
- Réviser régulièrement avec nouvelles données

### 7.4 Traçabilité et Reproductibilité

Toute analyse doit pouvoir être reproduite. Pour chaque analyse, documenter :

1. **Sources exactes**

   - Nom organisation
   - URL précise
   - Date de téléchargement
   - Version dataset si applicable

2. **Transformations appliquées**

   - Nettoyage (valeurs aberrantes supprimées)
   - Calculs dérivés (formules)
   - Agrégations (méthodes)
   - Interpolations/extrapolations

3. **Logiciels et versions**

   - Python 3.x, Pandas x.x
   - R version x.x
   - Excel/Power BI version

4. **Scripts et code**
   - Code source complet
   - Commentaires explicatifs
   - Paramètres configurables

---

## 8. GESTION DES VERSIONS

### Historique des Versions

| Version | Date       | Auteur      | Modifications                     |
| ------- | ---------- | ----------- | --------------------------------- |
| 1.0     | 2025-10-05 | Équipe ANIP | Création initiale du dictionnaire |
|         |            |             | - Structure complète              |
|         |            |             | - 50+ indicateurs documentés      |
|         |            |             | - 8 sources principales           |

### Mises à Jour Futures

Ce dictionnaire sera mis à jour :

- **Trimestriellement:** Ajout nouveaux indicateurs collectés
- **Annuellement:** Révision définitions et méthodologies
- **Ad-hoc:** Corrections et améliorations

---

## 9. CONTACT ET SUPPORT

### Pour Questions ou Suggestions

**Équipe Technique ANIP**

- Email: data@anip.bj
- Tél: +229 XX XX XX XX

**Pour Signaler des Erreurs**

- Utiliser le formulaire: [lien formulaire]
- Ou email: data-quality@anip.bj

### Ressources Complémentaires

- **Guide d'utilisation Power BI:** [lien]
- **Tutoriels d'analyse:** [lien]
- **Forum communauté:** [lien]
- **Documentation technique complète:** [lien]

---

## 10. ANNEXES

### Annexe A: Abréviations et Acronymes

| Acronyme | Signification Française                           | Signification Anglaise         |
| -------- | ------------------------------------------------- | ------------------------------ |
| ANIP     | Agence Nationale d'Identification des Personnes   | -                              |
| BEN      | Bénin                                             | Benin                          |
| BIT      | Bureau International du Travail                   | ILO                            |
| DHS      | Enquêtes Démographiques et de Santé               | Demographic and Health Surveys |
| FMI      | Fonds Monétaire International                     | IMF                            |
| IDE      | Investissement Direct Étranger                    | FDI                            |
| IDH      | Indice de Développement Humain                    | HDI                            |
| IMF      | -                                                 | International Monetary Fund    |
| IPC      | Indice des Prix à la Consommation                 | CPI                            |
| ISF      | Indice Synthétique de Fécondité                   | TFR                            |
| ODD      | Objectifs de Développement Durable                | SDG                            |
| OMD      | Objectifs du Millénaire pour le Développement     | MDG                            |
| OMS      | Organisation Mondiale de la Santé                 | WHO                            |
| ONG      | Organisation Non Gouvernementale                  | NGO                            |
| ONU      | Organisation des Nations Unies                    | UN                             |
| PIB      | Produit Intérieur Brut                            | GDP                            |
| PNUD     | Programme des Nations Unies pour le Développement | UNDP                           |
| PPA      | Parité de Pouvoir d'Achat                         | PPP                            |
| RNB      | Revenu National Brut                              | GNI                            |
| UEMOA    | Union Économique et Monétaire Ouest-Africaine     | WAEMU                          |
| UNESCO   | Organisation des Nations Unies pour l'Éducation   | UNESCO                         |
| UNICEF   | Fonds des Nations Unies pour l'Enfance            | UNICEF                         |
| VIH/SIDA | Virus de l'Immunodéficience Humaine               | HIV/AIDS                       |
| WHO      | -                                                 | World Health Organization      |

### Annexe B: Formules Mathématiques Principales

#### **Taux de Croissance**

```
Taux = ((Valeur_N - Valeur_N-1) / Valeur_N-1) × 100
```

#### **Taux de Variation Annuel Moyen (TAAM)**

```
TAAM = ((Valeur_finale / Valeur_initiale)^(1/nombre_années) - 1) × 100
```

#### **Indice Simple (base 100)**

```
Indice_N = (Valeur_N / Valeur_base) × 100
```

#### **Moyenne Mobile (3 périodes)**

```
MM_t = (Valeur_t-1 + Valeur_t + Valeur_t+1) / 3
```

#### **Coefficient de Variation**

```
CV = (Écart-type / Moyenne) × 100
```

### Annexe C: Conversion d'Unités Courantes

| De          | Vers          | Formule                   |
| ----------- | ------------- | ------------------------- |
| %           | Décimal       | Diviser par 100           |
| Pour 1000   | %             | Diviser par 10            |
| Pour 100000 | Pour 1000     | Multiplier par 0.01       |
| USD nominal | USD réel      | Diviser par déflateur PIB |
| Population  | Millions hab. | Diviser par 1,000,000     |

### Annexe D: Références Bibliographiques

1. **UNDP.** (2023). Human Development Report 2023/2024. New York: UNDP.

2. **World Bank.** (2024). World Development Indicators 2024. Washington, DC: World Bank.

3. **UN DESA.** (2024). World Population Prospects 2024. New York: United Nations.

4. **WHO.** (2024). World Health Statistics 2024. Geneva: WHO.

5. **IMF.** (2024). World Economic Outlook Database, October 2024. Washington, DC: IMF.

6. **INSAE Bénin.** (2023). Annuaire Statistique 2023. Cotonou: INSAE.

7. **UNESCO.** (2024). Education for All Global Monitoring Report. Paris: UNESCO.

---

## LICENCE ET UTILISATION

### Droits d'Utilisation

Ce dictionnaire et les données associées sont fournis sous licence **Creative Commons BY 4.0**.

Vous êtes libre de :

- ✅ **Partager** — copier, distribuer et communiquer le matériel
- ✅ **Adapter** — remixer, transformer et créer à partir du matériel
- ✅ **Utiliser** à des fins commerciales ou non

Sous les conditions suivantes :

- ✅ **Attribution** — Citer l'ANIP et les sources originales
- ✅ **Partager dans les mêmes conditions** si modifications

### Citation Recommandée

```
ANIP (2025). Dictionnaire des Variables et Glossaire -
Données Multisources Bénin 2000-2024. Version 1.0.
Agence Nationale d'Identification des Personnes, Bénin.
```

---

**FIN DU DOCUMENT**

_Dernière mise à jour: 05 Octobre 2025_  
_Version: 1.0_  
_Pages: [Auto-généré]_

---

**Pour la version PDF ou DOCX de ce document, veuillez consulter:**

- 📄 Format PDF: `documentation/Dictionnaire_Variables_ANIP.pdf`
- 📝 Format DOCX: `documentation/Dictionnaire_Variables_ANIP.docx`
- 📊 Format CSV (tableaux): `documentation/*.csv`
