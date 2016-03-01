class linkedin_hud:
    
    def __init__(self,hud,linkedin_user='seth.t.chase@gmail.com'):
        
        self.bh = hud

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
        
    def integrate(self,urls=[]):
        self.urls = urls
        self.current_url = self.urls[0]
        
        def general_page():
            opts = self.T.pd.read_sql("select trait from general_traits",
                                      self.T.eng).trait.tolist()
            fresh_opts = sorted([it.replace('_',' ').title() for it in opts])
            widget_component = self.bh.components['General_category']
            current_list = list(widget_component.options)
            new_list = fresh_opts
            new_list.insert(0,current_list[0])
            new_list.extend(current_list[1:])
            widget_component.options=tuple(new_list)  
        def trait_pages():

            def get_work_df():
                qry = """
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
                opts=self.T.pd.read_sql(qry,self.T.eng)

                hud_df = self.T.pd.DataFrame(columns=['trait','score'])
                for t in ['company','job_title']:
                    x = opts.ix[:,[t,'%s_rank' % t]].rename(columns={t:'trait','%s_rank' % t:'score'})
                    hud_df=hud_df.append(x,ignore_index=True)
                return hud_df
            def get_school_df():
                qry = """
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
                opts=self.T.pd.read_sql(qry,self.T.eng)

                hud_df = self.T.pd.DataFrame(columns=['trait','score'])
                for t in ['school','major','degree']:
                    x = opts.ix[:,[t,'%s_rank' % t]].rename(columns={t:'trait','%s_rank' % t:'score'})
                    hud_df=hud_df.append(x,ignore_index=True)
                return hud_df

            def push_data_to_hud(hud_df,hud_page=''):
                new_traits = hud_df[hud_df.score.isnull()].apply(lambda a: self.T.json.dumps({'trait':a.trait}),axis=1).tolist()
                scored_traits = hud_df[hud_df.score.isnull()==False].copy()
                scored_traits['score'] = scored_traits.score.map(int)
                scored_traits = scored_traits.apply(lambda a: self.T.json.dumps(a.to_dict()),axis=1).tolist()
                
                self.bh.components['%s_new_traits' % hud_page].options = new_traits
                self.bh.components['%s_scored_traits' % hud_page].options = scored_traits
            
            hud_df = get_work_df()
            push_data_to_hud(hud_df,hud_page='Work')
            
            hud_df = get_school_df()
            push_data_to_hud(hud_df,hud_page='School')
        
        general_page()
        trait_pages()
        
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