<div align="center">

<img src="assets/logo-scubanion.svg" alt="Logo animé Scubanion : la mascotte flotte, les lettres tombent une à une" width="100%">

<img src="assets/banniere.svg" alt="Animation : un joueur marche, son compteur de pas monte et son compagnon grandit, puis il approche son téléphone d'une borne qui lui débloque un chapeau exclusif au lieu" width="100%">

<sub><i>Le parcours complet, en quinze secondes : on marche, le compagnon grandit, on croise une borne, on repart avec un objet qu'on ne peut obtenir qu'en y étant allé.</i></sub>

<br><br>

![Android](https://img.shields.io/badge/Android-Nuxt%204%20%2B%20Capacitor-3DDC84?logo=android&logoColor=white)
![Laravel](https://img.shields.io/badge/API-Laravel%2013-FF2D20?logo=laravel&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-11.4-003545?logo=mariadb&logoColor=white)
![MQTT](https://img.shields.io/badge/Bornes-MQTT-660066?logo=eclipsemosquitto&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose%20%2B%20multi--stage-2496ED?logo=docker&logoColor=white)
![GitLab CI](https://img.shields.io/badge/CI-GitLab%20%2B%20SonarQube-FC6D26?logo=gitlab&logoColor=white)

<br>

<img src="assets/chiffres.svg" alt="Compteurs animés : 18 exigences Must, 206 tests côté serveur, 28 PR fusionnées, 9 entretiens terrain" width="100%">

</div>

---

## 🐋 Le problème

> **Comment réadapter l'homme à son environnement ?**

C'est le sujet imposé de notre SAE. Nous l'avons resserré sur deux maux qui se nourrissent l'un l'autre chez les 18-30 ans urbains : **la sédentarité** et **l'isolement social**.

<table>
<tr>
<td width="50%" valign="top">

### 📉 Ce qui existe déjà
Les applications de santé **mesurent et affichent**. Elles produisent des courbes que personne ne regarde, et l'abandon arrive en quelques semaines. Rien n'attache.

</td>
<td width="50%" valign="top">

### 📱 Et ce qui aggrave
Les réseaux sociaux **remplacent la rencontre** au lieu de la provoquer. On a mille contacts et personne à qui proposer un café à dix minutes de chez soi.

</td>
</tr>
</table>

## 🎯 Notre pari

Un **attachement affectif** fait ce qu'un graphique de pas ne fera jamais. Scubanion est un compagnon virtuel dont la santé dépend entièrement de votre activité réelle : il ne grandit que si vous sortez, et il dépérit si vous restez chez vous.

Et surtout, **l'objet connecté doit envoyer dehors** plutôt que retenir devant l'écran. C'est pour ça que notre seul matériel n'est pas un bracelet de plus : c'est une **borne**, posée dans un musée, un parc ou un restaurant, qui récompense le fait de s'être déplacé jusqu'à elle.

<div align="center">
<img src="assets/boucle.svg" alt="Diagramme animé : marcher fait grandir le compagnon, qui envoie vers une quête, puis vers une borne, qui débloque un objet exclusif, ce qui redonne envie de marcher" width="100%">
</div>

## 📱 L'application

<div align="center">
<img src="assets/app-carrousel.svg" alt="Carrousel animé des écrans de l'application : accueil, quêtes, carte, amis, profil" width="100%">
</div>

Le téléphone compte les pas tout seul, en fond. L'application s'ouvre **quelques secondes par jour** : le vrai moment de produit, c'est le passage en borne.

## 🗿 La borne

<div align="center">
<img src="assets/borne.svg" alt="Schéma animé de la borne : écran, anneau de LED, lecteur NFC, microcontrôleur, chacun annoté à son tour" width="100%">
</div>

### 🔁 Un pivot assumé

Le projet devait lire les pas sur un **bracelet Mi Band 3** en Bluetooth. L'authentification propriétaire du bracelet s'est révélée être un risque lourd sur le chemin critique, pour un bénéfice nul : **un téléphone compte déjà les pas**.

Nous avons donc tout basculé sur le capteur du téléphone, et **concentré l'IoT sur la borne**. Un objet fait à fond plutôt que deux à moitié, et plus rien à acheter pour le joueur.

## 🧩 La chaîne technique

```mermaid
flowchart LR
    T["📱 Application Android<br/>podomètre · quêtes · carte"] -->|HTTPS| S["🖥️ Serveur<br/>règles du jeu · anti-triche"]
    B["🗿 Borne IoT<br/>NFC · écran · LED"] -->|MQTT| S
    S -->|MQTT| B
    S --> T
```

| Brique | Ce qu'elle fait | Stack |
|---|---|---|
| 📱 **Application** | Compte les pas avec le capteur du téléphone, affiche le compagnon, les quêtes géolocalisées, la carte, les amis et les rencontres | Nuxt 4, Vue 3, TypeScript, Capacitor 8 |
| 🖥️ **Serveur** | **Toutes** les règles du jeu : XP, niveaux, validation des quêtes et des passages, garde-fous anti-triche. Abonné MQTT des bornes | Laravel 13, PHP 8.4, MariaDB 11.4 |
| 🗿 **Borne** | Le seul objet que nous concevons : lit le téléphone en NFC, publie le passage, affiche la récompense | Microcontrôleur, lecteur NFC, écran, MQTT |

Rien n'est calculé sur le téléphone. **Un client ment toujours** : les pas sont plafonnés par heure et recoupés avec la position, les quêtes et les passages sont validés côté serveur.

## 💶 Qui paie, et pourquoi

L'application est gratuite et le restera : elle construit l'audience. Ce que nous vendons, c'est **du passage vérifié** : un visiteur présent, pas une impression publicitaire.

| Offre | Prix | Qui paie, et pourquoi |
|---|---:|---|
| Cosmétiques | **1,99 €** | Le joueur attaché à son compagnon. **L'XP ne s'achète jamais.** |
| Abonnement par borne | **49 €/mois** | Le lieu, pour du flux mesurable et une animation clé en main |
| Quête sponsorisée | **300 € + 0,50 €**<br>par passage | Le commerce, parce qu'il ne paie une partie qu'au visiteur effectivement venu |
| Parcours de découverte | **3 000 – 8 000 €** | La collectivité, sur budget sport, santé ou tourisme |
| Programme bien-être | **3 €/mois**<br>par bénéficiaire | L'employeur ou la mutuelle, sur un budget prévention existant |

Pas de publicité, pas de revente de données, pas d'XP achetable. Ce sont trois promesses tenables, et c'est ce qui nous rend vendables à une collectivité.

## 🔬 Des chiffres, pas des impressions

Le prix d'un accessoire n'a pas été décidé en réunion. Nous avons appliqué la **méthode Toolbox Persona** : neuf personnes interrogées individuellement, une échelle de dix prix, deux questions, puis lecture de la zone de chevauchement.

| Ce qu'on a mesuré | Résultat |
|---|---:|
| Personnes interrogées, dont 8 dans la cible | **9** |
| Zone où tout le monde est d'accord | **0,99 € – 1,49 €** |
| Prix retenu, et pourquoi il sort d'un cran | **1,99 €** |
| Au-delà de 4,99 €, personne ne suit | **0 / 8** |

Deux enseignements qu'on ne cherchait pas : **deux personnes sur neuf ne connaissaient pas leur nombre de pas**, le capteur n'étant pas activé sur leur téléphone. Notre promesse repose dessus : l'activation doit devenir une étape guidée. Et la question du prix plancher s'applique mal à un objet purement décoratif, ce qu'un des interrogés nous a fait remarquer à juste titre.

## 🗺️ Où on en est

<div align="center">
<img src="assets/feuille-de-route.svg" alt="Feuille de route animée : cadrage terminé, jalon zéro en cours, puis soutenance, pilote sur 10 lieux et lancement commercial" width="100%">
</div>

Le point dur est matériel : **la borne n'est pas encore montée**, et elle porte 6 exigences sur 18. C'est écrit noir sur blanc dans notre charte de projet, avec le plan pour la rattraper. Un projet qui cache ses retards ne les rattrape pas.

## 🛠️ Comment on travaille

- **Une branche par tâche**, une PR, et **aucune fusion sans relecture** d'un autre membre.
- **Conventional Commits en français**, parce que l'historique se lit plus souvent qu'il ne s'écrit.
- **Le cahier des charges est la liste de suivi** : 32 exigences numérotées et priorisées *Must / Should / Could*, qu'on coche au fil de l'eau. Chaque décision technique y est reportée avec sa justification.
- **Un point de 30 minutes chaque vendredi** : relevé des indicateurs, tour de table, une décision. Une action non terminée est reportée **avec sa cause écrite**, jamais effacée.
- **Git est noté individuellement**, donc l'équilibre des contributions est un indicateur suivi, et il est publiquement hors cible en ce moment.

## 👥 L'équipe

<div align="center">

<a href="https://github.com/Picsou06"><img src="assets/equipe-Picsou06.svg" alt="Evan Dalmasso, application mobile" width="24%"></a>
<a href="https://github.com/CodeByHaamza"><img src="assets/equipe-CodeByHaamza.svg" alt="Hamza Karrouchi, back-end et données" width="24%"></a>
<a href="https://github.com/Tiretinium"><img src="assets/equipe-Tiretinium.svg" alt="Thomas Bandieras, CI/CD et infrastructure" width="24%"></a>
<a href="https://github.com/shalee-pnt"><img src="assets/equipe-shalee-pnt.svg" alt="Shaleena Lesueur, borne IoT" width="24%"></a>

<sub>SAE BUT 3 Informatique · R5.01 management · R5.04 IoT · R5.07 CI/CD · R5.13 économie durable · 2026–2027</sub>

</div>

## 📦 Dépôts

| Dépôt | Contenu |
|---|---|
| [**scubanion**](https://github.com/Scubatana/scubanion) | L'application, l'API, la borne, l'infrastructure, ainsi que toute la documentation du projet dans `docs/` |
| [**.github**](https://github.com/Scubatana/.github) | Cette page, et les scripts qui dessinent ses animations |

```bash
git clone https://github.com/Scubatana/scubanion.git
cd scubanion
cp .env.exemple .env
docker compose -f dev-docker-compose.yml up -d mariadb phpmyadmin
```

<div align="center">
<br>
<sub>Un compagnon qui vous attend à l'intérieur n'a aucun intérêt. 🐋</sub>
</div>
