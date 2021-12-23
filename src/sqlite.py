import aiosqlite3
import discord
import os


async def create_database_file_if_not_exists():
    if not os.path.isfile("database.sqlite"):
        with open("database.sqlite", 'x') as f:
            f.close()
    async with aiosqlite3.connect("database.sqlite") as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
            id VARCHAR(19),
            score TEXT
        )''')
        await db.commit()


async def get_score(player: discord.User):
    await create_database_file_if_not_exists()
    async with aiosqlite3.connect("database.sqlite") as db:
        cursor = await db.execute("SELECT score FROM leaderboard WHERE id=?", [str(player.id)])
        return await cursor.fetchone()

async def get_all_scores():
    async with aiosqlite3.connect("database.sqlite") as db:
        cursor = await db.execute("SELECT * FROM leaderboard ORDER BY score")
        return await cursor.fetchall()

async def set_score(player: discord.User, scores: str) -> None:
    await create_database_file_if_not_exists()
    async with aiosqlite3.connect("database.sqlite") as db:    
        if not await get_score(player):
            await db.execute("INSERT INTO leaderboard VALUES (?, ?)", (str(player.id), scores,))
        else:
            await db.execute("UPDATE leaderboard SET score=? WHERE id=?", (scores, str(player.id),))
        await db.commit()
        return