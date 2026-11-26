# Léo & le Prof

**Chaîne YouTube :** https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw

## Mission
Créer un YouTube Short éducatif par jour en français, avec deux avatars noirs récurrents côte à côte : Léo pose **trois questions scientifiques ou de culture générale successives**, le Prof répond à chacune simplement et avec rigueur.

## Objectif de production
- **1 seul Short par jour contenant 3 questions et 3 réponses**, publication à 18 h, fuseau `America/Toronto`.
- Niveau : débutant, intermédiaire et expert.
- Domaines : astronomie, sciences et nature, corps humain, géographie, histoire, inventions, culture générale, technologie et IA.
- Format : vertical 9:16 ; durée cible 45 à 90 secondes selon le rythme et la clarté des réponses. Léo à gauche et le Prof à droite, visibles ensemble, tournés l'un vers l'autre (face à face).
- Aucune installation sur le PC de l'utilisateur.
- Budget cible : 0 $ CA/mois, sous réserve des quotas cloud.

## Architecture envisagée
GitHub Actions → sélection de 3 questions différentes vérifiées → création de 3 échanges question/réponse → synthèse vocale → affichage simultané de Léo (gauche) et du Prof (droite) → montage et sous-titres en un seul Short → contrôle qualité → téléversement via YouTube Data API → publication à 18 h.

## État
- [x] Chaîne YouTube créée
- [x] Logo et bannière préparés
- [x] Dépôt GitHub connecté
- [ ] Moteur de génération des vidéos développé
- [ ] Avatars 2D animables finalisés
- [ ] Premier Short pilote testé
- [ ] Autorisations YouTube OAuth mises en place
- [ ] Workflow quotidien activé

## Sécurité et qualité
Ne jamais ajouter de mot de passe, de jeton OAuth ni de clé API dans ce dépôt public. Conserver les secrets uniquement dans GitHub Actions Secrets. Ne publier que les vidéos passées par des contrôles automatiques; en cas de doute factuel, utiliser un sujet prévalidé.

> Ce dépôt est en préparation : aucune publication automatique n'est encore active.

## Spécification validée du format
- Une seule publication quotidienne, jamais trois Shorts distincts.
- Une vidéo = trois séquences : question 1/réponse 1 ; question 2/réponse 2 ; question 3/réponse 3.
- Deux avatars noirs face à face dans le même décor : Léo à gauche regarde vers la droite, le Prof à droite regarde vers la gauche ; mise en évidence de celui qui parle.
- Conserver les voix françaises jugées satisfaisantes ; améliorer l'animation, la synchronisation et le montage.
- La version Studio V2 actuelle est un prototype à une seule question : **elle doit être adaptée et testée avant toute mise en ligne.**

## État de l'intégration SadTalker (26 novembre 2026)
- La vérification de l'accès à l'API d'un Space Hugging Face a réussi (workflow de contrôle uniquement).
- **Aucune vidéo animée par SadTalker n'a encore été rendue**. Une connexion réussie ne valide ni le fonctionnement de l'endpoint de rendu, ni le quota GPU, ni les gestes.
- Le connecteur actuel est expérimental : les arguments de génération doivent être alignés sur l'API effective du Space avant un appel réel.
- La publication YouTube reste inactive. Le test de rendu nécessitera les portraits de Léo et du Prof ainsi que les pistes vocales de Studio V2.

## Pilote 3 questions : version 2D (26 novembre 2026)
- Nouveau moteur `pilot_3_questions.py` : 3 questions distinctes, 6 scènes et 2 personnages visibles ensemble.
- Les voix sont synthétisées avec `edge-tts` (Léo : EloiseNeural ; Prof : HenriNeural).
- Animation labiale **approximative** fondée sur l'amplitude audio, plus gestes de bras simples ; ce n'est pas une synchronisation phonétique et ce ne sont pas encore les portraits officiels.
- Workflow GitHub Actions manuel **« Pilote 3 questions - animation 2D (sans publication) »** dans `.github/workflows/pilot-3-questions.yml`.
- À exécuter dans GitHub Actions via **Run workflow** ; résultat attendu dans les artifacts `leo-prof-3-questions-pilote`. L'exécution et la qualité réelle du MP4 n'ont pas encore été vérifiées.
- **Aucune publication YouTube**, aucun déclencheur quotidien actif : obtenir l'accord sur le rendu avant d'automatiser la diffusion.

## Pilote statique validé localement (26 novembre 2026)
- Un MP4 local de 30,44 secondes a été créé avec les portraits originaux de Léo (chandail bleu) et du Prof (blouse blanche). Il conserve la bande-son du précédent pilote 3 questions.
- **Ce MP4 n'est pas encore intégré aux GitHub Actions** : les deux PNG originaux doivent être ajoutés à `assets/avatars/leo.png` et `assets/avatars/prof.png` et le moteur de rendu statique doit remplacer le moteur 2D expérimental.
- Ne pas publier automatiquement avant vérification du son, de la correspondance paroles / textes et approbation du pilote.

## Décision éditoriale confirmée (26 novembre 2026)
- **Présentation officielle approuvée** : portraits originaux fixes de Léo (hoodie bleu) et du Prof (cheveux gris, lunettes, blouse blanche), côte à côte, palette bleue, halo de l'intervenant, texte de dialogue et 3 questions/réponses dans un Short.
- **Audio du pilote de 30 secondes refusé** : son de l'ancienne démonstration jugé insuffisant. **Ne pas réutiliser cette bande-son pour publier.**
- Nouveau moteur `studio_officiel_statique.py` : synthèse vocale Edge TTS, voix distinctes `fr-FR-EloiseNeural` (Léo) et `fr-FR-HenriNeural` (Prof), débit plus posé pour le Prof, aucun remplacement robotique en cas d'échec.
- Workflow de vérification manuel : `.github/workflows/studio-officiel-statique.yml`, sans publication.
- Portraits `assets/avatars/leo.png` et `assets/avatars/prof.png` visibles dans GitHub sur la capture utilisateur ; lancer le workflow et écouter le MP4 avant toute autorisation de publication.

## Nouvelle orientation éditoriale — culture scientifique générale (26 novembre 2026)
- Décision de l'éditeur : élargir la chaîne au-delà de la technologie et de l'IA vers **toutes les questions scientifiques et de culture générale**.
- Rubriques : Espace & astronomie ; Sciences & nature ; Corps humain & santé (information générale, sans conseil médical) ; Géographie & planète ; Histoire & découvertes ; Technologie & IA ; Culture générale.
- **Nom définitif approuvé : Léo & le Prof**. Le nom du dépôt GitHub et l'identifiant technique de la chaîne YouTube peuvent rester inchangés ; le nom public de la chaîne doit être modifié séparément sur YouTube.
- Format maintenu : 1 Short = 3 questions-réponses, portraits officiels fixes côte à côte, voix françaises naturelles, réponses sourcées, aucune publication sans validation de la qualité.
- Varier les thèmes dans la semaine sans promettre de publication de contenus non vérifiés. Chaque question doit avoir une référence fiable ; éviter les affirmations sensationnalistes trompeuses.

## Identité de marque définitive — 26 novembre 2026
- **Nom public choisi : Léo & le Prof** (sans « Tech »).
- Promesse : « Trois questions. Trois réponses. Une découverte à chaque vidéo. »
- Univers : science, découvertes et culture générale accessibles à tous, sans prétendre que toutes les réponses ont le même degré de certitude.
- Style audiovisuel validé : les deux portraits fixes officiels, fond bleu, halo de l'orateur, trois échanges, voix françaises naturelles. La bande son du vieux pilote a été rejetée et ne doit pas être publiée.
- Le moteur principal `studio_officiel_statique.py` et le workflow `studio-officiel-statique.yml` produisent désormais `Leo_et_le_Prof_Officiel_Voix_Naturelles.mp4`.
- Le catalogue `questions.json` comprend désormais 12 questions réparties entre informatique, astronomie, nature, géographie, corps humain, histoire et culture générale.
- La chaîne YouTube doit encore être renommée dans YouTube Studio : aucune modification des paramètres de compte YouTube n'a été réalisée par le dépôt GitHub.
- Statut : aucun nouveau Short approuvé/publié automatiquement. Validation audio du prochain MP4 requise avant activation de la publication.

## Validation utilisateur du pilote — 26 novembre 2026
- L'utilisateur confirme que **la vidéo produite est correcte** après le renommage « Léo & le Prof ».
- Conserver ce rendu comme **référence de présentation validée** : deux avatars officiels fixes, format vertical, 3 questions-réponses, identité bleue, voix françaises de la version testée.
- Avant publication automatique : vérifier l'authentification YouTube, la conformité éditoriale, le caractère inédit et la bonne attribution des sources ; aucune autorisation de publication automatique n'est encore configurée ni confirmée.

## Appel à l'abonnement (version 1 approuvée)
- À la fin de chaque Short, après la troisième réponse, **le Prof** prononce : « Chaque jour, une nouvelle découverte pour mieux comprendre le monde ! Abonne-toi à Léo & le Prof pour apprendre quelque chose d'utile chaque jour. »
- Carte finale aux couleurs de la chaîne avec l'indication visuelle **S'ABONNER**.
- Intégré au générateur principal `studio_officiel_statique.py` ; **rendu vidéo de cette nouvelle version non encore vérifié**. Le workflow de test reste manuel et ne publie pas sur YouTube.

## Lien d'abonnement officiel (demande validée)
- URL de la chaîne : https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw
- URL d'abonnement : https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw?sub_confirmation=1
- Le générateur du Short ajoute cette URL à `metadata.json` et `youtube_description.txt` **pour chaque vidéo**, ainsi qu'une indication visuelle de la chaîne à la fin du Short.
- Le Prof prononce toujours l'appel à l'abonnement approuvé, et le bouton graphique « S'ABONNER » apparaît.
- **Attention** : le lien imprimé dans l'image d'une vidéo n'est pas interactif ; les URL placées dans les descriptions et commentaires des Shorts ne sont généralement pas cliquables. Il faut aussi inviter les spectateurs à ouvrir le profil de la chaîne et à toucher le bouton d'abonnement.
- Le workflow reste manuel et aucune vidéo n'est encore publiée automatiquement.

## Validation utilisateur des éléments audiovisuels — 26 novembre 2026
- **Voix des personnages approuvées** : conserver les voix actuellement validées dans le Studio officiel.
- **Portraits/avatars approuvés** : garder strictement `assets/avatars/leo.png` et `assets/avatars/prof.png` ; ne pas remplacer leurs visages ni leurs tenues.
- La carte d'abonnement a été corrigée dans le code pour supprimer l'URL visuellement superposée ; un rendu de validation reste à lancer pour contrôler la nouvelle carte finale.
- Priorité suivante : publier un premier Short validé manuellement, puis préparer et tester l'intégration YouTube sans déclencher de publication automatique prématurée.
