import flet as ft
from pages import ChatPage
import os
from flet.auth.providers import GitHubOAuthProvider


GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Ava"
    provider = GitHubOAuthProvider(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        redirect_url="https://8550-balojey-ava-xxh9i2y4xkt.ws-eu111.gitpod.io/oauth_callback",
    )

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
        controls=[]
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

ft.app(main)