import { world, system, ItemStack, GameMode } from "@minecraft/server";

// Keep the search local so chopping a tree cannot traverse an entire wooden build.
const MAX_LOGS = 256;
const MAX_XZ_DISTANCE = 12;
const MAX_UP_DISTANCE = 32;
const MAX_DOWN_DISTANCE = 8;

const NEIGHBOURS = [
  { x: 1, y: 0, z: 0 },
  { x: -1, y: 0, z: 0 },
  { x: 0, y: 1, z: 0 },
  { x: 0, y: -1, z: 0 },
  { x: 0, y: 0, z: 1 },
  { x: 0, y: 0, z: -1 },
];

function isLogType(typeId) {
  // Includes normal/stripped logs and wood, plus Nether stems and hyphae.
  const path = typeId.replace(/^minecraft:/, "");
  return /(?:_log|_wood|_stem|_hyphae)$/.test(path);
}

function positionKey(pos) {
  return pos.x + "," + pos.y + "," + pos.z;
}

function isWithinSearchBounds(pos, origin) {
  return (
    Math.abs(pos.x - origin.x) <= MAX_XZ_DISTANCE &&
    Math.abs(pos.z - origin.z) <= MAX_XZ_DISTANCE &&
    pos.y >= origin.y - MAX_DOWN_DISTANCE &&
    pos.y <= origin.y + MAX_UP_DISTANCE
  );
}

function chopConnectedLogs(dimension, origin) {
  const queue = NEIGHBOURS.map((offset) => ({
    x: origin.x + offset.x,
    y: origin.y + offset.y,
    z: origin.z + offset.z,
  }));
  const visited = new Set();
  const logs = [];

  // Flood-fill all directly connected log/wood blocks around the block the
  // player broke. The original block is already handled by vanilla drops.
  for (let index = 0; index < queue.length && logs.length < MAX_LOGS; index++) {
    const pos = queue[index];
    if (!isWithinSearchBounds(pos, origin)) continue;

    const key = positionKey(pos);
    if (visited.has(key)) continue;
    visited.add(key);

    let block;
    try {
      block = dimension.getBlock(pos);
      if (!block || !isLogType(block.typeId)) continue;
    } catch {
      // Ignore unloaded chunks and positions outside the world.
      continue;
    }

    const typeId = block.typeId;
    logs.push({ pos, typeId });
    for (const offset of NEIGHBOURS) {
      queue.push({
        x: pos.x + offset.x,
        y: pos.y + offset.y,
        z: pos.z + offset.z,
      });
    }
  }

  for (const entry of logs) {
    try {
      const block = dimension.getBlock(entry.pos);
      if (!block || block.typeId !== entry.typeId) continue;
      block.setType("minecraft:air");
      dimension.spawnItem(
        new ItemStack(entry.typeId, 1),
        { x: entry.pos.x + 0.5, y: entry.pos.y + 0.5, z: entry.pos.z + 0.5 },
      );
    } catch {
      // Skip a block if Minecraft invalidates it while the tree is being cut.
    }
  }
}

world.afterEvents.playerBreakBlock.subscribe((event) => {
  const brokenTypeId = event.brokenBlockPermutation.type.id;
  if (!isLogType(brokenTypeId)) return;

  // Leave Creative mode alone; tree chopping is intended for Survival.
  if (event.player.getGameMode() !== GameMode.Survival) return;

  const origin = {
    x: event.block.location.x,
    y: event.block.location.y,
    z: event.block.location.z,
  };
  const dimension = event.dimension;

  // Defer mutations until after the block-break event has completed.
  system.run(() => {
    try {
      chopConnectedLogs(dimension, origin);
    } catch {
      // Keep one failed tree search from interrupting the script runtime.
    }
  });
});