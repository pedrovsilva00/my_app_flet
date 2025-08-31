import flet as ft
from parts.db import add,procura_in,excluir,procura,atualiza
from parts.appbar import Appbar
import random

class Main_movie(ft.View):
    def __init__(self,route:str,page):
        super().__init__()
        self.route = route
        self.page = page
        self.appbar = Appbar(title='Filmes Series e Musicas',page=page)
        self.scroll = ft.ScrollMode.AUTO
    def build(self):
        x = procura_in('msm','categoria',('filme','serie'),True)
        for item in x:
            last_fs = item[1]
        x = procura('msm',False,True,('musica'),'categoria')
        q = []
        for linha in x:
            q.append(linha[0])
        escolha = random.choice(q)
        print(escolha)
        x = procura('msm',False,True,(escolha),'id')
        for item in x:
            musica = item[1] 
        return ft.ResponsiveRow(
            columns=12,
            controls=[
                movie_serie(last_fs),
                music(musica),

            ]
        )

class movie_serie(ft.Container):
    def __init__(self,txt):
        super().__init__()
        self.padding = 15
        self.col = {'xs':8,'md':7}
        self.name_ms = ft.TextField(label='Nome',col={'xs':4,'md':3})
        self.date = ft.TextField(label='Data lançamento',col={'xs':4,'md':3},on_change=self.ver_data,max_length=10,data=0)
        self.resumo = ft.TextField(label='Sinopse',multiline=True,min_lines=1,col={'xs':5,'md':6})
        self.drop = drop('Filme ou Serie','filme','serie',{'xs':4,'md':3})
        g=['Ação','Aventura','Comédia','Animação','Anime','Super-heróis','Psicológico','Suspense','Ficção Científica','Romance','Fantasia','Guerra','Distopia','Crime','Documentário','História','Drama','Família']
        self.gene_ms = ft.SearchBar(
            bar_hint_text="Genero(s)",
            view_hint_text="Escolha 1 ou mais",
            col={'xs':4,'md':3},
            on_tap=self.open_gene,
            controls=[
                ft.ListTile(title=ft.Text(f"{i}"), on_click=self.close_anchor, data=i) for i in g   
            ],
        )
        c = [ft.DataColumn(label=ft.Text(value='Ações'),heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ft.DataColumn(ft.Text(value='Nome')), #
            ft.DataColumn(ft.Text(value='Genero(s)'),heading_row_alignment=ft.MainAxisAlignment.CENTER), # 
            ft.DataColumn(ft.Text(value='Categoria')), # 
            ft.DataColumn(ft.Text(value='Data de Lançamento',text_align=ft.MainAxisAlignment.START)), #
        ]
        self.tb_fs= ft.DataTable(
            expand=True,
            data_row_min_height = 35,
            data_row_max_height=55,
            column_spacing=50,
            columns=c,
            rows=[]
        )
# Barra de Pesquisa        
        self.pesquisa = ft.TextField(label='Pesquisa',col={'xs':4})
        self.drop_pesq = drop('Nome ou Genero','nome','genero',{'xs':2})
        self.botoes = ft.ResponsiveRow(
            columns=12,
            controls=[ #col={'xs':4,'md':3}
                ft.IconButton(icon='close',icon_color='red',on_click=self.close_tabela,col={'md':1}),
                ft.TextButton(content=ft.Text(value='Todos os Filmes',text_align=ft.TextAlign.CENTER),data=0,on_click=self.mostrar_fs,col={'md':2}),
                ft.TextButton(content=ft.Text(value='Todas as Series',text_align=ft.TextAlign.CENTER),data=1,on_click=self.mostrar_fs,col={'md':2}),
                self.pesquisa,
                self.drop_pesq,
                ft.IconButton(icon='search',icon_color='purple',col={'xs':1},data=2,on_click=self.mostrar_fs),
                
                
            ]
        )
#Conteudo principal
        self.conteudo = ft.ResponsiveRow(
                columns=12,
                #col={'xs':4,'md':6,'lg':9},
                controls=[
                    ft.Text('Filmes e Series',style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                    ft.Text(text_align=ft.TextAlign.JUSTIFY,color='gray',style=ft.TextThemeStyle.LABEL_LARGE,spans=[
                        ft.TextSpan('Ultimo adicionado: '),
                        ft.TextSpan(txt)
                    ]),
                    self.name_ms,
                    self.gene_ms,
                    self.date,
                    self.drop,
                    self.resumo,
                    ft.TextButton(
                        on_click=self.add_ms,
                        col={'md':3},
                        content=ft.Row(
                        tight=True,
                        controls=[
                            ft.Text(value='Adicionar',style=ft.TextTheme.body_large, color=ft.colors.PRIMARY ),
                            ft.Icon(name=ft.icons.ADD, size=14, color=ft.colors.PRIMARY)

                    ])
                    ),
                    
                    ft.TextButton(
                        col={'md':3},
                        on_click=self.mostrar_fs,
                        content=ft.Row(
                            tight=True,
                            controls=[
                                ft.Text(value='Lista Completa',style=ft.TextTheme.body_large, color=ft.colors.PRIMARY ),
                                ft.Icon(name=ft.icons.ARROW_FORWARD_IOS, size=14, color=ft.colors.PRIMARY)

                        ])
                    ),
                    
                ]
            )
#Tabela mostrar
        self.tabela = ft.Column(col={'xs':12},visible=False,controls=[self.botoes,self.tb_fs])
#content movie
        self.content = ft.Column(spacing=15,run_spacing=15,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[
            self.conteudo,
            self.tabela
            ])
#Variaveis de edição

        self.nome_edit = ft.TextField(label='Nome',col={'xs':4,'md':5})
        self.gene_edit = ft.SearchBar(
            bar_hint_text="Genero(s)",
            col={'xs':4,'md':3},
            on_tap=self.open_gene_edit,
            controls=[
                ft.ListTile(title=ft.Text(f"{i}"), on_click=self.close_anchor_edit, data=i) for i in g   
            ],
        )
        self.data_edit = ft.TextField(label='Data lançamento',col={'xs':3,'md':4},on_change=self.ver_data,max_length=10)
        self.res_edit = ft.TextField(label='Sinopse',multiline=True,min_lines=1,col={'xs':5,'md':6})
        self.drop_edit = drop('Filme ou Serie','filme','serie',{'xs':4,'md':3})
        self.myid = ft.Text(value='',col={'xs':3,'md':2},text_align=ft.TextAlign.CENTER,size=25)
        self.banner = ft.Banner(
            open=False,
            leading=ft.Icon(name='edit',color='purple',size=40),
            content_padding=15,
            margin=20,
            force_actions_below = True,
            content=ft.ResponsiveRow(columns=12,controls=[
                ft.Text('Edição de valores'),
                self.nome_edit, 
                self.data_edit,
                self.drop_edit,
                self.gene_edit,
                self.res_edit,
                self.myid
            ]),
            actions=[
                ft.TextButton(text='Salvar',on_click=self.mudar_fs),
                ft.TextButton(text='Excluir',on_click=self.showdelete,data=0),
                ft.TextButton(text='Cancelar',on_click=self.close_banner),
            ]
        )
    def close_anchor(self,e):
        text = f'{e.control.data}'
        self.gene_ms.value += text+"+"
        self.gene_ms.close_view(self.gene_ms.value)
    def open_gene(self,e):
        self.gene_ms.open_view()

    def close_anchor_edit(self,e):
        text = f'{e.control.data}'
        self.gene_edit.value += text+"+"
        self.gene_edit.close_view(self.gene_edit.value)
    def open_gene_edit(self,e):
        self.gene_edit.open_view()
    def add_ms(self,e):
        ir = ()
        if self.name_ms.value == '':
            self.name_ms.error_text = 'Falta adicionar nome'
            self.name_ms.update()
        else:
            self.name_ms.error_text = ''
            ir+=(self.name_ms.value,)
        if self.gene_ms.value == '':
            #self.gene_ms.error_text = 'Falta adicionar genero'
            self.gene_ms.update()
        else:
            #self.gene_ms.error_text = ''
            if self.gene_ms.value[-1] == '+':
                ir+=(self.gene_ms.value[:-1],)
            else:
                ir+=(self.gene_ms.value,)
        if self.drop.value == '':
            self.drop.error_text = 'Falta'
            self.drop.update()
        else:
            self.drop.error_text = ''
            ir +=(self.drop.value,)
        if self.resumo.value == '':
            self.resumo.error_text = 'Falta adicionar sinopse'
            self.resumo.update()
        else:
            self.resumo.error_text = ''
            ir+=(self.resumo.value,)
        if self.date.value == '':
            self.date.error_text = 'Falta adicionar data de lançamento'
            self.date.update()
        else:
            self.date.error_text = ''
            ir+=(self.date.value,)
        
        if ir:
            #('nome', 'genero', 'filme', 'resumo resumo', '12/12/2024')
            c = ('nome','genero','categoria','resumo','data')
            add('msm',c,ir)
            self.page.update()
        else:pass
    def ver_data(self,e):
        if e.control.data == 0:
            raw_text = self.date.value
        else:
            raw_text = self.data_edit.value
        formatted_text = ""
        for i in range(len(raw_text)):
            if i == 2 or i == 4:
                formatted_text += "/"
            formatted_text += raw_text[i]
        if len(formatted_text) == 10:
            if e.control.data == 0:
                self.date.value = formatted_text
                self.date.update()
            else:
                self.data_edit.value = formatted_text
                self.data_edit.update()
        else:pass      
    def mostrar_fs(self,e):
        self.tabela.visible=True
        if e.control.data == 0:
            self.tb_fs.rows.clear()
            x = procura('msm',False,True,('filme'),'categoria')
        elif e.control.data == 1:
            self.tb_fs.rows.clear()
            x = procura('msm',False,True,('serie'),'categoria')
        elif e.control.data == 2:
            if self.pesquisa.value == '':
                self.pesquisa.error_text = 'Falta Pesquisa'
                self.pesquisa.update()
            elif self.drop_pesq.value == '':
                self.drop_pesq.error_text = 'Falta'
                self.drop_pesq.update()
            else:
                self.tb_fs.rows.clear()
                self.pesquisa.error_text = ''
                self.drop_pesq.error_text = ''
                x = procura('msm',False,True,(self.pesquisa.value),self.drop_pesq.value) #Colocar notificação de não encontrado
                self.pesquisa.value = ''
        else:
            self.tb_fs.rows.clear()
            x = procura_in('msm','categoria',('filme','serie'),True)
        if x:
            for item in x:
                self.tb_fs.rows.append(
                    ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            icon='delete',
                                            icon_color='red',
                                            data=item[0],
                                            on_click=self.showdelete
                                        ),
                                        ft.IconButton(
                                            icon='edit',
                                            icon_color='green',
                                            data=item,
                                            on_click=self.preview
                                        ),
                                    ])
                                ),
                                ft.DataCell(ft.Text(item[1],tooltip=item[4])),
                                ft.DataCell(ft.Text(value=item[2],width=200,tooltip=item[4])),
                                ft.DataCell(ft.Text(item[3],tooltip=item[4])),
                                ft.DataCell(ft.Text(item[6],tooltip=item[4])),
                            ],
                        ),
                    )
        else:pass
        self.tabela.update()
    def close_tabela(self,e):
        self.tabela.visible = False
        self.tabela.update()
    def showdelete(self,e):
        if e.control.data == 0:
            myid = self.myid.value[3:]
            myid = int(myid)
        else:
            myid = e.control.data
        excluir('msm','id',myid)
    def close_banner(self,e):
        self.conteudo.visible = True
        self.page.update()
        self.page.close(self.banner)
    def preview(self,e):
        self.conteudo.visible = False
        temp = e.control.data
        self.myid.value = f'ID:{temp[0]}'
        self.nome_edit.value = temp[1]
        self.data_edit.value = temp[6]
        self.drop_edit.value= temp[3]
        self.gene_edit.value = temp[2]
        self.res_edit.value = temp[4]
        self.page.open(self.banner)
        self.page.update()
    def mudar_fs(self,e):
        temp = self.myid.value[3:]
        temp = int(temp)
        c = ['nome','genero','categoria','resumo','data']
        v= [self.nome_edit.value,self.gene_edit.value,self.drop_edit.value,self.res_edit.value,self.data_edit.value]
        atualiza('msm',c,v,5,'id',temp)
        self.drop.value = ''
        self.drop_edit = ''
        self.page.close(self.banner)
        self.conteudo.visible = True
        self.page.update()

class drop(ft.Dropdown):
    def __init__(self,label,op1,op2,col):
        super().__init__()
        self.col = col
        self.label = label
        self.value = ''
        self.options = [
            ft.dropdown.Option(op1),
            ft.dropdown.Option(op2),
        ]
class music(ft.Container):
    def __init__(self,txt):
        super().__init__()
        self.padding = 15
        self.col = {'xs':4,'md':5}
# filds inputs
        self.name_music = ft.TextField(label='Nome',col={'xs':6})
        self.cantor = ft.TextField(label='Cantor',col={'xs':6})
        self.gene_music = ft.TextField(label='Genero',col={'xs':5})
        self.fav = ft.IconButton(icon='STAR_BORDER_PURPLE500_SHARP',col={'xs':1},on_click=self.por_fav,data='n')
# conteudo input
        self.conteudo = ft.ResponsiveRow(columns=12,controls=[
                    ft.Text('Musicas',style=ft.TextThemeStyle.HEADLINE_MEDIUM,text_align=ft.TextAlign.RIGHT),
                    ft.Text(text_align=ft.TextAlign.RIGHT,color='gray',style=ft.TextThemeStyle.LABEL_LARGE,spans=[
                        ft.TextSpan('Recomendação do dia: '),
                        ft.TextSpan(txt)
                    ]),
                    self.name_music,
                    self.cantor,
                    self.gene_music,
                    self.fav,
                    ft.TextButton(
                        on_click = self.add_music,
                        col = {'xs':3},
                        content=ft.Row(
                        tight=True,
                        controls=[
                            ft.Text(value='Adicionar',style=ft.TextTheme.body_large, color=ft.colors.PRIMARY ),
                            ft.Icon(name=ft.icons.ADD, size=14, color=ft.colors.PRIMARY)

                    ])
                    ),
                    
                    ft.TextButton(
                        col={'xs':3},
                        on_click=self.mostra_mu,
                        content=ft.Row(
                            tight=True,
                            controls=[
                                ft.Text(value='Lista Completa',style=ft.TextTheme.body_large, color=ft.colors.PRIMARY),
                                ft.Icon(name=ft.icons.ARROW_FORWARD_IOS, size=14, color=ft.colors.PRIMARY)
                            ])
                    )
                    ])
#tabela
        self.tb_mu= ft.DataTable(
            expand=True,
            data_row_min_height = 35,
            data_row_max_height=55,
            column_spacing=50,
            columns=[ft.DataColumn(label=ft.Text(value='Ações'),heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ft.DataColumn(ft.Text(value='Nome')), #
            ft.DataColumn(ft.Text(value='Genero'),heading_row_alignment=ft.MainAxisAlignment.CENTER), # 
            ft.DataColumn(ft.Text(value='Cantor')),],
            rows=[]
        )
        self.botoes =  ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
            ft.TextButton('Mais Recentes',on_click=self.mostra_mu,data=0),
            ft.TextButton('Favoritas',on_click=self.mostra_mu,data=1),
            ft.IconButton(icon='close',icon_color='red',on_click=self.close_banner,data=0)
        ])
#tabela + botoes
        self.tabela = ft.Column(col={'xs':12},visible=False,controls=[self.botoes,self.tb_mu])
# Content        
        self.content = ft.Column(
            spacing=15,
            run_spacing=15,
            #col={'xs':6,'lg':3},
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.conteudo,
                self.tabela
            ]
        )
# inputs e banner editação
        
        self.nome_edit = ft.TextField(label='Nome',col={'xs':6})
        self.cant_edit = ft.TextField(label='Cantor',col={'xs':6})
        self.gene_edit = ft.TextField(label='Genero',col={'xs':8})
        self.myid = ft.Text(value='',col={'xs':4},text_align=ft.TextAlign.CENTER,size=25)
        self.banner= ft.Banner(
            open=False,
            leading=ft.Icon(name='edit',color='purple',size=40),
            content_padding=15,
            margin=20,
            force_actions_below = True,
            content=ft.ResponsiveRow(columns=12,controls=[
                ft.Text('Edição de valores'),
                self.nome_edit, 
                self.cant_edit,
                self.gene_edit,
                self.myid
            ]),
            actions=[
                ft.TextButton(text='Salvar',on_click=self.mudar_mu),
                ft.TextButton(text='Excluir',on_click=self.showdelete,data=0),
                ft.TextButton(text='Cancelar',on_click=self.close_banner),
            ]
        )
        self.close_banner
    def por_fav(self,e):
        if self.fav.icon == 'STAR_BORDER_PURPLE500_SHARP':
            self.fav.data = 'favorito'
            self.fav.icon = 'STAR'
            self.fav.update()
        else:
            self.fav.icon = 'STAR_BORDER_PURPLE500_SHARP'
            self.fav.data = 'n'
            self.fav.update()   
    def favorita(self,e):
        myid = e.control.data
        myid = int(myid)
        if e.control.icon == 'STAR_BORDER_PURPLE500_SHARP':
            atualiza('msm',['resumo'],['favorito'],1,'id',myid)
            e.control.icon = "STAR"
            e.control.update()
        else:
            atualiza('msm',['resumo'],['n'],1,'id',myid)
            e.control.icon = 'STAR_BORDER_PURPLE500_SHARP'
            e.control.update()
    def close_banner(self,e):
        if e.control.data == 0:
            self.tabela.visible = False
        else:    
            self.page.close(self.banner)
        self.page.update()
    def add_music(self,e):
        ir = ()
        if self.name_music.value == '':
            self.name_music.error_text = 'Falta adicionar nome da musica'
            self.name_music.update()
        else:
            self.name_music.error_text = ''
            ir+=(self.name_music.value,)
        if self.gene_music.value == '':
            self.gene_music.error_text = 'Falta adicionar genero'
            self.gene_music.update()
        else: 
            self.gene_music.error_text = ''
            ir+=(self.gene_music.value,'musica',self.fav.data)  
        if self.cantor.value == '':
            self.cantor.error_text = 'Falta adicionar cantor'
            self.cantor.update()
        else: 
            self.cantor.error_text = ''
            ir+=(self.cantor.value,)
        if ir:
            print(ir) #('nome ', 'genero', 'musica', 'cantor')
            c = ('nome','genero','categoria',"resumo",'cantor')
            add('msm',c,ir)

        else:pass
    def mostra_mu(self,e):
        self.tabela.visible = True
        self.tabela.update()
        if e.control.data == 0:
            self.tb_mu.rows.clear()
            x = procura('msm',False,False,('musica'),'categoria')
        elif e.control.data == 1:
            self.tb_mu.rows.clear()
            x = procura('msm',False,True,('favorito'),'resumo')
        else:
            self.tb_mu.rows.clear()
            x = procura('msm',False,True,('musica'),'categoria')
        if x:
            for item in x:
                if item[4] == 'favorito':
                    icone = 'STAR'
                else: icone = 'STAR_BORDER_PURPLE500_SHARP'
                self.tb_mu.rows.append(
                    ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            icon='delete',
                                            icon_color='red',
                                            data=item[0],
                                            on_click=self.showdelete
                                        ),
                                        ft.IconButton(
                                            icon='edit',
                                            icon_color='green',
                                            data=item,
                                            on_click=self.abrir_banner
                                        ),
                                        ft.IconButton(
                                            icon=icone,
                                            data=item[0],
                                            on_click=self.favorita
                                        ),
                                    ])
                                ),
                                ft.DataCell(ft.Text(item[1])),
                                ft.DataCell(ft.Text(value=item[2])),
                                ft.DataCell(ft.Text(item[5])),
 
                            ],
                        ),
                    )
        else:pass
        self.tb_mu.update()
    def abrir_banner(self,e):
        temp = e.control.data
        if temp[4] == 'favorito':
            cor = ft.Colors.AMBER
        else: cor = ft.Colors.GREY
        self.myid.value = f'ID {temp[0]}'
        self.myid.color = cor
        self.nome_edit.value = temp[1]
        self.gene_edit.value = temp[2]
        self.cant_edit.value = temp[5]
        self.page.open(self.banner)
        self.page.update()
    def mudar_mu(self,e):
        myid = self.myid.value[3:]
        c = ['nome','genero','cantor']
        v = [self.nome_edit.value,self.gene_edit.value,self.cant_edit.value]
        atualiza('msm',c,v,3,'id',int(myid))
        self.page.close(self.banner)
        self.page.update()
    def showdelete(self,e):
        if e.control.data == 0:
            myid = self.myid.value[3:]
            myid = int(myid)
        else:
            myid = e.control.data
        excluir('msm','id',myid)