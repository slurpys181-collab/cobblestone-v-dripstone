# Cobblestone V Dripstone

A Minecraft Bedrock behavior pack for Bedrock 26.52. It adds one shaped crafting recipe:

\`\`\`text
Cobblestone               Cobblestone

             Cobblestone
                   ↓
         Pointed Dripstone ×1
\`\`\`

In a 3×3 crafting table grid, put cobblestone in the **top-left**, **top-right**, and **bottom-centre** slots. This makes a V shape and crafts one pointed dripstone. The pack does not replace vanilla recipes or require experimental features.

## Download

Download [Cobblestone-V-Dripstone.mcpack](./Cobblestone-V-Dripstone.mcpack) from this repository, then open/import it with Minecraft Bedrock. Activate it in your world's **Behavior Packs** settings.

## Tree Chop add-on

This repository also includes **Tree Chop**, a separate Bedrock behavior pack. In Survival, break a log to remove nearby connected log/wood blocks and drop their matching items.

- Download [Tree-Chop.mcpack](./Tree-Chop.mcpack).
- Browse the editable pack source in [tree-chop/](./tree-chop/).
- Read the [Tree Chop setup notes](./tree-chop/README.md), including its search limits.

## GitHub Pages website

This repository includes index.html and a GitHub Actions workflow at .github/workflows/pages.yml. In GitHub, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**. The workflow publishes the site after a push to main (or after you run the workflow manually). The site URL will be https://slurpys181-collab.github.io/cobblestone-v-dripstone/ after GitHub Pages is enabled and deployment succeeds.

## Files

- Cobblestone-V-Dripstone.mcpack — ready-to-import dripstone behavior pack
- Tree-Chop.mcpack — ready-to-import tree chopping behavior pack
- index.html — dripstone download website
- manifest.json, recipes/pointed_dripstone.json — dripstone pack source
- tree-chop/manifest.json, tree-chop/scripts/main.js — tree chop pack source
- pack_icon.png and tree-chop/pack_icon.png — pack icons
- .github/workflows/pages.yml — GitHub Pages deployment workflow

## Compatibility note

The dripstone pack declares minimum engine version 1.26.0, covering the Bedrock 1.26 / 26.x version line. The recipe uses the documented minecraft:recipe_shaped schema. Tree Chop declares minimum engine version 1.26.0 and uses the stable @minecraft/server 2.7.0 Script API.