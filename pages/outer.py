import flet as ft  
from parts.appbar import Appbar
class Main_error404(ft.View):
    def __init__(self,route:str,page):
        super().__init__()
        self.route = route
        self.page = page
        self.appbar = Appbar(title='Pagina não Encontrada',page=page)
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER
        self.bgcolor = '#1d2124'
    def build(self):
        return ft.Container(
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src='images/notfound.png',border_radius=ft.border_radius.all(100),height=600),
                    ft.Button(text="Voltar Inicio",on_click=lambda _:self.page.go('/'))
                ]
            )
        )