# Convertisseur YouTube/SoundCloud vers MP3

Une application web qui permet de convertir des vidéos YouTube, SoundCloud et autres en fichiers MP3.

## Fonctionnalités

- Téléchargement de vidéos depuis YouTube, SoundCloud et autres plateformes
- Support des playlists
- Import des liens via fichier texte (un lien par ligne)
- Conversion automatique en MP3
- Suppression automatique des fichiers vidéo après conversion

## Installation

1. Assurez-vous d'avoir Python 3.8 ou supérieur installé sur votre système.

2. Clonez ce dépôt :
```bash
git clone [url-du-repo]
cd youtube_mp3
```

3. Installez les dépendances :
```bash
pip3 install -r requirements.txt
```

## Utilisation

1. Lancez l'application :
```bash
python3 app.py
```

2. Ouvrez votre navigateur et accédez à :
```
http://localhost:5000
```

3. Dans l'interface web :
   - Importez un fichier texte contenant vos liens (un par ligne)
   - Cliquez sur "Télécharger"
   - Une fois le téléchargement terminé, cliquez sur "Convertir en MP3"

4. Les fichiers MP3 seront sauvegardés dans le dossier `downloads` du projet.

## Format du fichier de liens

Le fichier texte doit contenir un lien par ligne, par exemple :
```
https://www.youtube.com/watch?v=example1
https://soundcloud.com/artist/example2
https://www.youtube.com/playlist?list=example3
```

## Technologies utilisées

- Backend : Python/Flask
- Frontend : HTML, CSS, JavaScript
- Bibliothèques :
  - yt-dlp : Téléchargement des vidéos
  - moviepy : Conversion en MP3

## Notes

- Les fichiers vidéo sont automatiquement supprimés après la conversion en MP3
- Les noms de fichiers sont automatiquement nettoyés pour éviter les caractères invalides
- Les fichiers MP3 sont sauvegardés dans le dossier `downloads` du projet
