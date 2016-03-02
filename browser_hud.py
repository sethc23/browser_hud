# Widget Setup
import ipywidgets as widgets
from IPython.display import display,HTML,clear_output
import json
from time import sleep
from IPython import get_ipython
from py_classes import To_Class

class browser_hud:
    
    def __init__(self,display_type=''):
        self.widget = widgets.Box(_dom_classes=['inspector'])
        self.widget.overflow_x = 'hidden'
        self.widget.overflow_y = 'hidden'
        self.widget.background_color='#444648'
        if display_type:
            self.display_type = display_type
        else:
            self.display_type = 'float'

    def _get_all_components(self,_dict,_widget):
        """
            Recursively iterates through all children, 
                updating the 'parent' attribute of each child, and
                returning an object containing all children.
        """
        for c in _widget.children:
            
            try:
                c.parent = _widget
            except:
                print c
                print _widget.children
                c.parent = _widget

            if hasattr(c,'id'):
                _dict.update({c.id:c})

            if hasattr(c,'children'):
                _dict = self._get_all_components(_dict,c)

        return _dict

    def set_color_scheme(self,_scheme,_objects=[]):
        for it in _objects:
            for k,v in _scheme.iteritems():
                setattr(it,k,v)
        return _objects

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
                                                           ".menu_bar { 'line-height': 5px }",
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
        get_ipython().run_cell_magic(u'javascript', u'',
                                     u"""
                                     $('button.update_btn_1').css('visibility', 'hidden');
                                     $('.widget-label').css('color', '#53D2FF');
                                     $('.widget-readout').css('color', '#53D2FF');
                                     $('button.menu_bar_btn').css('line-height', '5px');
                                     $("div.inspector").mouseover(function() {
                                            $(this).css("overflow-y","scroll");
                                        }).mouseout(function() {
                                            $(this).css("overflow-y","hidden");
                                        });
                                     """)
        # open external -- #pager-button-area > a:nth-child(1)
        # close pager -- pager-button-area > a:nth-child(2)
        get_ipython().run_cell_magic(u'javascript', u'',
                                     u"""
                                     var external_button = $('#pager-button-area > a:nth-child(1)');
                                     external_button.onclick = external_button_click;
                                    function external_button_click() {
                                        var a = IPython.notebook.get_cell(0);
                                        a.focus_cell();
                                        IPython.notebook.execute_cell(0);
                                    };
                                    """)
           
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
                second_col = self.widget.components.General_category.parent
                children_list = list(second_col.children)
                category_idx = children_list.index(self.widget.components.General_category)
                if D['new']=='(New)':
                    new_category = widgets.Text(description='(New)',
                                                id='%s_new_category'%page_title,
                                                padding=col_item_padding,
                                                width=box_width)
                    children_list.insert(category_idx + 1, new_category)
                if D['old']=='(New)':
                    children_list.pop(category_idx + 1)
                second_col.children = tuple(children_list)
                self.set_css()
        
        col_item_padding = '5px 0px 5px 0px'  

        add_button = widgets.Button(description='ADD',
                                       tooltip='Add to Stored Comments',
                                       _dom_classes=['add_button'],
                                       from_page=page_title,
                                       id='%s_add_button'%page_title)
        add_button.on_click(self.page_click)
        
        cmt = widgets.Textarea(description='Comment',
                               id='%s_comment'%page_title,
                               padding=col_item_padding)
        score = widgets.IntSlider(description='Score',
                                  min=0,
                                  max=5,
                                  id='%s_score'%page_title,
                                  padding=col_item_padding)
        saved_comments = widgets.Select(description='Stored Comments',
                                        id='%s_stored_comments'%page_title)
        edit_button = widgets.Button(description='EDIT',
                                     tooltip='Edit a Stored Comment',
                                     from_page=page_title,
                                     id='%s_edit_button'%page_title)
        edit_button.on_click(self.page_click)
        category = widgets.Dropdown(description='Category',
                                    options=['Not Specified','(New)'],
                                    id='%s_category'%page_title)
        category.observe(dropdown_check)

        color_scheme =  {'background_color': '#75715e',
                         'color': '#a6e22e',
                         'font_family': u'verdana',
                         'font_size': u'14px',
                         'font_weight': u'bold'}
        self.set_color_scheme(color_scheme,[add_button,edit_button])

        box_width = '250px'
        box_height = '81px'
        slider_width = '220px'
        button_width = '95px'
        

        cmt.height = box_height
        cmt.width = box_width
        score.width = slider_width
        saved_comments.height = box_height
        saved_comments.width = box_width
        

        col1 = add_button
        col1.margin = '5px 25px 0px 5px'
        cmt.margin = '5px 0px 5px 0px'
        col2 = widgets.VBox([category,score,cmt],id='%s_col2'%page_title)
        col2.margin = '5px 0px 5px 0px'
        col3 = saved_comments
        col3.margin =  '5px 0px 5px 25px'
        col4 = edit_button
        col4.margin =  '5px 0px 5px 0px'

        row = widgets.HBox([col1,col2,col3,col4])
        return widgets.Box(children=[row],description=page_title,id='%s_page'%page_title)

    def make_trait_scoring_page(self,page_title='Traits'):
        
        col_item_padding = '5px 0px 5px 0px' 

        new_traits = widgets.Select(description='New Traits',
                                    id='%s_new_traits'%page_title)
        score_button = widgets.Button(description='EDIT NEW',
                                      from_page=page_title,
                                      id='%s_score_button'%page_title)
        score_button.on_click(self.page_click)
        
        scored_traits = widgets.Select(description='Scored Traits',
                                       id='%s_scored_traits'%page_title)
        edit_button = widgets.Button(description='EDIT',
                                     from_page=page_title,
                                     id='%s_edit_button'%page_title)
        edit_button.on_click(self.page_click)
        
        
        cmt = widgets.Textarea(description='Comment',
                               id='%s_comments'%page_title,
                               padding=col_item_padding)

        trait = widgets.Text(description='Trait',value='',
                             disabled=True,
                             id='%s_trait'%page_title,
                             padding=col_item_padding)
        
        score = widgets.IntSlider(description='Score',
                                  min=0,
                                  max=5,
                                  id='%s_score'%page_title,
                                  padding=col_item_padding)

        update_button = widgets.Button(description='UPDATE',
                                       tooltip='Increase Points',
                                       from_page=page_title,
                                       id='%s_update_button'%page_title)
        update_button.on_click(self.page_click)
        fake_button = widgets.HBox()
        

        color_scheme =  {'background_color': '#75715e',
                         'color': '#a6e22e',
                         'font_family': u'verdana',
                         'font_size': u'14px',
                         'font_weight': u'bold'}
        self.set_color_scheme(color_scheme,[score_button,edit_button,update_button,fake_button])

        box_width = '250px'
        box_height = '81px'
        slider_width = '220px'
        button_width = '95px'

        update_button.width = button_width
        fake_button.width = button_width
        trait.width = box_width
        score.width = slider_width        
        cmt.width = box_width
        cmt.height = box_height
        new_traits.margin = cmt.margin
        new_traits.height = box_height
        new_traits.width = box_width
        scored_traits.height = box_height
        scored_traits.width = box_width

        r1_col1 = update_button
        r1_col1.margin = '5px 0px 0px 5px'
        r2_col1 = fake_button
        r2_col1.margin = r1_col1.margin
        
        r1_col2 = widgets.VBox([ trait,score ])
        r1_col2.margin = '0px 0px 5px 0px'
        r1_col2.height = box_height
        
        r2_col2 = cmt
        r2_col2.margin = '5px 0px 5px 0px'
        r2_col2.height = box_height

        r1_col3 = new_traits
        r1_col3.margin = '5px 0px 5px 0px'
        
        
        r2_col3 = scored_traits
        r2_col3.height = r2_col2.height
        r1_col3.margin = r1_col3.margin

        r1_col4 = widgets.VBox([score_button])
        r1_col4.width = button_width
        r1_col4.margin = '5px 0px 0px 10px'
        r1_col4.pack='start'
        r1_col4.align='end'

        r2_col4 = widgets.VBox([edit_button])
        r2_col4.width = r1_col4.width
        r2_col4.margin = r1_col4.margin
        r2_col4.height = r2_col3.height
        r2_col4.orientation='horizontal'
        r2_col4.pack='end'
        r2_col4.align='start'

        row1_a = widgets.HBox([r1_col1,r1_col2])
        row2_a = widgets.HBox([r2_col1,r2_col2])

        col_a = widgets.VBox([row1_a,row2_a])
        # col_a.margin = '0px 10px 0px 0px'

        row1_b = widgets.HBox([r1_col3,r1_col4])
        row1_b.pack='end'
        row1_b.align='start'
        row2_b = widgets.HBox([r2_col3,r2_col4])
        row2_b.pack='end'
        row2_b.align='end'

        col_b = widgets.VBox([row1_b,row2_b])
        col_b.pack='end'
        col_b.align='end'

        row = widgets.HBox([col_a,col_b])
        return widgets.Box(children=[row],description=page_title,id='%s_page'%page_title)

    def make_tabs(self,_pages):
        tabs = widgets.Tab(children=_pages,id='tabs')
        tabs.background_color='#444648'
        tabs.font_family='verdana'
        tabs.font_weight='bold'
        tabs.font_size='14px'
        tabs.color='#DC44FF'
        
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
                self.close_widget()

        prev_button=widgets.Button(description='<<--  PREV',
                                   background_color='#3BBAF5',
                                   _dom_classes=['prev_btn','menu_bar_btn'],
                                   id='prev_button')
        prev_button.on_click(click)
        
        
        next_button=widgets.Button(description='NEXT -->>',
                                   background_color='#3BBAF5',
                                   _dom_classes=['next_btn','menu_bar_btn'],
                                   id='next_button')
        next_button.on_click(click)
        
        exit_button=widgets.Button(description='EXIT',
                                   background_color = '#FA7676',
                                   _dom_classes=['exit_btn','menu_bar_btn'],
                                   id='exit_button')
        exit_button.on_click(click)


        color_scheme = {'background_color':'#D95D18',
                        'font_family':'verdana',
                        'font_weight':'bold',
                        'font_size':'14px',
                        'color':'#f8f8f2'}
        for it in [prev_button,next_button,exit_button]:
            for k,v in color_scheme.iteritems():
                setattr(it,k,v)
        
        button_height = '20px'
        prev_button.height = button_height
        next_button.height = button_height
        exit_button.height = button_height
        # prev_button.margin = '0% 0% 0% 0%'
        # next_button.margin = '0% 0% 0% 0%'
        exit_button.margin = '0px 0px 0px 15px'

        col1 = widgets.HBox()
        col1.width = '33%'
        col2 = widgets.HBox([prev_button,next_button])
        col2.width = '33%'
        col2.pack='center'
        col2.align='center'
        col3 = widgets.HBox([exit_button])
        col3.width = '33%'
        col3.margin = '0% 0% 0% 25%'
        # col3.pack = 'end'
        # col3.align = 'end'
        menu_bar = widgets.HBox(children=[ col1,col2,col3 ],
                               _dom_classes=['menu_bar'],id='menu_bar')

        menu_bar.padding = '4px'
        # menu_bar.pack='center'
        return menu_bar

    def display_widget(self):
        self.set_css()
        display(self.widget)
        if self.display_type=='float':
            get_ipython().run_cell_magic(u'javascript', u'',u"$('#pager').height('280px');$('#pager').hide();")
            get_ipython().run_cell_magic(u'javascript', u'', 
                                         u"""$('div.inspector').detach().prependTo($('body'))
                                            .css({ 'z-index': 999,           
                                                position: 'fixed',
                                                'box-shadow': '5px 5px 12px 3px black',
                                                'min-width': '50%',
                                                opacity: 0.9, 
                                                left: '15%',
                                                bottom: '50px'
                                                })
                                            .draggable({
                                            
                                                })
                                            .resizable({
                                                autoHide: 'true',
                                                handles: "all",
                                                });
                                            """)
        elif self.display_type=='pager':
            get_ipython().run_cell_magic(u'javascript', u'',u"$('#pager').height('280px');$('#pager').show();")
            get_ipython().run_cell_magic(u'javascript', u'',u"$('div.inspector').prependTo($('#pager-container'));" )
            get_ipython().run_cell_magic(u'javascript', u'',u"$('#pager-container > pre').hide();")
        self.set_css()
        if hasattr(self,'start_container'):
            self.start_container.close()                         
    
    def close_widget(self,display_type=''):
        get_ipython().run_cell_magic(u'javascript', u'',u"$('#pager').hide();")
        self.widget.close()
        self.create_start_hud_button(self.display_type)
        
    def create_start_hud_button(self,display_type):
        self.start_button = widgets.Button(description='START HUD')
        self.start_button.background_color = '#30FA34'

        def click_start_hud_btn(b):
            self.display_type = self.start_container.display_type
            self.start_container.close()
            self.start_button.close()
            get_ipython().run_cell_magic(u'javascript', u'',u"$('div.start_button_container').remove();")
            self.display_type = 'float' if self.display_type=='pager' else 'pager'
            browser_hud(self.display_type).start_hud()

        self.start_button.on_click(click_start_hud_btn)

        self.start_container = widgets.Box([self.start_button],_dom_classes=['start_button_container'])
        self.start_container.height='40px'
        self.start_container.width='70px'
        self.start_container.display_type = self.display_type

        display(self.start_container)
        get_ipython().run_cell_magic(u'javascript', u'', 
                                                 u"""$('div.start_button_container').detach().prependTo($('body'))
                                                     .css({ 'z-index': 999,           
                                                            position: 'fixed',
                                                            bottom: '10%',
                                                            left: '50px',
                                                            });""")

    def start_hud(self,**kwargs):
        
        make_display = True if not kwargs.has_key('make_display') else kwargs['make_display']

        menu_bar = self.make_menu_bar()
        general = self.make_general_page(page_title='General')
        work = self.make_trait_scoring_page(page_title='Work')
        school = self.make_trait_scoring_page(page_title='School')
        tabs = self.make_tabs([general,work,school])
        
        self.widget.children = [menu_bar,tabs]
        self.widget.components = To_Class(self._get_all_components({},self.widget))
        self.set_css()
        if make_display:
            self.display_widget()

        global bh
        bh = self
        return bh



