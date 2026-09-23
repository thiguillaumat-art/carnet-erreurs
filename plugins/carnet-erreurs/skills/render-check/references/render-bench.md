# Le banc de rendu — comment voir chaque sortie

L'objection la plus fréquente est « je n'ai pas de navigateur ». Elle est
presque toujours fausse. Voici le moyen adapté à chaque type de sortie.

---

## PDF

Charger le module qui le produit **sans passer par un build**, puis convertir
chaque page en image et la regarder.

```bash
# jiti charge un module TypeScript directement, sans compilation
node -e "
const createJiti = require('./node_modules/jiti').createJiti
const jiti = createJiti(__filename, { alias: { '@': process.cwd() } })
const mod = jiti('./lib/pdf.ts')
mod.generatePDF(donneesDeTest).then(b64 =>
  require('fs').writeFileSync('/tmp/out.pdf', Buffer.from(b64, 'base64')))
"

pdftoppm -png -r 100 /tmp/out.pdf /tmp/page   # une image par page
```

Puis **regarder chaque image**. Pas la première seulement : les défauts de
pagination — texte coupé, élément orphelin, police changée après un saut de
page — n'apparaissent qu'à partir de la deuxième.

⚠️ `pdftoppm` vient de `poppler-utils`.

---

## E-mail

Le HTML d'un e-mail n'est jamais visible : il part dans un envoi. La parade est
un faux module d'envoi qui l'intercepte.

```js
// stub/nodemailer.js — remplace le vrai module le temps du test
module.exports = {
  createTransport: () => ({
    sendMail: async (o) => {
      require('fs').writeFileSync('/tmp/mail.html', o.html)
      return { messageId: 'stub' }
    }
  })
}
```

Charger le module d'envoi avec un alias pointant sur ce faux module, appeler la
fonction, puis rendre le HTML :

```bash
python3 -c "import weasyprint; weasyprint.HTML(filename='/tmp/mail.html').write_pdf('/tmp/mail.pdf')"
pdftoppm -png -r 110 /tmp/mail.pdf /tmp/mail
```

⚠️ `weasyprint` n'est pas un client de messagerie : il ne reproduit ni Outlook
ni Gmail. Il montre la mise en page, la typographie et les couleurs — ce qui
suffit à trouver la quasi-totalité des défauts. Pour le reste, il n'y a que
l'envoi réel.

---

## Page rendue en JavaScript

`fetch` d'une URL retourne le HTML **avant exécution du JavaScript** : sur une
page rendue côté client, on récupère une coquille vide. Utiliser un outil de
navigateur qui exécute le JavaScript, puis lire le texte ou l'arbre
d'accessibilité plutôt qu'une capture — on obtient le contenu réel et sa
structure, pas des pixels.

⛔ Si la page oppose une vérification anti-robot, **s'arrêter**. Ne pas la
contourner. Le dire à l'utilisateur et proposer une autre source.

---

## Composant React ou page d'application

Le plus difficile, parce qu'il faut un moteur de rendu complet.

Par ordre de préférence :

1. **Le serveur de développement de l'utilisateur**, avec un outil de
   navigateur. C'est le vrai composant : rien ne vaut mieux.
2. **Une transcription HTML fidèle** du balisage et des styles, rendue à part.
   ⚠️ **À annoncer explicitement comme une approximation** — c'est une
   retranscription, elle peut diverger du vrai composant.
3. Faute des deux, **le dire**, et demander à l'utilisateur de regarder.

---

## Affichage mobile

La même chaîne, en imposant la largeur :

```python
import weasyprint
weasyprint.HTML(filename='page.html').write_pdf(
    'mobile.pdf',
    stylesheets=[weasyprint.CSS(string='@page { size: 375px 1400px; margin: 0 }')])
```

⭐ **Calculer d'abord la largeur réelle de la colonne de lecture** au point de
rupture le plus étroit : largeur de l'écran, moins les marges de page, moins les
marges intérieures. Ce nombre explique à lui seul le troncage, la longueur des
lignes et le nombre de lignes d'un titre.

Exemple mesuré : 375 − 48 (page) − 72 (article) = **255 px**, soit environ 27
caractères par ligne à 18 px — très en dessous des 45 minimum confortables.

---

## Ce qui n'est pas un rendu

- Relire le code.
- Vérifier que le build se termine.
- Faire confiance à une modification « évidente ».
- Regarder la première page d'un document qui en compte cinq.
- Vérifier sur un seul écran.
