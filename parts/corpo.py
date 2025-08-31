import flet as ft
from parts.appbar import Appbar
from parts.db import quantidade,last_item
#**kwargs

class Corpo(ft.View):
    def __init__(self,route:str,page):
        super().__init__()
        self.route = route
        self.page = page
        self.txt = 'txt'
        self.appbar = Appbar(title='Meu App',page=page)

#INfo banners receitas
        rec_q1 = quantidade('recipe','nome')
        self.rec_q1 = str(rec_q1)
        x = last_item('recipe')
        self.rec_q2 = x[0]
#Info banner movie e music
        msm_q1 = quantidade('msm','nome')
        self.msm_q1 = str(msm_q1)
        x = last_item('msm')
        self.msm_q2 = x[1] 
#Info banner humorado
        hum_q1 = quantidade('humorado','date')
        self.hum_q1 = str(hum_q1)
        x = last_item('humorado')
        self.hum_q2 = x[0]
    def build(self):
        hp = 55
        return ft.ResponsiveRow(
            expand=True,
            columns=12,
            controls=[
                ft.Text(value='corpinho',style=ft.TextThemeStyle.HEADLINE_LARGE),
                ft.Row(controls=[
                    AppItem(title='Money',txt1='Cotação ',q1='+30',txt2='Balanço ',q2='+5',url='/financa'),
                    AppItem(title='Receitas',txt1='Quantidade receitas ',q1=self.rec_q1,txt2='Ultima adicionada ',q2=self.rec_q2,url='/receitas'),
                    AppItem(title='Filmes e Series',txt1='Quantidade adicionada ',q1=self.msm_q1,txt2='Ultima adicionado ',q2=self.msm_q2,url='/msm'),
                    AppItem(title='Humorado',txt1=f'Estamos a {self.hum_q1} dias fazendo',q1='',txt2='Last Update ',q2=f'{self.hum_q2}',url='/humor')

            ]),
                
            ]
        )

class AppItem(ft.Container):
    def __init__ (self,title:str,txt1:str,q1:str,txt2:str,q2:str,url:str):
        super().__init__()
        #self.expand=True
        self.bgcolor=ft.colors.ON_INVERSE_SURFACE
        self.padding=5
        self.expand=True
        self.content=ft.Column (
            col = {'xs': 6, 'lg': 3},
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text(value=title,style=ft.TextTheme.headline_large,text_align=ft.MainAxisAlignment.CENTER,color=ft.colors.WHITE),
                ft.Text(
                    text_align=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spans=[
                        ft.TextSpan(text=txt1,style=ft.TextTheme.body_medium),
                        ft.TextSpan(text=q1,style=ft.TextTheme.body_large)
                    ]
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(text=txt2,style=ft.TextTheme.body_medium),
                        ft.TextSpan(text=q2,style=ft.TextTheme.body_large)
                    ]
                ),
                ft.TextButton(
                    on_click=lambda _:self.page.go(url),
                    content=ft.Row(
                        tight=True,
                        controls=[
                            ft.Text(value='ENTRAR',style=ft.TextTheme.body_large, color=ft.colors.PRIMARY ),
                            ft.Icon(name=ft.icons.ARROW_FORWARD_IOS, size=14, color=ft.colors.PRIMARY)

                    ])
                )

            ]
        )   
        