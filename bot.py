import discord
from discord.ext import commands
import json


# Define intents and enable message content
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# File to store posts
DATA_FILE = "data.json"

# Helper functions
def load_posts():
    """Load all posts from the data file."""
    try:
        with open(DATA_FILE, "r") as file:
            posts = json.load(file)
            if not isinstance(posts, list):  # Ensure the structure is a list
                return []
            return posts
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_posts(posts):
    """Save posts to the data file."""
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=4)

def add_post(title, content, image_url="", video_url=""):
    """Add a new post to the data file."""
    if not title or not content:
        return False  # Title and content are required
    posts = load_posts()
    post = {
        "title": title,
        "content": content,
        "image_url": image_url,
        "video_url": video_url
    }
    posts.append(post)
    save_posts(posts)
    return True

def delete_post_by_title(title):
    """Delete a post by its title."""
    posts = load_posts()
    filtered_posts = [post for post in posts if post["title"].lower() != title.lower()]
    save_posts(filtered_posts)
    return len(posts) != len(filtered_posts)  # Returns True if a post was deleted

def edit_post_by_title(title, new_content=None, new_image_url=None, new_video_url=None):
    """Edit a post by its title."""
    posts = load_posts()
    for post in posts:
        if post["title"].lower() == title.lower():
            if new_content:
                post["content"] = new_content
            if new_image_url:
                post["image_url"] = new_image_url
            if new_video_url:
                post["video_url"] = new_video_url
            save_posts(posts)
            return True  # Successfully edited
    return False  # Post not found

# Bot commands
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="post")
async def post(ctx, title=None, content=None, image_url=None, video_url=None):
    """Add a new post."""
    if not title or not content:
        await ctx.send("❌ **Error:** Both title and content are required for a post. Usage: `!post <title> <content> [image_url] [video_url]`")
        return
    success = add_post(title, content, image_url, video_url)
    if success:
        embed = discord.Embed(title="✅ Post Added", color=discord.Color.green())
        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Content", value=content, inline=False)
        if image_url:
            embed.set_image(url=image_url)
        if video_url:
            embed.add_field(name="Video", value=video_url, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ **Error:** Unable to add post. Please try again.")

@bot.command(name="delpost")
async def delpost(ctx, title=None):
    """Delete a post by title."""
    if not title:
        await ctx.send("❌ **Error:** Title is required to delete a post. Usage: `!delpost <title>`")
        return
    success = delete_post_by_title(title)
    if success:
        embed = discord.Embed(title="🗑️ Post Deleted", description=f"Post titled '{title}' has been deleted.", color=discord.Color.red())
    else:
        embed = discord.Embed(title="❌ Post Not Found", description=f"Could not find a post titled '{title}'.", color=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(name="editpost")
async def editpost(ctx, title=None, new_content=None, new_image_url=None, new_video_url=None):
    """Edit a post by title."""
    if not title:
        await ctx.send("❌ **Error:** Title is required to edit a post. Usage: `!editpost <title> [new_content] [new_image_url] [new_video_url]`")
        return
    success = edit_post_by_title(title, new_content, new_image_url, new_video_url)
    if success:
        embed = discord.Embed(title="✏️ Post Edited", description=f"Post titled '{title}' has been updated.", color=discord.Color.blue())
    else:
        embed = discord.Embed(title="❌ Post Not Found", description=f"Could not find a post titled '{title}'.", color=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(name="commands")
async def help_command(ctx):
    """Provide a list of commands and their usage."""
    embed = discord.Embed(title="📜 Help - Available Commands", color=discord.Color.blurple())
    embed.add_field(name="!post", value="Add a post. Usage: `!post <title> <content> [image_url] [video_url]`", inline=False)
    embed.add_field(name="!delpost", value="Delete a post by title. Usage: `!delpost <title>`", inline=False)
    embed.add_field(name="!editpost", value="Edit a post. Usage: `!editpost <title> [new_content] [new_image_url] [new_video_url]`", inline=False)
    embed.add_field(name="!help", value="Show this help message.", inline=False)
    await ctx.send(embed=embed)

# Global error handler
@bot.event
async def on_command_error(ctx, error):
    """Handle errors globally."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ **Error:** Missing required arguments. Use `!help` for more info.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ **Error:** Command not found. Use `!help` to see the list of available commands.")
    else:
        await ctx.send("❌ **An unexpected error occurred. Please try again.**")
        print(f"Error: {error}")  # Log the error for debugging

bot.run(st.secrets["DISCORD_TOKEN"])
