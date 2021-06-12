from typing import ClassVar, List, Optional, TYPE_CHECKING

from asyncpg import Record
from attr import dataclass
from mautrix.types import EventID, RoomID
from mautrix.util.async_db import Database

from .model_base import Model

fake_db = Database("") if TYPE_CHECKING else None


@dataclass
class Reaction(Model):
    db: ClassVar[Database] = fake_db

    mxid: EventID
    mx_room: RoomID
    li_message_urn: str
    li_receiver_urn: str
    li_sender_urn: str
    reaction: str

    _table_name = "reaction"
    _field_list = [
        "mxid",
        "mx_room",
        "li_message_urn",
        "li_receiver_urn",
        "li_sender_urn",
        "reaction",
    ]

    @classmethod
    def _from_row(cls, row: Optional[Record]) -> Optional["Reaction"]:
        if row is None:
            return None
        return cls(**row)

    async def insert(self):
        query = Reaction.insert_constructor()
        await self.db.execute(
            query,
            self.mxid,
            self.mx_room,
            self.li_message_urn,
            self.li_receiver_urn,
            self.li_sender_urn,
            self.reaction,
        )

    async def delete(self):
        query = """
            DELETE FROM reaction
             WHERE li_message_urn=$1
               AND li_receiver_urn=$2
               AND li_sender_urn=$3
        """
        await self.db.execute(
            query,
            self.li_message_urn,
            self.li_receiver_urn,
            self.li_sender_urn,
        )

    async def save(self):
        query = """
            UPDATE reaction
               SET mxid=$1,
                   mx_room=$2,
                   reaction=$3
             WHERE li_message_urn=$1
               AND li_receiver_urn=$2
               AND li_sender_urn=$3
        """
        await self.db.execute(
            query,
            self.mxid,
            self.mx_room,
            self.reaction,
            self.li_message_urn,
            self.li_receiver_urn,
            self.li_sender_urn,
        )