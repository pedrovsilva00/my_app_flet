import flet as ft
from parts.corpo import Corpo
from pages.financa import Main_financa
from pages.receitas import Main_receitas
from pages.humor import Main_humor
from pages.outer import Main_error404
from pages.movie import Main_movie

class AppTheme:
    theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            background='#20202a',
            on_background='#2d2d3a',
            on_inverse_surface='#2d2d3a',
            primary=ft.colors.AMBER,
        ),
        text_theme=ft.TextTheme(
            body_large=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                size=14,
            ),
            body_medium=ft.TextStyle(
                weight=ft.FontWeight.NORMAL,
                color=ft.colors.GREY,
                size=14,
            ),
            headline_large=ft.TextStyle(
                weight=ft.FontWeight.W_900,
                color=ft.colors.WHITE,
                size=50,
            ),
            label_large=ft.TextStyle(
                weight=ft.FontWeight.W_700,
                color=ft.colors.WHITE,
                size=16,
            ),
            headline_medium=ft.TextStyle(
                weight=ft.FontWeight.W_700,
                color=ft.colors.WHITE,
                size=30,
            )
        ),
        
    )


def main(page: ft.Page):
    page.title = "Routes Example"
    page.theme = AppTheme.theme
    def route_change(route):
        if page.route == '/':
            page.views.clear()
            page.views.append(
                    Corpo(route='/',page=page)
            )
        elif page.route =='/financa': #falta o acompanhamento da carteira, as ações e os graficos
            page.views.append(
                Main_financa(route='/financa',page=page)
            )
        elif page.route =='/receitas': # 80% concluida
            page.views.append(
                Main_receitas(route='/receitas',page=page)
            )
        elif page.route == '/humor':
            page.views.append(
                Main_humor(route='/humor',page=page)
            )
        elif page.route == '/msm': #Falta embelezar e refinar, funções basicas ok
            page.views.append(
                Main_movie(route='/msm',page=page)
            )
        else: 
            page.views.append(Main_error404(route='/error404',page=page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, assets_dir="assets")

