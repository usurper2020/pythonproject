def create_main_tab(self):
    """

    :param self:
    :type self:
    """
    main_tab = QWidget()
    main_layout = QVBoxLayout(main_tab)

    # Create a text box for the target website
    self.textbox.setPlaceholderText("Enter target website")
    main_layout.addWidget(self.textbox)

    # Add more UI elements as needed
    # ...

    self.tab_widget.addTab(main_tab, "Main")
