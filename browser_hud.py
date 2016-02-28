# Widget Setup
import ipywidgets as widgets
from IPython.display import display,HTML,clear_output
import json

class browser_hud:
    
    def __init__(self):
        self._widget = widgets.Box(_dom_classes=['inspector'])
        self._widget.overflow_x = 'scroll'
        self._widget.overflow_y = 'scroll'

    def set_css(self):
        """
        
        { Top Right Bottom Left }
        
        """

        get_ipython().run_cell_magic(u'html', u'', 
                                     '\n'.join([u'<link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css">',
                                                u'<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css">',
                                                u'<style>\n %s ;\n</style>' % 
                                                ','.join(['.faded { opacity: 0.3}',
                                                           '.prev_btn { }',
                                                           '.next_btn { }',
                                                           '.exit_btn { }',
                                                           '.menu_bar { }',
                                                           '.selected_tab { }',
                                                           '.unselect_tab { }',
                                                           '.comment {  }',
                                                           ".score { 'margin-left': 60px }",
                                                           ".category { 'margin-left': 60px }",
                                                           ".trait { 'margin-left': 4px }",
                                                           ".update_btn_1 { 'visibility': 'hidden','display':'block' }",
                                                           ".col_b { 'margin-left': 2%, 'flex-direction': 'column' }",
                                                           ".row2_b { 'align-items': 'flex-start'}",
                                                           #".update_button { 'margin-left': 100px }",
                                                           #"""div[class$="score"] {
                                                           #       width: '10%', 
                                                           #       display: '-webkit-inline-box'
                                                           #   }""", 

                                                          ])
                                                ])
                                     )
        
    
    def page_click(self,button):
        page = button.from_page
        this_page = getattr(self,page)
        page_rows = this_page.children[0].children
        if page.lower()=='general':
            update_row = page_rows[0].children
            scored_traits = page_rows[1].children[0]
        else:
            update_row = page_rows[1].children
            scored_traits = page_rows[0].children[2]
            new_traits = page_rows[0].children[0]
        
        button_type=button.description.lower()
        if button_type.count('update'):
            new_traits = {}
            for it in update_row:
                if not it._view_name.lower().count('button'):
                    new_traits.update({it.description:it.value})                     
                    if it._view_name=='DropdownView':
                        it.value=it.options[0]
                    elif it._view_name.count('Int'):
                        it.value=0
                    else:
                        it.value=''
            new_traits = json.dumps(new_traits, ensure_ascii=False)
            _options = [] if not scored_traits.options else list(scored_traits.options)
            _options.append(new_traits)
            scored_traits.options = _options
            
        
        elif button_type.count('edit'):
            edit_idx = scored_traits.options.index(scored_traits.value)
            old_traits = list(scored_traits.options)
            edit_dict = eval(old_traits.pop(edit_idx))
            scored_traits.options = old_traits

            for it in update_row:
                if edit_dict.has_key(it.description):
                    it.value = edit_dict[it.description]

        elif button_type.count('score'):
            
            edit_idx = new_traits.options.index(new_traits.value)
            new_traits = list(new_traits.options)
            edit_dict = eval(new_traits.pop(edit_idx))
            new_traits.options = new_traits

            for it in update_row:
                if edit_dict.has_key(it.description):
                    it.value = edit_dict[it.description]
                    
    
    def make_general_page(self,page_title='General'):
        
        def dropdown_check(choice):
            D = {'old':'','new':''}
            if choice['old'] and type(choice['old'])==unicode:
                D['old'] = choice['old']
            if choice['new'] and type(choice['new'])==unicode:
                D['new'] = choice['new']
            if [it for it in D.values() if it]:
                this_page = bh.General
                second_col = this_page.children[0].children[1]
                children_list = list(second_col.children)
                if D['new']=='(New)':
                    new_category = widgets.Text(description='(New)')
                    children_list.append(new_category)
                if D['old']=='(New)':
                    children_list.pop(-1)
                second_col.children = tuple(children_list)
                
        add_button = widgets.Button(description='ADD',
                                       tooltip='Add to Stored Comments',
                                       _dom_classes=['add_button'],
                                       from_page=page_title)
        add_button.on_click(self.page_click)
        
        cmt = widgets.Textarea(description='Comment')
        score = widgets.BoundedIntText(description='Score',
                                       min=0,
                                       max=5)
        score.width='50px'
        
        saved_comments = widgets.Select(description='Stored Comments')
        edit_button = widgets.Button(description='EDIT',
                                     tooltip='Edit a Stored Comment',
                                     from_page=page_title)
        edit_button.on_click(self.page_click)

        

        category = widgets.Dropdown(description='Category',
                                    options=['Not Specified','(New)'])
        category.observe(dropdown_check)
        
        col1 = add_button
        col1.margin = '5px 25px 0px 5px'
        cmt.margin = '5px 0px 5px 0px'
        col2 = widgets.VBox([cmt,widgets.HBox([score,category])])
        col2.margin = '5px 0px 5px 0px'
        col3 = saved_comments
        col3.margin =  '5px 0px 5px 25px'
        col4 = edit_button
        col4.margin =  '5px 0px 5px 0px'


        row = widgets.HBox([col1,col2,col3,col4])

        # row1 = widgets.HBox(children=[ add_button,cmt,score,category ],
        #                     pack='start',align='start',
        #                     padding='10px 0px 10px 0px')
        # row2 = widgets.HBox(children=[ saved_comments,edit_button ],
        #                     padding='10px 0px 10px 0px')
        # rows = widgets.VBox(children=[ row1,row2 ],align='center')
        return widgets.Box(children=[row],description=page_title)

    def make_trait_scoring_page(self,page_title='Traits'):
        
        new_traits = widgets.Select(description='New Traits')
        score_button = widgets.Button(description='EDIT NEW',
                                      from_page=page_title)
        score_button.on_click(self.page_click)
        
        scored_traits = widgets.Select(description='Scored Traits')
        edit_button = widgets.Button(description='EDIT',
                                     from_page=page_title)
        edit_button.on_click(self.page_click)
        
        
        cmt = widgets.Textarea(description='Comment')
        score = widgets.BoundedIntText(description='Score',
                                       min=0,
                                       max=5,
                                       _dom_classes=['score'])
        score.width = '50px'
        trait = widgets.Text(description='Trait',disable=True)
        update_button = widgets.Button(description='UPDATE',
                                       tooltip='Increase Points',
                                       from_page=page_title)
        update_button.on_click(self.page_click)
        
        # r1_col1 = update_button
        # r1_col1.margin = '5px 25px 0px 5px'
        # cmt.margin = '0px 0px 5px 0px'
        # score.margin = '0px 0px 5px 0px'
        # r1_col2 = cmt
        # # widgets.VBox([ cmt,score,trait ])
        # r1_col2.margin = '5px 0px 5px 0px'
        # # new_traits.height = '81px'
        # # new_traits.margin = '0px 5px 5px 0px'
        # # scored_traits.margin = '0px 5px 0px 0px'
        # # scored_traits.height = '81px'
        # r1_col3 = new_traits

        r1_col1 = update_button
        r1_col1.margin = '5px 25px 0px 5px'
        r2_col1 = widgets.Button(description='UPDATE')
        r2_col1._dom_classes = ['update_btn_1']
        r2_col1.margin = r1_col1.margin
        
        cmt.height = '81px'
        r1_col2 = cmt
        r1_col2.margin = '5px 0px 5px 0px'
        r1_col2.height = '81px'

        score.margin = '0px 0px 10px 0px'
        r2_col2 = widgets.VBox([ score,trait ])
        # r2_col2.pack = 'baseline'
        r2_col2.margin = r1_col2.margin
        r2_col2.height = cmt.height


        new_traits.margin = cmt.margin
        new_traits.height = cmt.height
        r1_col3 = new_traits
        r1_col3.margin = '5px 0px 5px 0px'
        
        scored_traits.height = cmt.height
        r2_col3 = scored_traits
        r2_col3.height = r2_col2.height
        r1_col3.margin = r1_col3.margin

        r1_col4 = widgets.VBox([score_button])
        r1_col4.width = '95px'
        r1_col4.margin = '5px 0px 0px 0px'
        r2_col4 = widgets.VBox([edit_button])
        r2_col4.width = r1_col4.width
        r2_col4.height = r2_col3.height
        r2_col4.orientation='horizontal'
        r2_col4.pack='end'
        r2_col4.align='start'

        
        
        

        # col1 = widgets.VBox([r1_col1,r2_col1])
        # col2 = widgets.VBox([r1_col2,r2_col2])
        # col3 = widgets.VBox([r1_col3,r2_col3])
        # col4 = widgets.VBox([r1_col4,r2_col4])

        row1_a = widgets.HBox([r1_col1,r1_col2])
        row2_a = widgets.HBox([r2_col1,r2_col2])

        col_a = widgets.VBox([row1_a,row2_a])

        row1_b = widgets.HBox([r1_col3,r1_col4])
        row1_b.pack='end'
        row1_b.align='end'
        row2_b = widgets.HBox([r2_col3,r2_col4])
        # row2_b._dom_classes = ['row2_b']
        row2_b.pack='end'
        row2_b.align='end'

        


        col_b = widgets.VBox([row1_b,row2_b])
        col_b.pack='end'
        col_b.align='end'
        # col_b._dom_classes = ['col_b']
        # col_b.pack='end'
        # col_b.align='start'

        row = widgets.HBox([col_a,col_b])
        # new_box = widgets.HBox([new_traits,score_button])
        # new_box.align = 'stretch'
        # stored_box = widgets.HBox([scored_traits,edit_button])
        # stored_box.align = 'stretch'
        # col3 = widgets.VBox([new_box,stored_box])



        # col3 = widgets.VBox([new_traits,scored_traits])
        # col3.margin =  '5px 0px 5px 25px'
        # col3.align='end'
        # col4 = widgets.VBox([score_button,edit_button])
        # col4.margin =  '5px 0px 5px 0px'
        # # col4.align='end'
        # col4.orientation='vertical'
        # col4.pack='stretch'




        # row = widgets.HBox([col1,col2,col3,col4])
        # col = widgets.VBox([row1,row2])


        # row1 = widgets.HBox(children=[ new_traits,score_button,scored_traits,edit_button ],
        #                     padding='10px 0px 10px 0px')
        # row2 = widgets.HBox(children=[ cmt,score,trait,update_button ],
        #                     pack='start',align='start',
        #                     padding='10px 0px 10px 0px')
        # rows = widgets.VBox(children=[ row1,row2 ],align='center')

        return widgets.Box(children=[row],description=page_title)

    def make_tabs(self,_pages):
        tabs = widgets.Tab(children=_pages)
        tabs.background_color = '#fff'
        tabs.border_color = '#ccc'
        tabs.border_width = 1
        tabs.border_radius = 5
        
        for i in range(len(tabs.children)):
            it=tabs.children[i]
            if it.__dict__.has_key('description'): 
                tabs.set_title(i, it.description)
                
        return tabs

    def make_menu_bar(self):
        
        def click(b):
            if b.description.lower().count('prev'):
                self.load_url('prev')
            elif b.description.lower().count('next'):
                self.load_url('next')
            elif b.description.lower().count('exit'):
                self._widget.close()
        
        prev_button=widgets.Button(description='<<--  PREV',
                                   margin = '0% 2% 0% 2%',
                                   background_color='#3BBAF5',
                                   padding = 4,
                                   _dom_classes=['prev_btn'])
        prev_button.on_click(click)
        
        next_button=widgets.Button(description='NEXT -->>',
                                   margin = '0% 0% 0% 0%',
                                   background_color='#3BBAF5',
                                   padding = 4,
                                   _dom_classes=['next_btn'])
        next_button.on_click(click)
        
        exit_button=widgets.Button(description='EXIT',
                                   margin = '0% 0% 0% 70%',
                                   background_color = '#FA7676',
                                   padding = 4,
                                   _dom_classes=['exit_btn'])                          
        exit_button.on_click(click)
        
        menu_bar = widgets.HBox(children=[ prev_button,next_button,exit_button ],
                                padding=4,
                                align='center',
                               _dom_classes=['menu_bar'])
        return menu_bar

    def make_widget(self,_children):
        x = self._widget
        x.children = _children
        x._dom_classes = ['inspector']
    
    def remake_widget(self,children):
        self._widget.__init__(children)

    def display_widget(self):
        display(self._widget)
        get_ipython().run_cell_magic(u'javascript', u'', 
                                     u"""$('div.inspector').detach().prependTo($('body'))
                                         .css({ 'z-index': 999,           
                                                position: 'fixed',
                                                'box-shadow': '5px 5px 12px 3px black',
                                                'min-width': '50%',
                                                opacity: 0.9, 
                                                width: '85%', 
                                                height: '300px', 
                                                left: '7.5%',
                                                bottom: '50px'
                                                }).draggable({scroll: 'true'}).resizable();""")
    
    def close(self):
        self._widget.close()
        

    def start(self):
        self.General = self.make_general_page(page_title='General')
        self.Work = self.make_trait_scoring_page(page_title='Work')
        self.School = self.make_trait_scoring_page(page_title='School')
        self.menu_bar = self.make_menu_bar()
        self.tabs = self.make_tabs([self.General,self.Work,self.School])
        self.make_widget([self.menu_bar,self.tabs])
        self.set_css()
        self.display_widget()
        global bh
        bh = self
        return bh



