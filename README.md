# gallery.kado-ber.de

Eine moderne, reaktionsschnelle Galerie für KI-generierte Bilder – umgesetzt mit **React**, **TypeScript**, **TailwindCSS** und einer JSON-basierten Bilddatenstruktur.  
Ziel ist eine visuelle Präsentation ausgewählter Bilder mit Fokus auf Ästhetik, Übersichtlichkeit und optionaler Kontaktmöglichkeit.

## ✨ Funktionen

- 🖼️ Dynamische Bilderverwaltung über `images.json`
- 🧭 Pagination für große Bildmengen
- 🏷️ Filterung nach Kategorien und Tags
- 🔍 Lightbox mit Tastatur- und Buttonnavigation
- 📩 Kontaktfunktion zur Bildanfrage via E-Mail
- 🌙 Responsive Design für Desktop und Mobilgeräte

## 📁 Projektstruktur

```
public/
  images/               # Galerie-Bilder (JPG)
  data/images.json      # Bildmetadaten (alt, category, tags)

src/
  App.tsx               # Hauptkomponente mit Grid, Filter, Pagination
  styles/globals.css    # Basis-Styling
  main.tsx              # Einstiegspunkt
```

## 🔧 Setup

1. Repository klonen:

   ```bash
   git clone https://github.com/chefkoch0312/gallery.kado-ber.de.git
   cd gallery.kado-ber.de
   ```

2. Abhängigkeiten installieren:

   ```bash
   npm install
   ```

3. Entwicklungsserver starten:
   ```bash
   npm run dev
   ```

## 🖋️ Bildverwaltung

Bilder werden über die Datei `public/data/images.json` verwaltet.  
Jeder Eintrag folgt diesem Schema:

```json
{
  "src": "/images/bildname.jpg",
  "alt": "Bildbeschreibung",
  "category": "AI",
  "tags": ["blue", "cyber", "robot"]
}
```

Zur automatischen Erstellung kann ein Python-Skript verwendet werden.

## 📬 Kontaktfunktion

Jedes Bild kann über die Lightbox per Mail angefragt werden.  
Der Betreff enthält Alt-Text und Dateiname – z. B.:

```
Betreff: Bildanfrage: Futuristische Stadt bei Nacht (bild23.jpg)
```

## ⚠️ Hinweis

Dieses Projekt dient aktuell ausschließlich der Präsentation.  
Es ist **nicht als Webshop konzipiert**, sondern als ästhetisch zurückhaltende Galerie mit optionalem Kontaktangebot.

---

## 🛠️ Zusatztools

Die folgenden Python-Skripte befinden sich im Verzeichnis `public/tools/`:

### 🔄 `generate_images_json.py`

Ein Python-Skript zur automatischen Erstellung der Datei `images.json`.
Es liest alle `.jpg`-Dateien im Ordner `public/images` aus und erzeugt für jedes Bild einen Eintrag mit Alt-Text, Kategorie und Tags.

### 🖋️ `add_watermark.py`

Ein optionales Wasserzeichen-Tool für vorbereitete Bilder.
Es versieht jedes Bild mit einem dezenten Wasserzeichen und speichert es im `.jpg`-Format – ideal für die Galerie-Veröffentlichung.

Die Tools können lokal ausgeführt werden, beeinflussen aber nicht den React-Build oder das Webfrontend. Sie dienen ausschließlich der vorbereitenden Medienverarbeitung.

Entwickelt & gepflegt von [Kai Dombrowski](https://kado-ber.de/)
