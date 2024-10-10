titleStyle = """
QLabel {
    color: #929292;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 10px;
}
"""
labelStyle = """
QLabel {
    color: #76D4D4;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 12px;
    margin-top:10px;
}
"""

signalChooseStyle = """
QComboBox{
    background-color: rgba(0, 0, 0, 0);
    color: #76D4D4;
    border: none;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 14px;
    height:30px;
}
QComboBox::drop-down {

}
QComboBox::down-arrow {
    image: url(Assets/RightPanel/dropdownArrowColor.png);
    
}

QComboBox QAbstractItemView {
    background-color: #2D2D2D;
    color: #76D4D4;
    selection-background-color: #EFEFEF;
    selection-color: #2D2D2D;
    border: none;
}
"""
colorSignalChooseStyle = """
QComboBox{
    background-color: #242424;
    color: #EFEFEF;
    border: none;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 12px;
    height:26px;
}
QComboBox::drop-down {
    border: none
}
QComboBox::down-arrow {
    image: url(Assets/RightPanel/dropdownArrowWhite.png);
    
}

QComboBox QAbstractItemView {
    background-color: #242424;
    color: #EFEFEF;
    selection-background-color: rgba(0,0,0,0);
    selection-color: #76D4D4;
    border: none;
    padding: 5px;
    margin: 2px;
}
"""

sliderStyle = """
QSlider::handle {
            background-color: #76D4D4;
            width: 5px;
            height: 7px;
            border-radius: 5px;
        }
        """
valueBoxStyle = """
QLineEdit{
    background-color: #242424;
    color: #EFEFEF;
    border: none;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 12px;
    height:26px;
}
"""
tableStyle = """
QTableWidget {
    background-color: #242424;
    color: #EFEFEF;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 12px;
    border: none;
    padding: 10px;
}

QTableWidget::item {
    border-bottom: 1px solid #2D2D2D;
}
"""