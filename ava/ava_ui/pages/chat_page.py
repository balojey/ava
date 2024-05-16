import flet as ft
# from ava.ava_backend.rag_query import index

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


class ChatPage(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = True
        self.new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            disabled=False, # if self.page.auth else True,
            on_submit=self.send_message_click,
        )
        self.chat = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )
        self.controls = [
            ft.Container(
                content=self.chat,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    self.new_message,
                    ft.IconButton(
                        icon=ft.icons.SEND_ROUNDED,
                        tooltip="Send message",
                        disabled=False, # False if self.page.auth else True,
                        on_click=self.send_message_click,
                    ),
                ]
            ),
        ]

    # def build(self):
    #     self.update_page_drawer()

    def send_message_click(self, e):
        if self.new_message.value != "":
            message = Message(self.new_message.value, "Balo")
            m = ChatMessage(message)
            self.new_message.value = ""
            self.new_message.disabled = True
            self.chat.controls.append(m)
            # ava_response = index.as_query_engine().query(message.text)
            # response = Message(ava_response.response)
            # self.chat.controls.append(ChatMessage(response))
            self.new_message.disabled = False
            self.new_message.focus()
            self.update()

    def update_page_drawer(self, control: ft.Control = None):
        if len(self.page.drawer.controls) == 0:
            self.page.drawer.controls.extend([
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Item 1",
                    icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
                ),
                ft.Divider(thickness=2),
            ])
        if control != None:
            self.page.drawer.controls.append(control)
        self.page.drawer.update()

