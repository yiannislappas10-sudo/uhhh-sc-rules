import os
import discord
from discord import app_commands
from discord.ext import commands

# Replace this number with your actual Discord Server ID
GUILD_ID = discord.Object(id=1529246492332920872) 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class RuleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1. Weapon Discipline", value="1", emoji="🔫"),
            discord.SelectOption(label="2. Identification", value="2", emoji="🪪"),
            discord.SelectOption(label="3. Post Discipline", value="3", emoji="📍"),
            discord.SelectOption(label="4. Authority", value="4", emoji="🎖️"),
            discord.SelectOption(label="5. Restricted Areas", value="5", emoji="🚫"),
            discord.SelectOption(label="6. Incidents", value="6", emoji="🚨"),
            discord.SelectOption(label="7. Professional Conduct", value="7", emoji="💼"),
            discord.SelectOption(label="8. Roleplay Discipline", value="8", emoji="🎭"),
            discord.SelectOption(label="9. Equipment", value="9", emoji="📦"),
            discord.SelectOption(label="10. Accountability", value="10", emoji="⚖️"),
        ]
        super().__init__(placeholder="Select The Rule", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        rules = {
            "1": "**1. WEAPON DISCIPLINE**\n• Do not fire without a valid threat.\n• No unnecessary firing or mag-dumping.\n• Do not shoot personnel because of suspicion alone.\n• Do not fire into crowds or populated areas recklessly.\n• Keep your weapon under control at all times.",
            "2": "**2. IDENTIFICATION**\n• Know who you are dealing with before taking action.\n• Do not attack someone simply because they are unfamiliar.\n• Ask questions and verify authorization when appropriate.\n• If unsure, contact a superior rather than escalating.",
            "3": "**3. POST DISCIPLINE**\n• Stay at assigned position unless given permission to leave.\n• Do not abandon post during minor incidents.\n• Do not wander around looking for trouble.\n• Remain attentive while stationed.",
            "4": "**4. AUTHORITY**\n• Follow orders from authorized superiors.\n• Do not give orders beyond your rank.\n• Do not threaten/intimidate personnel with weapons.\n• Security authority must never be used for personal arguments.",
            "5": "**5. RESTRICTED AREAS**\n• Do not allow unauthorized personnel into restricted areas.\n• Do not enter restricted zones without proper clearance.\n• Do not grant other players access to uncleared areas.",
            "6": "**6. INCIDENTS**\n• Stay calm during emergencies.\n• Protect nearby personnel and secure the area.\n• Do not exacerbate incidents through reckless behavior.\n• Report serious incidents to a superior immediately.",
            "7": "**7. PROFESSIONAL CONDUCT**\n• No harassment, bullying, or unnecessary aggression.\n• Do not randomly detain or attack people.\n• Do not start conflicts while on duty.\n• Remain professional even during difficult interactions.",
            "8": "**8. ROLEPLAY DISCIPLINE**\n• Do not use OOC information for IC decisions.\n• Do not randomly kill players for entertainment.\n• Follow facility RP rules and character boundaries.",
            "9": "**9. EQUIPMENT**\n• Do not misuse security equipment.\n• Do not take another officer's equipment without permission.\n• Report missing or damaged equipment to a superior.",
            "10": "**10. ACCOUNTABILITY**\n• Mistakes must be reported instead of hidden.\n• Repeated violations result in disciplinary action.\n• Severe misconduct leads to immediate removal."
        }
        
        selected_text = rules.get(self.values[0], "Rule not found.")
        embed = discord.Embed(
            title="📜 Rule Directive",
            description=selected_text,
            color=0x2F3136
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class SecurityDashboardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RuleSelect())

        self.add_item(discord.ui.Button(label="Community Guidelines", url="https://dis.gd/tos", row=1, emoji="📋"))
        self.add_item(discord.ui.Button(label="Support", url="https://discord.gg/kCz3W4VT4", row=1, emoji="❓"))

    @discord.ui.button(label="Point Info", style=discord.ButtonStyle.secondary, custom_id="point_info_btn", row=2, emoji="📌")
    async def point_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚖️ Points & Disciplinary Action",
            description=(
                "Failure to follow rules will result in disciplinary action. Caught violations lead to:\n\n"
                "• **Warning**\n"
                "• **Suspension**\n"
                "• **Demotion**\n"
                "• **Removal from Security**\n\n"
                "*Re-joining is permitted only via High Rank approval.*"
            ),
            color=0xE74C3C
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    bot.add_view(SecurityDashboardView())
    
    # Syncs slash commands directly to your server on startup
    bot.tree.copy_global_to(guild=GUILD_ID)
    await bot.tree.sync(guild=GUILD_ID)
    
    print(f"Logged in as {bot.user} - Synced commands to Server ID {GUILD_ID.id}")


@bot.tree.command(name="setup_security", description="Post the Aegis 17 Security directives panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_security(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Site Aegis 17 Security Directive",
        description=(
            "Welcome to the **Site Aegis 17 Security Protocol**. All active personnel must adhere strictly to these guidelines. "
            "Security is a position of trust—failure to maintain proper conduct will lead to immediate disciplinary action.\n\n"
            "And most important thing, you must follow [Discord's Terms of Service](https://dis.gd/tos).\n\n"
            "Click *Select The Rule* to read other rules. They're important too.\n"
            "If it gives error *\"This interaction failed\"* try again."
        ),
        color=0x2B2D31
    )
    
    embed.add_field(
        name="📌 Core Directive",
        value="*If you cannot control your weapon, your authority, or your behavior, you will not remain Security.*",
        inline=False
    )
    embed.add_field(
        name="⚠️ Consequences",
        value="Violating these directives will result in actions including **Warning**, **Suspension**, **Demotion**, or **Removal** depending on severity.",
        inline=False
    )
    embed.add_field(
        name="Click the button to see points and punishment.",
        value="│ • You may re-join only by *High Rank* approval\nYou can apply with apologize\n\n│ • Your warnings with points will be removed after a month.\nIf you get banned again, will be perm with no excuse.",
        inline=False
    )
    embed.set_footer(text="Authored by Ryx and Heathcliff • Site Aegis 17 Security Command")

    await interaction.channel.send(embed=embed, view=SecurityDashboardView())
    await interaction.response.send_message("Dashboard created!", ephemeral=True)


bot.run(os.getenv("DISCORD_TOKEN"))
