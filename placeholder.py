    


    @commands.command()
    async def hold(self, ctx: commands.Context) -> discord.Message:
        embeds: list[discord.Embed] = make_general_embeds(3)
        embed_index: int = 0
        view = HoldView()
        message: discord.Message = ctx.send(content = 'Here are the series that you have on hold.', embed=embeds[embed_index], view = view)
        view.message_awareness(message)
        view.embeds_awareness(embeds)
        view.embed_index_awareness(embed_index)
        await message


    @commands.command()
    async def refresh(self, ctx: commands.Context) -> discord.Message: #Allows user to refresh embed list if there was a manual update to MAL after startup
        keys = ['1', '2', '3', '4', '6']
        for key in keys:
            cache_anime_meta(key)
        await ctx.send("Anime List has been updated")