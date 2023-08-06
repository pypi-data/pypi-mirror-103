// Copyright (c) Mito

import React from 'react';

// Import css
import "../../css/formula-bar.css";
import "../../css/widths.css"
import "../../css/mito.css"

const FormulaBar = (props: {
    formulaBarValue: string, 
}): JSX.Element => {

    return(
        <div className="vertical-align-content formula-bar-container">
            <div className="formula-bar">
                <p className="fx-text vertical-align-content">Fx</p>
                <div className="vertical-line"></div>
                <input className="formula-bar-input w-100p" value={props.formulaBarValue} disabled />
            </div>
        </div>
    )
}

export default FormulaBar
