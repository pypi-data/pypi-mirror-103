import discord
from .constants import *


class Embed(discord.Embed):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _check_integrety(self):
        if len(self) > MAX_EMBED_TOTAL_LENGTH:
            raise ValueError(f"Embed total length cannot exceed {MAX_EMBED_TOTAL_LENGTH} in length")
        elif len(self.title) > MAX_EMBED_TITLE_LENGTH:
            raise ValueError(f"Embed title cannot exceed {MAX_EMBED_TITLE_LENGTH} in length")
        elif len(self.description) > MAX_EMBED_DESCRIPTION_LENGTH:
            raise ValueError(f"Embed description cannot exceed {MAX_EMBED_DESCRIPTION_LENGTH} in length")
        elif len(self.fields) > MAX_EMBED_FIELD_COUNT:
            raise ValueError(f"Embed field count cannot exceed {MAX_EMBED_FIELD_COUNT}")

    def add_field(self, *, name, value, inline):
        return super().add_field(name, value, inline=inline)
    
    def insert_field_at(self, index, *, name, value, inline):
        e = super().insert_field_at(index, name, value, inline=inline)
        self._check_integrety()
        return e
