import flet as ft, time
from ava.ava_backend.rag_query import index

class Message():
    def __init__(self, text: str, user_name: str = "Ava"):
        self.user_name = user_name
        self.text = text

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold"),
                        ft.Text(message.text, selectable=True),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"  # or any default value you prefer

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"

    # def join_chat_click(e):
    #     if not join_user_name.value:
    #         join_user_name.error_text = "Name cannot be blank!"
    #         join_user_name.update()
    #     else:
    #         page.session.set("user_name", join_user_name.value)
    #         page.dialog.open = False
    #         new_message.prefix = ft.Text(f"{join_user_name.value}: ")
    #         page.update()

    def send_message_click(e):
        if new_message.value != "":
            message = Message(new_message.value, "Balo")
            m = ChatMessage(message)
            new_message.value = ""
            new_message.disabled = True
            chat.controls.append(m)
            ava_response = index.as_query_engine().query(message.text)
            response = Message(ava_response.response)
            chat.controls.append(ChatMessage(response))
            new_message.disabled = False
            new_message.focus()
            page.update()

    # A dialog asking for a user display name
    # join_user_name = ft.TextField(
    #     label="Enter your name to join the chat",
    #     autofocus=True,
    #     on_submit=join_chat_click,
    # )
    # page.dialog = ft.AlertDialog(
    #     open=True,
    #     modal=True,
    #     title=ft.Text("Welcome!"),
    #     content=ft.Column([join_user_name], width=300, height=70, tight=True),
    #     actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
    #     actions_alignment="end",
    # )

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

ft.app(main)