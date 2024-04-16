from webexteamssdk import WebexTeamsAPI



def send_notification(message: str, webex_api: WebexTeamsAPI, room_id: str ) -> None:
    webex_api.messages.create(roomId=room_id, text=message)