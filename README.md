# EmuHub

EmuHub est un hub local Python/PySide6 pour organiser et lancer des jeux avec
leurs émulateurs.

## Démarrage

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Les dépendances sont listées dans [requirements.txt](requirements.txt).

## Catalogue JSON

Le catalogue se trouve dans [data/library.json](data/library.json). Les chemins
sont relatifs à la racine du projet :

```json
{
  "emulators": [
    {
      "id": "mgba",
      "name": "mGBA",
      "platform": "GBA",
      "executable": "emu/GBA/mgba.exe",
      "arguments": []
    }
  ],
  "games": [
    {
      "id": "pokemon-fire-red",
      "name": "Pokemon FireRed",
      "platform": "GBA",
      "rom": "game/GBA/Pokemon Fire Red.gba",
      "emulator_id": "mgba"
    }
  ]
}
```

Les dossiers `emu/` et `game/` restent locaux et leur contenu est exclu du
dépôt Git. Seuls les métadonnées et le code du hub sont versionnés.
