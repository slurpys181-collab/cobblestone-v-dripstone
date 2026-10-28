# Tree Chop — Minecraft Bedrock Behavior Pack

Break a log in **Survival** and the pack searches for nearby, directly connected log/wood blocks. It removes those blocks and drops one matching log/wood item for each block it removes. The first block you mine still uses Minecraft's normal drop behaviour.

## Install

1. Open Tree-Chop.mcpack with Minecraft Bedrock to import it.
2. Edit your world's settings and open **Behavior Packs**.
3. Activate **Tree Chop** for that world.
4. Enter the world and break a tree log in Survival.

The script uses the stable @minecraft/server 2.7.0 module and declares minimum engine version 1.26.0. It does not require experimental gameplay toggles where that stable scripting API is available.

## Notes

- Supports standard and stripped Overworld logs/wood and Nether stems/hyphae.
- Leaves are not manually removed; Minecraft can decay them normally after the logs are gone.
- Search is capped at 256 connected logs, with a 12-block horizontal radius, 32 blocks upward, and 8 blocks downward. Large or unusual trees can exceed the limit.
- Avoid chopping directly connected log/wood structures you want to keep, because connected log blocks are what the script targets.