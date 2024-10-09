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
            background-color: #ef233c;
            border: 1px solid #ef233c;
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }

        QSlider::groove:horizontal {
            border: 0px solid #606060;
            height: 30px;
            background-color: white;
            margin-top: 7.5px;
        }

        QSlider:hover {
            --brightness-hover: 180%;
        }

        QSlider:pressed {
            --brightness-down: 80%;
        }
        """