import flet as ft  

class Appbar(ft.AppBar):
    def __init__(self,title,page):
        super().__init__()
        self.title = ft.Text(value=title,style=ft.TextTheme.headline_large)
        self.bgcolor = ft.colors.ON_INVERSE_SURFACE
        self.center_title = True
        self.actions=[
            ft.PopupMenuButton(
                expand=True,
                menu_padding=5,
                padding=5,
                items=[
                    ft.PopupMenuItem(icon=ft.icons.HOME,text="Inicio",on_click=lambda _:page.go('/')),
                    ft.PopupMenuItem(icon=ft.icons.ATTACH_MONEY,text="Finanças",on_click=lambda _:page.go('/financa')),
                    ft.PopupMenuItem(icon=ft.icons.FASTFOOD,text="Livro de Receitas",on_click=lambda _:page.go('/receitas')),
                    ft.PopupMenuItem(icon=ft.icons.MOVIE_FILTER_OUTLINED,text="Filmes, Musicas e Series",on_click=lambda _:page.go('/msm')),
                    ft.PopupMenuItem(icon=ft.icons.HEALTH_AND_SAFETY,text="Humorado",on_click=lambda _:page.go('/humor')),
                ]
            )
        ]