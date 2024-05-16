import flet as ft
from pages import ChatPage
import os
from datetime import datetime
from flet.auth.providers import GitHubOAuthProvider
from llama_index.core.memory import ChatMemoryBuffer
from ava.ava_backend import mongodb_client, index


GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Ava"
    page.chat_memory = ChatMemoryBuffer.from_defaults()
    page.chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=page.chat_memory,
        system_prompt=(
            """Your name is Ava and you are a sui blockchain expert. 
            You offer help regarding all sorts of issue related to 
            the sui blockchain and move programming language."""
        )
    )
    # page.chat_db = "ava" # mongodb_client[os.getenv("CHAT_DB_NAME")]
    # page.chat_collection = "chats" # mongodb_client[os.getenv("CHAT_COLLECTION_NAME")]
    page.current_chat_doc_id = ""

    provider = GitHubOAuthProvider(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        redirect_url="https://8550-balojey-ava-xxh9i2y4xkt.ws-eu111.gitpod.io/oauth_callback",
    )

    def reset_chat_memory():
        page.chat_memory.reset()

    def save_chat_in_db():
        chats = {
            chats: page.chat_memory.to_dict(),
            created_at: datetime.utcnow(),
            updated_at: datetime.utcnow(),
        }
        if page.current_chat_doc_id == "":
            # saved_chat = page.chat_collection.insert_one(chats).inserted_id
            # page.current_chat_doc_id = f"balo###{str(saved_chat)}"
            return
        # saved_chat = page.chat_collection.find_one({"_id": page.current_chat_doc_id})
        saved_chat.update(chats)

    def get_chats_from_db():
        # chats = filter(lambda chat: "balo###" in chat["_id"], page.chat_collection.find())
        pass

    def get_chat_from_db():
        # chat = page.chat_collection.find_one({"_id": page.current_chat_doc_id})
        # page.chat_memory.from_dict(chat["chats"])
        pass

    def login_click(e):
        page.login(provider)

    def logout_click(e):
        page.logout()

    login_button = ft.ElevatedButton(text="Continue with Github", on_click=login_click)
    logout_button = ft.ElevatedButton(text="Logout", on_click=logout_click)

    def on_login(e):
        print("Login error:", e.error)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)

    page.on_login = on_login
    page.appbar = ft.AppBar(
        title=ft.Text("Ava"),
        leading_width=20,
        bgcolor=ft.colors.BLUE_500,
        actions=[
            ft.Container(
                content=login_button if not page.auth else logout_button
            )
        ]
    )
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="New Chat",
                icon=ft.icons.ADD_TASK_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
        ]
    )

    

    # page.dialog = ft.AlertDialog(
    #     open=True if not page.auth else False,
    #     modal=True,
    #     title=ft.Text("Welcome!"),
    #     content=ft.Column([ft.Text("Please login to continue")], width=300, height=70, tight=True),
    #     actions=[login_button],
    #     actions_alignment="end",
    # )
    page.add(ChatPage(page))

ft.app(main, port=8008, export_asgi_app=True)