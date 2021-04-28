class Quote():
    def __init__(self):
        self.quote_list = ["If you stat it, they can kill it.", "DnD is for bosses.", "Made with love...", "Written in Python", "Beware the forbidden deck...", "Don't touch the shiny thing.", "The world is a vampire.", "If you like Metroid, we can be friends.", "Just fireball...", "If the answer isn't fireball, the question is incorrect.", "Melee types use sword magic.", "Beware the forbidden duck..."]

    def get_quote(self, rand_num):
        return self.quote_list[rand_num]