import flet as ft
from parts.appbar import Appbar
from parts.db import add,procura,quantidade
import math
from random import randint

##################### Falta tratar em mostrar a receita alem do update e delete
class Main_receitas(ft.View):
    def __init__(self,route:str,page):
        super().__init__()
        self.route = route
        self.page = page
        self.scroll = ft.ScrollMode.AUTO ### COLOCAR SCROLL
        self.appbar = Appbar(title='Livro de Receitas',page=page)
        self.nome = ft.TextField(label='Nome',col={'xs':6,'md':3})
        self.ingre = ft.TextField(label='Ingredientes',multiline=True,min_lines=1)
        self.prep=ft.TextField(label='Modo Preparo',multiline=True,min_lines=1)
        self.tempo = ft.TextField(label='Tempo de Preparo',col={'xs':12,'md':4},expand_loose=True)
        self.tag = ft.TextField(label='Tags',col={'xs':12,'md':4},expand_loose=True)
        self.obs =ft.TextField(label='Observações',col={'xs':12,'md':4},expand_loose=True)
        self.categ = drop(self)
        self.dif = outros_drops('Dificuldade',"Facil","Medio","Dificil",{'xs':6,'md':3})
        self.por = outros_drops('Porções',"Individual","2 Pessoas","Para a galera",{'xs':6,'md':3})
        self.input = ft.Container( 
            visible=False,
            padding=20,
            expand=True,
            border=ft.border.all(1),
            bgcolor = ft.colors.ON_INVERSE_SURFACE,
            content= ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=True,controls=[
                ft.Text(value='Adicionar nova receita',style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.ResponsiveRow(columns=12,alignment=ft.MainAxisAlignment.SPACE_AROUND,expand=True,controls=[
                    self.nome,
                    self.categ,
                    self.dif,
                    self.por,
                ]),
                self.ingre,
                self.prep,
                ft.ResponsiveRow(alignment=ft.MainAxisAlignment.SPACE_AROUND,expand=True,controls=[
                    self.tempo,
                    self.tag,
                    self.obs,
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[
                        ft.TextButton(text='Salvar',on_click=self.pre_add),
                        ft.TextButton(text='Cancelar',on_click=self.hide_input),
                    ])
            ])
        )
        #Pesquisa
        self.pesquisa = ft.TextField(label='Pesquisa',col={'xs':5,'md':4})
        self.filtro = outros_drops('Filtros','Categoria','Ingredientes','Tags',{'xs':2,'md':3})
        self.search = ft.ResponsiveRow(columns=14,spacing=10,run_spacing=8,vertical_alignment=ft.CrossAxisAlignment.CENTER,controls=[
            self.pesquisa,
            self.filtro,
            ft.IconButton(icon=ft.icons.SEARCH,col={'xs':1},on_click=self.all_recipe),
            ft.TextButton(col={'xs':2},text='Todos',on_click=self.all_recipe,data=True),
            ft.TextButton(col={'xs':2},text='Sozinho'),
            ft.TextButton(col={'xs':2},text='Galera'),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
        )
        self.tb = ft.DataTable(
            expand=True,
            columns=[
                ft.DataColumn(ft.Text(value='Ações')),
                ft.DataColumn(ft.Text(value='Nome')), #
                ft.DataColumn(ft.Text(value='Tempo de Preparo')), # 
                ft.DataColumn(ft.Text(value='Categoria')), # 
                ft.DataColumn(ft.Text(value='Facilidade')), #
                ft.DataColumn(ft.Text(value='Porções')), #
                ft.DataColumn(ft.Text(value='Tags')), #
            ],
            rows=[]
        )
    def all_recipe(self,e):
        if e.control.data == True:
            self.tb.rows.clear()
            x = procura('recipe',True)
        else:
            if self.pesquisa.value == '':
                self.pesquisa.error_text = 'Falta pesquisa'
                self.pesquisa.update()
                #x = procura('recipe',True) 
            elif self.filtro.value == '':
                self.pesquisa.error_text = ''
                self.tb.rows.clear()
                x = procura('recipe',False,True,self.pesquisa.value,'nome')
            else:
                self.pesquisa.error_text = ''
                if self.filtro.value == 'Categoria':
                    colu = 'categ'
                elif self.filtro.value == 'Ingredientes':
                    colu = 'ingre'
                else: colu = 'tag'
                self.tb.rows.clear()
                x = procura('recipe',False,True,self.pesquisa.value,colu)
        if x:    
            for item in x:
                self.tb.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon='create',
                                        icon_color='blue',
                                        data=item,
                                        #on_click=self.showedit
                                    ),
                                    ft.IconButton(
                                        icon='delete',
                                        icon_color='red',
                                        data=item[0],
                                        #on_click=self.showdelete
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.MORE_HORIZ_ROUNDED,
                                        icon_color='green',
                                        data=item,
                                        on_click=self.preview
                                    ),
                                ])
                            ),
                            ft.DataCell(ft.Text(item[0])),
                            ft.DataCell(ft.Text(item[3])),
                            ft.DataCell(ft.Text(item[6])),
                            ft.DataCell(ft.Text(item[7])),
                            ft.DataCell(ft.Text(item[8])),
                            ft.DataCell(ft.Text(item[4])),
                        ],
                    ),
                )
        else:pass
        self.tb.update()
    def preview(self,e):
        x = e.control.data 
        self.nome.value = x[0]
        self.por.value = x[8]
        self.tempo.value = x[3]
        self.ingre.value = x[1]
        self.prep.value =x[2]
        self.tag.value =x[4]
        self.dif.value =x[7]
        self.obs.value =x[5]
        self.categ.value = x[6]
        self.input.visible = True
        self.page.update()
    def pre_add(self,e):
        ir = ()
        if self.nome.value == '':
            self.nome.error_text = 'Falta adicionar nome'
            self.nome.update()
        else:
            self.nome.error_text = ''
            ir+=(self.nome.value,)
        if self.ingre.value == '':
            self.ingre.error_text = 'Falta adicionar os ingredientes'
            self.ingre.update()
        else:
            self.ingre.error_text = ''
            ir+=(self.ingre.value,)
        if self.prep.value == '':
            self.prep.error_text = 'Falta adicionar modo de preparo'
            self.prep.update()
        else:
            self.prep.error_text = ''
            ir+=(self.prep.value,)
        if self.tempo.value == '':
            self.tempo.error_text = 'Falta dizer o tempo de preparo'
            self.tempo.update()
        else:
            self.tempo.error_text = ''
            ir +=(self.tempo.value,)
        if self.tag.value == '':
            self.tag.error_text = 'Falta adicionar pelo menos 1 tag'
            self.tag.update()
        else:
            self.tag.error_text = ''
            ir+=(self.tag.value,)
        if self.obs.value == '':
            self.obs.error_text = 'Se não houver observações escreva 0'
            self.obs.update()
        else:
            self.obs.error_text = ''
            ir+=(self.obs.value,)
        if self.categ.value == '':
            self.categ.error_text = 'Falta definir categoria'
            self.categ.update()
        else:
            self.categ.error_text = ''
            ir+=(self.categ.value,)
        if self.dif.value == '':
            self.dif.error_text = 'Falta definir a dificuldade'
            self.dif.update()
        else:
            self.dif.error_text = ''
            ir+=(self.dif.value,)
        if self.por.value == '':
            self.por.error_text = 'Falta definir para quantas pessoas serve'
            self.por.update()
        else:
            self.por.error_text = ''
            ir+=(self.por.value,)
        if ir != ():
            add('recipe',("nome","ingre","prep","tempo","tag","obs","categ","dif","por"),ir)
        else: 
            pass
   
    def show_input(self,e):
        self.input.visible = True
        self.page.update()
    def hide_input(self,e):
        self.input.visible = False
        self.page.update()
    def build(self):
        dr =[]
        ld = procura('recipe',False,False,('drink'),'categ') # Buscar ultimo drink
        for item in ld:
            dr += item
        dnm,dct,ddf,dtp,dtg = dr[0],dr[6],dr[7],dr[3],dr[4]
        rr = []
        lr = procura('recipe',False,False,('salgado'),'tag') # Buscar ultimo prato salgado
        for item in lr:
            rr += item
        rnm,rct,rdf,rtp,rtg = rr[0],rr[6],rr[7],rr[3],rr[4]
        q = randint(1,quantidade('recipe','nome'))
        print(q)
        r = []
        ar = procura('recipe',False,True,(q),'ROWID')
        for item in ar:
            r += item
        anm,act,adf,atp,atg = r[0],r[6],r[7],r[3],r[4]
        return ft.ResponsiveRow(
            expand=True,
            controls=[
                self.input,
                ft.TextButton(text='Adicionar',on_click=self.show_input),
                recomenda(rnm,rct,rdf,rtp,rtg,'Ultimo Prato'),
                recomenda(dnm,dct,ddf,dtp,dtg,'Ultimo Drink'),
                recomenda(anm,act,adf,atp,atg,'Receita do Dia'),
                self.search,
                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[self.tb]),
            ])
class recomenda(ft.Container):
    def __init__(self,nome,categoria,dificuldade,tempo,tags,info): # add url para direcionar a receita completa
        super().__init__() 
        self.bgcolor = ft.colors.GREY_600
        self.col ={'xs':3,"md":4}
        base = ft.Column(spacing=15,run_spacing=15,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,spacing=15,controls=[
                #ft.Text(text_align=ft.TextAlign.START,value='Ultima adicionada '),
                ft.Text(value=nome,style=ft.TextTheme.label_medium,weight=ft.FontWeight.BOLD),
            ]),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[
                ft.Text(text_align=ft.TextAlign.JUSTIFY,value=categoria),
                ft.Text(text_align=ft.TextAlign.JUSTIFY,value=dificuldade),
            ]),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[
                ft.Text(text_align=ft.TextAlign.JUSTIFY,value='Tempo para prepararar'),
                ft.Text(text_align=ft.TextAlign.JUSTIFY,value=tempo),
            ]),
            ft.Text(value=tags),
            ft.TextButton(text='Ver Completa')
        ])
        self.content = ft.Stack(
            controls=[
                base,
                ft.Container(
                    bgcolor=ft.colors.PRIMARY,
                    content=ft.Text(value=info, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                    padding=ft.padding.symmetric(vertical=4, horizontal=40),
                    right=-30,
                    top=30,
                    rotate=ft.Rotate(angle=math.radians(40)),
                )
            ]
        )
class outros_drops(ft.Dropdown):
    def __init__(self,label,op1,op2,op3,col):
        super().__init__()        
        self.label = label
        self.col= col
        self.value = ''
        self.options=[
            ft.dropdown.Option(op1),
            ft.dropdown.Option(op2),
            ft.dropdown.Option(op3),
        ]
class drop(ft.Dropdown):#compleatar os outros itens
    def __init__(self,e):
        super().__init__()
        self.label = 'Categoria'
        self.col = {'xs':6,'md':3}
        self.value=''
        self.options= [
            ft.dropdown.Option("Drinks Alcoolicos"),
            ft.dropdown.Option("Acompanhamentos"),
            ft.dropdown.Option("Drinks Não Alcoolicos"),
            ft.dropdown.Option("Bolos"),
            ft.dropdown.Option("Doces Gelados"),
            ft.dropdown.Option("Tortas doces"),
            ft.dropdown.Option("Peixes"),
            ft.dropdown.Option("Bovinos"),
            ft.dropdown.Option("Suinos"),
            ft.dropdown.Option("Frutos do Mar"),
            ft.dropdown.Option("Caldos"),
            ft.dropdown.Option("Saladas"),
            ft.dropdown.Option("Molhos"),
            ft.dropdown.Option("Sopas"),
            ft.dropdown.Option("Sanduiches e Burguer"),
            ft.dropdown.Option("Petiscos e Entradas"),
            ft.dropdown.Option("Massas"),
            ft.dropdown.Option("Pãos"),
            ft.dropdown.Option("Tortas"),
            ft.dropdown.Option("Sobremessa"),


        ]
'''Opções dropdown:
Drink-> Alcoolicos e não alcoolicos (talvez criar subdivisão de drinks longos, para compartilhar, requinntados, etc)
Salgados-> Peixes, aves, carnes, saladas/molhos, sopas, caldos, sanduiches/burguer, petiscos, entradas, massas, tortas salgadas, veganos, vegie, frutos do mar
doces -> para compartilhar, bolos, tortas doces

'''