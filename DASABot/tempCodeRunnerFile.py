
        em.add_field(name='</airport:1133054254203011082>  `<college]>`',
                        value='Displays data about the nearest airport to the college specified by the user.',
                        inline=False)
        em.set_footer(text="This message will be deleted after 1 minute.")
        await interaction.response.send_message(embed=em, delete_after=60)


@bot.command(description='Reload a cog.')
@commands.is_owner()