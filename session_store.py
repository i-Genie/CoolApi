import uuid


class SessionStore:
    def __init__(self) -> None:
        self.sessions = {}

    def create(self):
        session_id = str(
            uuid.uuid4()
        )

        self.sessions[session_id] = {}
        return session_id

    def get(
        self,
        session_id
    ):
        return self.sessions.get(
            session_id
        )

    def set(
        self,
        session_id,
        key,
        value
    ):
        if session_id in self.sessions:
            self.sessions[session_id][key] = value