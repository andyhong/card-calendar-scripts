from dhooks import Webhook, Embed

def send_new_set(webhook, set_info):

  hook = Webhook(webhook)
  embed = Embed(
    color=1127128,
    title="New Card Release Added",
    description=set_info["name"],
    timestamp="now",
  )

  embed.add_field(
    name="Release Date",
    value=set_info["release_date"],
    inline=False
  )

  embed.add_field(
    name="Category",
    value=set_info["category"],
    inline=False
  )

  embed.add_field(
    name="View Full Calendar",
    value="[Click here](https://tempest.cards/)",
    inline=True
  )

  embed.set_author(
    name="Card Release Calendar",
    icon_url="https://cdn.discordapp.com/attachments/161323390362320897/743688864694009856/Untitled-1.png"
  )

  embed.set_footer(
    text="Tempest Cards Release Calendar",
    icon_url="https://cdn.discordapp.com/attachments/161323390362320897/743688864694009856/Untitled-1.png"
  )

  hook.send(embed=embed)

def update_set(webhook, set_info):

  hook = Webhook(webhook)
  embed = Embed(
    color=14177041,
    title="Release Date Update",
    description=set_info["name"],
    timestamp="now",
  )

  embed.add_field(
    name="Release Date",
    value=set_info["release_date"],
    inline=False
  )

  embed.add_field(
    name="Category",
    value=set_info["category"],
    inline=False
  )

  embed.add_field(
    name="View Full Calendar",
    value="[Click here](https://tempest.cards/)",
    inline=True
  )

  embed.set_author(
    name="Card Release Calendar",
    icon_url="https://cdn.discordapp.com/attachments/161323390362320897/743688864694009856/Untitled-1.png"
  )

  embed.set_footer(
    text="Tempest Cards Release Calendar",
    icon_url="https://cdn.discordapp.com/attachments/161323390362320897/743688864694009856/Untitled-1.png"
  )

  hook.send(embed=embed)
