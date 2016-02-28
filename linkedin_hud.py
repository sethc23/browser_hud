class linkedin_hud:
    
    def __init__(self,hud,urls,linkedin_user='seth.t.chase@gmail.com'):
        
        self.bh = hud
        self.urls = urls
        self.current_url = self.urls[0]
        
        from os import environ as os_environ
        from os import path as os_path
        from sys import path as py_path
        py_path.append(os_path.join(os_environ['GIT_REPOS'],'emt/src'))

        from emt import EMT
        self.x = EMT()
        self.x.pg.check_db_config()
        self.x.web.initiate_web_session(linkedin_user)
        self.pg = self.x.pg
        self.T = self.pg.T
        
        

    def load_data(self):
        _html,_info = self.x.web.collect_and_save_data(self.current_url)
        for tag in _html.find_all('div',{'id':'profile'}):
            tag.attrs['style'] = "width: 100%"
        self.html = _html.renderContents()
        
    def integrate(self):
        self.load_data()
        D = []
        general_info_qry="select trait from general_traits"
        vals = self.x.pg.T.pd.read_sql(general_info_qry,self.x.pg.T.eng).trait.tolist()
        this_page = getattr(self.bh,'General')
        page_rows = this_page.children[0].children
        
        print page_rows
        
        work_info_qry = """
            select 
                company, t_company.rank company_rank,
                job_title,  t_job_title.rank job_title_rank
            from (
                select 
                    entries->>'company' company,
                    entries->>'title' job_title
                from 
                    (
                    select jsonb_array_elements((json_info->>'work')::jsonb) entries
                    from candidates 
                    where json_info->>'url'='%s'
                    ) f1
            ) f2
            inner join traits t_company on t_company.trait=company
            inner join traits t_job_title  on t_job_title.trait=job_title
            """ % self.current_url
        school_info_qry = """
            select 
                school, t_school.rank school_rank,
                major,  t_major.rank major_rank,
                degree, t_degree.rank degree_rank
            from (
                select 
                    entries->>'institution' school,
                    entries->>'major' major,
                    entries->>'degree' degree
                from 
                    (
                    select jsonb_array_elements((json_info->>'school')::jsonb) entries
                    from candidates 
                    where json_info->>'url'='%s'
                    ) f1
            ) f2
            inner join traits t_school on t_school.trait=school
            inner join traits t_major  on t_major.trait=major
            inner join traits t_degree on t_degree.trait=degree
            """ % self.current_url
        
        
        
        
    def load_url(self,position=''):
        
        def check_button_style():
            if self.current_url==self.urls[0]:
                _prev,_next,_exit = bh.menu_bar.children
                _prev._dom_classes = ['faded']
                _next._dom_classes = ()
            elif self.current_url==self.urls[-1]:
                _prev,_next,_exit = bh.menu_bar.children
                _prev._dom_classes = ()
                _next._dom_classes = ['faded']
            else:
                _prev,_next,_exit = bh.menu_bar.children
                _prev._dom_classes = ()
                _next._dom_classes = ()
            bh.set_css()
        
        if not position:
            self.current_url = self.urls[0]
        elif position=='prev':
            if self.urls.index(self.current_url)==0:
                return
            self.current_url = self.urls[ self.urls.index(self.current_url)-1 ]
        elif position=='next':
            if self.urls.index(self.current_url)==len(self.urls)-1:
                return
            self.current_url = self.urls[ self.urls.index(self.current_url)+1 ]


        check_button_style()
        clear_output()
        get_ipython().run_cell_magic(u'html', u'',self.html)