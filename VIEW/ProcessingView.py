from julesTk import view

__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class ProcessingView(view.View):

    def _prepare(self):
        # resize frame with window size
        self.configure_grid(self)
        self.configure_row(self, 0)
        self.configure_column(self, 0)
        # parent should also resize with window
        self.configure_row(self.parent, 0)
        self.configure_column(self.parent, 0)
        lbl = view.ttk.Label(self, text="hello world!", font=self.FONT_LARGE)
        self.add_widget("label1", lbl)
        lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)
        btn = view.ttk.Button(self, text="Click Me!", command=self.clicked)
        self.add_widget("button", btn)
        btn.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    def clicked(self):
        self.controller.ProcessingClick()